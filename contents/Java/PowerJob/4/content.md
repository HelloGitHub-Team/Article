# 哇咔咔干货来啦：PowerJob 原理剖析之 Akka Toolkit
> 本文适合有 Java 基础知识的人群

![](../cover.png)

作者：HelloGitHub-**Salieri**

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列。

> Akka is a toolkit for building highly concurrent, distributed, and resilient message-driven applications for Java and Scala.

上面这段文字摘抄自 Akka 官网（akka.io），翻译成中文也就是：“Akka 是一个为 Java 和 Scala 构建高并发、分布式和弹性消息驱动应用程序的工具包”。而 Akka 具有的一切特性，其实都源自于一个用于处理并发计算问题的模型——Actor 模型。

> PowerJob 项目地址：
>
> https://github.com/KFCFans/PowerJob

## 一、Actor 模型

Actor 模型在 1973 年于 Carl Hewitt、Peter Bishop 及 Richard Steiger 的论文中提出，现在已经被用作并发计算的理论理解框架和并发系统的实际实现基础。

在计算机科学中，Actor 模型是一种并发运算上的模型。Actor 是一种程序上的抽象概念，被视为并发运算的基本单元：当一个 Actor 接收到一则消息，它可以做出一些决策、创建更多的 Actor 、发送更多的消息、决定要如何处理接下来的消息。Actors 可以修改它们自己的私有状态，但是只能通过消息间接的相互影响（避免了基于锁的同步）。

每一个 Actor 都由状态（State）、行为（Behavior）和邮箱（MailBox，其实就是一个消息队列）三部分组成：

- 状态：Actor 中的状态指 Actor 对象的变量信息，状态由 Actor 自己管理，避免了并发环境下的锁和内存原子性等问题。
- 行为：Actor 中的计算逻辑，通过 Actor 接收到的消息来改变 Actor 的状态。
- 邮箱：邮箱是 Actor 和 Actor 之间的通信桥梁，邮箱内部通过 FIFO（先入先出）消息队列来存储发送方 Actor 消息，接受方 Actor 从邮箱队列中获取消息。

![](1.png)

前面说了一大堆晦涩难懂的概念，相信大家看的也都云里雾里的。这里结合我自己的理解用白话文讲一下：其实 Actor 模型的设计思想就是事件驱动，可以简单理解为线程级的消息中间件。所有 Actor 之间不共享数据，只通过消息沟通，因此不用关心传统并发程序编写过程中的并发安全问题（因为根本没有共享的数据）。同时，得益于 Actor 底层轻巧的设计（这部分其实属于具体实现了，不过目前所有的实现 Actor 设计都很轻量），使得单机可以存在百万量级的 Actor，因此能够带来极好的并发性能。

此外，由于 Actor 模型中万物都是 Actor，所以它是天然支持分布式的，即不同机器之间的 Actor 通讯和本地 Actor 之间的通讯没有实质上的区别。

因此，只要你掌握了事件驱动的编程思想，利用 Actor 模型，结合具体的实现框架（比如 JVM 系的 Akka），能够轻松编写出高性能的分布式应用。

## 二、Akka Toolkits

Akka Toolkit 也就是 Akka 工具包，其实就是 JVM 平台上对 Actor 模型的一种实现。Akka 本身提供了完整的 Actor 模型支持，包括对并发/并行程序的简单的、高级别的抽象、异步、非阻塞、高性能的事件驱动编程模型和非常轻量的事件驱动处理。同时，作为一个“工具包”，Akka 还额外提供了许多功能，由于篇幅有限，这里就简单介绍几个包，有兴趣可以前往官网（见参考文档）详细了解～

* akka-streams：流处理组件，提供直观、安全的方式来进行异步、非阻塞的背压流处理。

* akka-http：HTTP 组件，现代、快速、异步、流媒体优先的 HTTP 服务器和客户端。

* akka-cluster：集群组件，包括集群成员管理、弹性路由等。

* akka-remote(artery-remoting)：通讯组件，也是 PowerJob 所使用的核心组件，然而官网并不推荐直接使用（直接使用 remote 启动还会警告使用了过于底层的 API），普通分布式应用推荐直接使用 cluster。

* akka-persistence：持久化组件，提供“至少投递一次”的能力来保证消息的可靠送达。

## 三、Akka 简单使用

接下来是关于 Akka 的一个超简明教程，帮助大家初步理解并入门 Akka，其内容涵盖了所有 PowerJob 中用到的 API，也就是说，看懂这部分，源码中的 Akka 就不再可怕喽～

### 3.1 开发 Actor

首先，不得不提的一点是，Akka 从 2.6 版本开始，维护了 2 套 API（算上 Scala 和 Java 版本就 4 套了...看着IDE的智能提示就头大...），分别叫 classic 和 typed。typed 与原先的 classic 相比，最大的特色就是其具有了类型（Java 范型）。每一个 Actor 处理的消息类型可以直接由范型规定，从而有效限制程序 bug（将错误从运行期提前到了编译期）。然而，对于复杂系统要处理的消息不胜枚举，强类型就限制了一个 Actor 只能处理一种类型的消息。虽然从逻辑上来讲确实清晰，但实际工程实现中，必然导致代码阅读困难，整体结构松散（个人感觉这一点也是计算机科学与工程之间存在分歧的表现，当然也可能是我学艺不精，不了解正确的用法）。解释了那么多，终于可以点明主旨了～作者比较喜欢 classic，因此 PowerJob 只使用 AKKA classic API，本文也只涉及 AKKA classic API，反正官网说了会长期维护～

