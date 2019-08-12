# 超简单的Tale博客系统-- 5分钟私人订制

**Tale** 是轻量级Java平台的博客系统，实现 小，美，快，稳 的目标，让有故事的人更好的表达想法，程序完全开源免费，面向所有用户。如果你也想快速搭建一套自己的博客，只需要花5分钟，Tale帮你快速构建一套精美的个人博客。下面是效果图：

![](https://pic1.superbed.cn/item/5d4c42a2451253d178012702.png)

## 技术栈

- **Blade 框架**：一款快速搭建一个 Web 应用程序的开源框架，它的代码简洁，风格优雅。 

- **Jetbrick-template 模板引擎**：  适合于动态 HTML 页面输出或者代码生成，可替代 JSP 页面或者 Velocity 等模板。 指令和 Velocity 相似，表达式和 Java 保持一致，易学易用。

- **Sqlite数据库**：是一种嵌入式数据库,它的数据库就是一个文件。

## 源码目录简介

项目结构如下图：

![](https://b2.bmp.ovh/imgs/2019/08/ff12dd72b6cd4ff2.png)

1. 后台代码目录说明

   annotation：自定义注解目录

   bootstarp：初始化操作目录，项目启动的初始化操作

   controller：业务的控制器目录

   extension：底层公用代码目录，包括后台公共函数，主题公共函数

   hooks：拦截器/过滤器目录，做一些拦截器的操作

   model：数据模型目录

   service：业务层目录，实现具体的业务代码

   task：定时任务目录

   utils：业务层工具类目录

   validators：验证器目录

   Application：入口类，在IDE中可直接运行。

2. 前台代码目录说明

   plugins：此目录作者废弃了

   static：静态资源目录，包括css,images,js和第三方插件

   templates：模板资源目录，包括后台管理界面，公共模板和主题模板，支持扩展主题

   application*.properties：项目环境配置文件

   

Tale的项目的结构很简单，当然它运行起来超级简单，你是不是开始手痒痒了，你接下来我们一起让项目运行起来。

## 实战操作

1. 准备工作

   1.确保本地已安装Java8开发环境；

   ![](https://pic.superbed.cn/item/5d4c3fe9451253d17801138c.png)

   

   2.确保本地已安装maven工具；

   ![](https://pic.superbed.cn/item/5d4c3fe9451253d17801138e.png)

   

2. 下载项目

   ```
   git clone https://github.com/otale/tale.git
   ```

3. 运行项目

   1. IDE里面运行

      a.将项目导入到IDE中，这里我使用的是Idea

      ![](https://pic3.superbed.cn/item/5d4c4136451253d178011e5e.png)

      b.找到 com.tale.Application类，直接运行

      ![](https://pic.superbed.cn/item/5d4c4240451253d178012472.png)

      c.运行成功如下图

      ![](https://pic.superbed.cn/item/5d4c4240451253d178012476.png)

   2.命令行运行项目

      a.切换到项目源码路径,编译源码

   ```
   mvn clean package -Pprod -Dmaven.test.skip=true
   ```

   编译成功如下图：
![](https://ae01.alicdn.com/kf/H43fd1ae8a5c6425cae89b125736d9cec6.png)


   b.切换路径到 tale\target\dist\ 

   ![](https://pic3.superbed.cn/item/5d4c3fd0451253d178011289.png)

   c.解压 tale.zip 压缩文件

   ![](https://ae01.alicdn.com/kf/H6c20314a208041de9931ede998e621fcr.png)

   d.运行 tale-latest.jar

   ```
   java -jar  tale-latest.jar
   ```

   启动成功如下图：

   ![](https://ae01.alicdn.com/kf/H636b04d1a2484a778b0de24c870b611fx.png)

   3.在Idea的Terminal窗口执行打包命令

  Idea的Terminal窗口与cmd窗口的功能是相同的。可以执行

   ```
   mvn clean package -Pprod -Dmaven.test.skip=true
   ```

   对源码进行打包，然后也可以在命令行启动项目。

4. 项目启动成功

   1.首次登录，需要填写配置信息

   ![](https://pic.superbed.cn/item/5d4c4240451253d17801247e.png)

   2.登录后台管理系统

   后台系统链接：<http://127.0.0.1:9000/admin/login> 

   输入管理员账号和密码即可登录

   ![](https://pic.superbed.cn/item/5d4c4240451253d178012481.png)

   后台管理页面

   ![](https://pic1.superbed.cn/item/5d4c42a2451253d178012700.png)

   3.博客前台页面

   博客前台链接：<http://127.0.0.1:9000/> 

   ![](https://pic1.superbed.cn/item/5d4c42a2451253d178012702.png)

   

   

参考资料：

https://github.com/otale/tale/wiki

https://lets-blade.com/docs/why-blade.html

https://www.oschina.net/p/jetbrick-template