# 摸鱼神器 —— 在终端浏览 HelloGitHub

> 本文不会涉及太多技术细节和源码，请放心食用

<img src="./images/cover.jpg" style="zoom:80%;" />

自从对 [tui-rs](https://github.com/fdehau/tui-rs) 产生兴趣后，就一直在琢磨如何能基于她写出一个终端应用呢？写一个什么应用呢？

[hellogithub.com](https://hellogithub.com/) 本就是我平时没事喜欢闲逛的网站，一个想法很自然的就产生了，我能不能在终端浏览呢？

## 一、初步构思

首先我希望这个应用能有以下功能：

- 有搜索框，可以按关键词搜索 hellogithub 中的任意项目
- 通过表格按列展示搜索结果
- 既然是终端应用，那操作方式肯定是使用键盘方式，快捷键我采用了一些大家熟知的 Vim 快捷键
- 浏览项目的途中，可以随时在浏览器中打开当前浏览的项目

有了这些主要功能点的思路，下面就要想想怎么设计一个界面了，我本职工作是一条后端 🐶，一碰到画界面就头疼，几经周折，大概把界面设计成了这样：

![](./images/1.png)

又因为是 TUI 界面层级不能太深，所以再多弄个详情页面（用来浏览文字明细）或者弹窗页面（提示消息）就差不多了，我又想到了 GitHub 为每一种编程语言都设计了一种颜色，我可以把这些颜色应用在我的项目里，让整个终端界面看起来没那么单调，色彩更丰富。我这里展示下目前的成品效果图

主界面：

![](./images/2.png)

详情页：

![](./images/3.png)

弹窗提示：

![](./images/4.png)

最后为了向 TUI 妥协，按期数或类别搜索，我是通过使用搜索前缀来和普通关键词搜索作出区别

上面展示的这些差不多已经是这个项目的全部了

## 二、技术选型

要实现上述的那些功能，就要从 Rust 的生态中选择合适的库了

下面这些是我这个项目中使用到的：

- 基础设施： `anyhow`、`thiserror`、`lazy_static`、`better-panic`
- 绘制 UI：`tui`、`crossterm`
- HTTP client：`reqwest`
- 缓存：`cached`
- HTML 解析：`nipper`
- 工具：`regex`、`crossbeam-channel`
- 命令行：`clap`

Rust 虽然还是编程界的小学生（2011 年启动），但是经过了这些年的发展，生态已经逐渐完善（和几位大哥还是差很多），加上 Rust 是系统级的语言，所以我相信未来 Rust 一定能成为多面手。

项目目录规划（非全部）

```rust
src
├── app.rs			// 统一管理整个应用的状态
├── cli.rs			// 命令行解析
├── draw.rs			// 绘制 UI
├── events.rs		// UI 事件、输入事件、通知
├── fetch.rs		// HTTP 请求
├── main.rs			// 入口
├── parse.rs		// HTML 解析
├── utils.rs		// 工具
└── widget 			// 自定义组件
    ├── ...
```

合理的分文件（目录）开发，可以让每个功能模块 高内聚、低耦合，并且可以很容易的分开进行单元测试。

当然这些文件也不是在项目之初就已经一股脑的建立好的，都是在完善功能的路上一点点添加进来的～

## 三、实现代码片段

因为是基于 `tui-rs` 开发的应用，所以主流程肯定是遵循该库的设计的，首先需要定义一个 `App` 用来保存整个项目的状态信息

```rust
pub struct App {
    /// 用户输入框
    pub input: InputState,

    /// 内容展示
    pub content: ContentState,

    /// 弹窗提示
    pub popup: PopupState,

    /// 状态栏
    pub statusline: StatusLineState,

    /// 模式
    pub mode: AppMode,

    /// 项目明细子页面
    pub project_detail: ProjectDetailState,
		
  	...
}

```

每一个状态字段其实就是对应一个自定义组件，要在 `tui-rs` 中实现自定义组件（实现方式也是我自己的理解）也很简单，只要三步，我以 `Input` 组件为例

```rust
/// 用户输入框组件，组件本身没有字段，是一个无状态的对象
/// 无状态对象只关心 UI 怎么绘制，不存储数据
pub struct Input {}

/// 组件的状态，每一个字段就是组件需要存储的数据
#[derive(Debug)]
pub struct InputState {
    input: String,
    active: bool,
    pub mode: SearchMode,
}

/// 最后为 Input 组件实现 StatefulWidget trait
impl StatefulWidget for Input {
    type State = InputState; // 指定关联类型为 InputState
  
  	/// area 绘制的区域
    /// buf 缓冲区（可以直接写入字符串，如果要高度定制的话，可以理解为画笔）
    /// state 从这个变量中直接取绘制过程中需要的数据
    fn render(self, area: Rect, buf: &mut Buffer, state: &mut Self::State) {
        // 具体绘制的逻辑
      	...
    }
}
```

只要是面向用户的应用都会处理各种各样的用户输入（事件），Rust 中一般都使用 channel 来解耦处理各种各样的事件，再利用 Rust 强大的枚举支持，定义各种各样的事件（用户输入和非用户输入）

```rust
/// 定义事件枚举
#[derive(Debug, Clone)]
pub enum HGEvent {
  	/// 用户事件（键盘事件）
    UserEvent(KeyEvent),

  	/// 应用内部组件的通知事件
    NotifyEvent(Notify),
}

#[derive(Debug, Clone, PartialEq)]
pub enum Notify {
    /// 重绘界面
    Redraw,

    /// 退出应用
    Quit,

    /// 弹出窗口展示消息
    Message(Message),

    /// tick，比如一些数据需要每隔一段时间自动更新的（比如：显示的时间）
    Tick,
}

/// 弹窗的消息，分为 错误、警告、提示
#[derive(Debug, Clone, PartialEq)]
pub enum Message {
    Error(String),

    Warn(String),

    Tips(String),
}
```

为了区分用户事件和通知，我使用了两个不同的 channel 分别处理这两类

```rust
lazy_static! {
    /// 因为通知队列希望被应用内部共享，所以使用了 lazy_static 方便使用
    pub static ref NOTIFY: (Sender<HGEvent>, Receiver<HGEvent>) = bounded(1024);
}
```

又因为不同的事件处理，并不应该互相阻塞，所以整个应用采用了最基础的多线程模型来提高性能，这里使用的也是标准库的多线程

```rust
pub fn handle_key_event(event_app: Arc<Mutex<App>>) {
    let (sender, receiver) = unbounded();
    ...

    std::thread::spawn(move || loop {
        // 单独一个线程接收用户事件
        if let Ok(Event::Key(event)) = crossterm::event::read() {
            sender.send(HGEvent::UserEvent(event)).unwrap();
        }
    });
    std::thread::spawn(move || loop {
      	// 单独一个线程处理用户事件
        if let Ok(HGEvent::UserEvent(key_event)) = receiver.recv() {
            ...
        }
    });
}
```

其他剩下的就是本应用的业务逻辑，具体的代码可以直接看仓库 [https://github.com/kaixinbaba/hg-tui](https://github.com/kaixinbaba/hg-tui) 

## 四、开发心路

仔细想想这可能是我写的第一个拥有完整功能的 Rust TUI 项目，从有想法到完成开发前后差不多用了三周不到的时间，期间碰到了各种各样的问题，我整理了一下：

- tui-rs 如何使用，为了看懂她的模板流程，我基本看完了 tui-rs 本身的所有源码（源码很少说实话，并不是一件难事）
- 查看其他使用的 tui-rs 的项目，学习她们是如何使用 tui-rs 的（看了不下数十个项目，如果你有兴趣的话，这里是[地址](https://github.com/fdehau/tui-rs#apps-using-tui)）
- 在生态中寻找合适的 Rust crate 来处理我当前的场景并学会使用她
- 和 Rust 编译器斗智斗勇（Rust 新手的第一座大山，Orz）
- 尽量编写符合 Rust 的代码风格项目

其实一开始我也只是打算把这个项目完成基本功能，然后开源就完事了，但在[蛋蛋](https://github.com/521xueweihan)的建议下我又完成一些功能的完善，但我还是觉得我这个项目太小，没什么可说的，但他说了一句话我影响很深刻：**任何一个开源项目都是从小项目开始的，完成一个开源项目不难，十年如一日的维护才是最难的**。

---

如果你们有什么好的建议，欢迎给我提 [issue](https://github.com/kaixinbaba/hg-tui/issues)

最后如果你喜欢本文章和本项目的话，欢迎点赞，star～爱你们哟～

![](./images/5.jpeg)