前面说过，对于 Actor 模型个人认为最简单的理解方式就是消息中间件。Actor 的本质是事件驱动，即接收消息并处理。反映到编程上，Actor 的开发也类似于消息中间件 consumer 的开发，无非是换了个接口、多几个功能罢了。

话不多说，看代码：

```java
public class FriendActor extends AbstractActor {
  
    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(Ping.class, this::onReceivePing)
                .matchAny(obj -> log.warn("unknown request: {}.", obj))
                .build();
    }

    private void onReceivePing(Ping ping) {
        getSender().tell(AskResponse.succeed(null), getSelf());
    }
}
```

首先自然是新建类并实现接口 `AbstractActor`，该接口需要重写 `createReceive` 方法，该方法需要一个 `Receive` 对象作为返回值。对于开发者而言，需要做的就是构建这个 `Receive` 对象，也就是指明该 Actor 接受到什么类型的消息时进行什么样的处理。

### 3.2 初始化 ActorSystem

Actor 作为处理消息的“角色”，就像工厂中的一个个工人，每个人各司其职，兢兢业业地接收指令完成任务。然而群龙不能无首，就像现实生活中工人需要由工厂来组织管理一样，Actor 也需要自己的工厂—— ActorSystem。为此，创建 Actor 之前，首先需要创建 ActorSystem。

PowerJob 使用以下方法创建 ActorSystem。其中，第一个参数指明了该 ActorSystem 的名称，第二个参数则传入了该 ActorSystem 所使用的配置信息，包括工作端口、序列化方式、日志级别等。

```java
actorSystem = ActorSystem.create("powerjob-server", akkaConfig);
```

完成 ActorSystem 这个“工厂”的创建后，就可以正式开始创建 Actor 了，代码如下所示：

```java
actorSystem.actorOf(Props.create(FriendActor.class), "friend_actor");
```

其中，第一个参数Props是一个用来在创建 Actor 时指定选项的配置类；

第二个参数则指定了该 Actor 的名称，通过该 Actor 的名称和其 ActorSystem 的名称，我们就可以构建出路径 `akka://powerjob-server/user/server_actor`（本地路径，远程路径需要变更协议并添加地址），然后轻松得根据该路径找到该 Actor，实现通信。

### 3.3 信息交互

完成 ActorSystem 的初始化和 Actor 的创建后，就可以正式使用 Akka 框架了。PowerJob 主要使用 Akka 框架的 remote 组件，用于完成系统中各个分布式节点的通讯。

```java
String actorPath = "akka://powerjob-server@192.168.1.1/user/friend_actor";
ActorSelection actorSelect = actorSystem.actorSelection(actorPath);
actorSelect.tell(startTaskReq, null);
```

和其他通讯方式一样，进行通讯前，需要首先获取目标地址。根据 akka-remote 的语法规范，指定目标 Actor 的名称、其所在的 ActorSystem 名称和目标机器地址，即可获取用于通讯的 URI。得到 URI 后，便可通过 `actorselection()` 方法获取 Actorselection 对象。通过 Actorselection 对象，调用 tell 方法就可以向目标 Actor 发送消息了。

那么细心的小伙伴肯定要问了，PowerJob 之所以采用 akka-remote 作为底层通讯框架，是看上了它极简的通讯 API，看到这里，也没发现有多简单啊。发送一个 HTTP 请求，用高层封装库其实也就差不多三行代码的样子，你这用个 Akka 前置准备工作还那么多，说好的简单呢？那么下面就带大家来一探究竟，akka-remote 到底简单在哪里～

首先，如果不选择现有的协议，自己用 Netty 造轮子，那光 server、client、listener、codec 就一大堆代码了。如果使用现有协议如 HTTP，发送也许 3 行代码能搞定，但接收一定远不止三行。HTTP 全称超文本传输协议，那么传输的自然已经是经过序列化的文本数据了，所以接收方需要自行进行解码、解析，更别提异常处理、失败重试等功能了。而 akka-remote 呢？从刚刚 Actor 的代码中可以看出，match 方法后面跟的是一个具体的类，也就是说 Akka 自动帮你完成了反序列化，作为消息的接收方，是真正的拿到就能用，没有任何多余代码。同时，Akka 已经帮你搞定了各种异常后的处理。也就是说，使用 akka-remote，可以让数据接收方非常的简单，只专注逻辑的实现。

其次，在分布式环境中，通讯往往不是单向的。尤其是 PowerJob 这种追求高可用的框架，有时候为了确认消息送达，往往需要应答机制。akka-remote 提供了难以置信的 API 来回复请求：

```java
AskResponse response = new AskResponse(true, "success");
getSender().tell(response, getSelf());
```

通过 `getSender()` 方法，就能获取到消息发送方的 Actor 引用对象，并通过该对象回复信息。

## 四、最后
那么以上就是本篇文章全部的内容啦～

通过本篇文章，我相信大家已经了解了 Actor 模型的基础概念，同时掌握了 JVM 上 Actor 模型的实现——Akka 框架的简单使用。

下一篇文章，就是万众期待的 PowerJob 调度层原理分析啦（小伙伴进群必问榜 TOP 1）～我将会为大家揭秘是什么支撑着 PowerJob 的调度，让我能放肆“吹牛”说调度性能秒杀现有一切框架～

那我们下起再见喽～拜拜～

## 五、参考文献

- [官方文档](https://akka.io/docs/)

- [Actor_model wiki](https://en.wikipedia.org/wiki/Actor_model)

- [Actor 编程模型浅谈](http://jiangew.me/actor-model/)


## 作者游记

![](2.png)