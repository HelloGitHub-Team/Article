# Java 序列化界新贵 kryo 和熟悉的“老大哥”，就是 PowerJob 的序列化方案

> 本文适合有 Java 基础知识的人群

![](../cover.png)

作者：HelloGitHub-**Salieri**

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列。

> 项目地址：
>
> https://github.com/KFCFans/PowerJob

序列化与反序列化一直是分布式编程中无法绕开的话题。PowerJob 作为一个完全意义上的分布式系统，自然少不了节点通讯时不可避免的序列化问题。由于 PowerJob 定位是中间件，出于对性能的追求，在序列化上自然也是花费了不少时间去雕琢。以下是整个过程中的一些经验与分享，希望对大家有所帮助。

## 一、序列化界新贵：kryo

kryo 作为目前最快的序列化框架，自然受到了我的青睐。在 PowerJob 中，kryo 是内置默认的序列化框架。下面为大家介绍 kryo 的用法。

### 1.1 基础用法

对于序列化框架来说，API 其实都差不多，毕竟入参和出参都定义好了（一个是需要序列化的对象，一个是序列化后的结果，比如字节数组）。下面简单介绍下 kryo 的基础用法，由于序列化和反序列化类似，以下使用序列化来作为演示。

```java
Kryo kryo = new Kryo();
try (Output opt = new Output(1024, -1)) {
    kryo.writeClassAndObject(opt, obj);
    opt.flush();
    return opt.getBuffer();
}
```

代码很简单，首先需要创建两个对象：Kryo 和 Output。其中，Kryo 是序列化主角，负责完成实际的序列化/反序列化工作。而 Output 则是 kryo 框架封装的流对象，用于存储序列化后的二进制数据。当两个对象都准备完毕后，调用 `kryo.writeClassAndObject(opt, obj)` 方法即可完成对象的序列化，最后调用 Output 流对象的 `getBuffer()` 方法获取序列化结果，也就是二进制数组。

### 1.2 线程不安全

相信大家都用过 fastjson，初次接触 fastjson 肯定会被它简单的 API 所吸引，常用的序列化/反序列化统统一行代码搞定，比如 `JSON.toJSONString()`。通常来说，这种通过静态方法暴露的 API，其背后的设计与实现都是**线程安全**的，也就是在多线程环境中，你可以安心的使用 fastjson 的静态方法进行序列化和反序列化，那么 kryo 可以吗？

从上述代码不难看出，不可以～否则，人家为什么要多次一举让你创建对象提高使用成本呢？

王进喜同志说过，没有条件就创造条件。既然 kryo 官方不提供静态方法让我们简单使用，那就自己封装一个吧～

![](1.png)

抛开性能因素，封装一个工具类非常简单，毕竟我们的目标是解决 kryo 的并发安全问题，而当没有任何共享资源时，是不存在任何并发安全问题的。那么我们只需要在刚刚的实例代码上，套上一个静态方法，就完成了最简单的kryo 工具类封装，代码示例如下：

```java
public static byte[] serialize(Object obj) {
    Kryo kryo = new Kryo();
    try (Output opt = new Output(1024, -1)) {
        kryo.writeClassAndObject(opt, obj);
        opt.flush();
        return opt.getBuffer();
    }
}
```

安全问题是解决了，但...事情往往不会那么简单。这种模式下，每一次调用都会重复创建 2 个新对象（Kryo 和 Output），这在高并发下会产生一笔不小的开销。为了获取性能的提升，自然要考虑到对象的复用问题。对象的复用常用解决方案有两个，分别是对象池和 ThreadLocal，下面分别进行介绍。

### 1.3 对象池

在编程中，“池”这个名词相信大家一定不陌生。线程池、连接池已经是并发编程中不可避免的一部分。“池”重复利用了复用的思想，将创建完后的对象通过某个容器保存起来反复使用，从而达到提升性能的作用。Kryo 对象池原理上便是如此。Kryo 框架自带了对象池的实现，因此使用非常简单，不外乎**创建池、从池中获取对象、归还对象**三步，以下为代码实例。

首先，创建 Kryo 对象池，通过重写 Pool 接口的 create 方法，便可创建出自定义配置的对象池。

```java
private static final Pool<Kryo> kryoPool = new Pool<Kryo>(true, false, 512) {
    @Override
    protected Kryo create() {
        Kryo kryo = new Kryo();
        // 关闭序列化注册，会导致性能些许下降，但在分布式环境中，注册类生成ID不一致会导致错误
        kryo.setRegistrationRequired(false);
        // 支持循环引用，也会导致性能些许下降 T_T
        kryo.setReferences(true);
        return kryo;
    }
};
```

当需要使用 kryo 时，调用 `kryoPool.obtain()` 方法即可，使用完毕后再调用 `kryoPool.free(kryo)` 归还对象，就完成了一次完整的租赁使用。

```java
public static byte[] serialize(Object obj) {
    Kryo kryo = kryoPool.obtain();
    // 使用 Output 对象池会导致序列化重复的错误（getBuffer返回了Output对象的buffer引用）
    try (Output opt = new Output(1024, -1)) {
        kryo.writeClassAndObject(opt, obj);
        opt.flush();
        return opt.getBuffer();
    }finally {
        kryoPool.free(kryo);
    }
}
```

对象池技术是所有并发安全方案中性能最好的，只要对象池大小评估得当，就能在占用极小内存空间的情况下完美解决并发安全问题。这也是 PowerJob 诞生初期使用的方案，直到...PowerJob 正式推出容器功能后，才不得不放弃该完美方案。

在容器模式下，使用 kryo 对象池计算会有什么问题呢？这里简单给大家提一下，**至于看不看得懂，就要看各位造化了～**

PowerJob 容器功能指的是动态加载外部代码进行执行，为了进行隔离，PowerJob 会使用单独的类加载器完成容器中类的加载。因此，每一个 powerjob-worker 中存在着多个类加载器，分别是系统类加载器（负责项目的加载）和每个容器自己的类加载器（加载容器类）。序列化工具类自然是 powerjob-worker 的一部分，随 powerjob-worker 的启动而被创建。当 kryo 对象池被创建时，其使用的类加载器是系统类加载器。因此，当需要序列化/反序列化容器中的类时，kryo 并不能从自己的类加载器中获取相关的类信息，妥妥的抛出 ClassNotFoundError！

因此，PowerJob 在引入容器技术后，只能退而求其次，采取了第二种并发安全方法：ThreadLocal。

### 1.4 ThreadLocal

ThreadLocal 是一种典型的牺牲空间来换取并发安全的方式，它会为每个线程都单独创建本线程专用的 kryo 对象。对于每条线程的每个 kryo 对象来说，都是顺序执行的，因此天然避免了并发安全问题。创建方法如下：

```java
private static final ThreadLocal<Kryo> kryoLocal = ThreadLocal.withInitial(() -> {
    Kryo kryo = new Kryo();
    // 支持对象循环引用（否则会栈溢出），会导致性能些许下降 T_T
    kryo.setReferences(true); //默认值就是 true，添加此行的目的是为了提醒维护者，不要改变这个配置
    // 关闭序列化注册，会导致性能些许下降，但在分布式环境中，注册类生成ID不一致会导致错误
    kryo.setRegistrationRequired(false);
    // 设置类加载器为线程上下文类加载器（如果Processor来源于容器，必须使用容器的类加载器，否则妥妥的CNF）
    kryo.setClassLoader(Thread.currentThread().getContextClassLoader());
    return kryo;
});
```

之后，仅需要通过 `*kryoLocal*.get()` 方法从线程上下文中取出对象即可使用，也算是一种简单好用的方案。（虽然理论性能比对象池差不少)

## 二、老牌框架：Jackson

大名鼎鼎的 Jackson 相信大家都听说过，也是很多项目的御用 JSON 序列化/反序列化框架。在 PowerJob 中，本着不重复造轮子的原则，在 akka 通讯层，使用了 jackson-cbor 作为默认的序列化框架。


“什么，你问我为什么不用性能更好且已经在项目中集成了的 kryo？”

“那当然是因为 akka 官方没有提供 kryo 的官方实现，于是......”

![](2.png)

如果使用 kryo，则需要自己实现一大堆编解码器，俨然有点写 netty 的味道...而 jackson-cbor 呢？只需要一点小小的配置就能搞定～

```java
actor {
    provider = remote
    allow-java-serialization = off
    serialization-bindings {
        "com.github.kfcfans.powerjob.common.OmsSerializable" = jackson-cbor
    }
  }
```

虽然绝对性能可能不及 kryo，但对比于自带的 Java 序列化方式，性能已经提升 10 倍以上，在绝大部分场景都不会是性能瓶颈。所以～又有什么理由拒绝它呢～

## 三、最后
好了，这就是本文的全部内容了。下篇文章将会为大家带来 PowerJob 的独一无二分布式计算功能背后的原理分析，如此重磅的文章作为本专栏的压轴好戏也是再恰当不过了～

那么，我们下期再见喽～