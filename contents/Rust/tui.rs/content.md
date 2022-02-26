# Rust 超好用的跨平台命令行界面库

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，本期介绍让你快速拥有完美命令行界面的跨平台 Rust 库—— **tui.rs**

> 项目地址：https://github.com/fdehau/tui-rs
>
> 官方文档：https://docs.rs/tui/latest/tui/index.html

你一定有过这样的纠结：我的程序需要一个界面，但使用诸如 Qt 等框架又比较繁琐。现在 **tui.rs** 来了，它是 Rust 下的命令行 UI 库，不仅上手方便内置多种组件，而且效果炫酷支持跨平台使用（一份代码可以无缝运行在 Linux/Windows/Mac）之上！让我们看看示例效果：

![img](E:\Article\contents\Rust\tui.rs\images\demo.gif)

下面将详细简介，如何玩转这个库！

## 一、安装

和所有其他 Rust 依赖的安装方法一样，直接在 `cargo.toml` 中添加依赖即可：

```toml
[dependencies]
tui = "0.17"
crossterm = "0.22"
```

如果需要官方示例，则直接 clone 官方仓库：

```shell
$ git clone http://github.com/fdehau/tui-rs.git
$ cd tui-rs
$ cargo run --example demo
```

## 二、快速入门

### 2.1 一览芳容

我们主要使用 ``tui.rs`` 提供的以下模块进行 UI 编写（所有 UI 元素都实现了 ``Widget`` 或 ``StatefuWidget`` Trait）：

- ``bakend``  用于生成管理命令行的后端
- ``layout`` 用于管理 UI 组件的布局
- ``style`` 用于为 UI 添加样式
- ``symbols`` 描述绘制散点图时所用点的样式
- ``text`` 用于描述带样式的文本
- ``widgets`` 包含预定义的 UI 组件

如下代码就可以实现一个很简单的 ``tui`` 界面：

```rust
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use std::{io, time::Duration};
use tui::{
    backend::{Backend, CrosstermBackend},
    layout::{Alignment, Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    text::{Span, Spans, Text},
    widgets::{Block, Borders, Paragraph, Widget},
    Frame, Terminal,
};

struct App {
    url: String, // 存放一些数据或者 UI 状态
}
fn main() -> Result<(), io::Error> {
    // 初始化终端
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;
    let mut app = App {
        url: String::from(r"https://hellogithub.com/"),
    };
    // 渲染界面
    run_app(&mut terminal, app)?;
    // 恢复终端
    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;

    Ok(())
}

fn run_app<B: Backend>(terminal: &mut Terminal<B>, mut app: App) -> io::Result<()> {
    loop {
        terminal.draw(|f| ui(f, &mut app))?;
        // 处理按键事件
        if crossterm::event::poll(Duration::from_secs(1))? {
            if let Event::Key(key) = event::read()? {
                match key.code {
                    KeyCode::Char(ch) => {
                        if 'q' == ch {
                            break;
                        }
                    }
                    _ => {}
                }
            }
        }
        // 处理其他逻辑
    }
    Ok(())
}
fn ui<B: Backend>(f: &mut Frame<B>, app: &mut App) {
    //
    let chunks = Layout::default() // 首先获取默认构造
        .constraints([Constraint::Length(3), Constraint::Min(3)].as_ref()) // 按照 3 行 和 最小 3 行的规则分割区域
        .direction(Direction::Vertical) // 垂直分割
        .split(f.size()); // 分割整块 Terminal 区域
    let paragraph = Paragraph::new(Span::styled(
        app.url.as_str(),
        Style::default().add_modifier(Modifier::BOLD),
    ))
    .block(Block::default().borders(Borders::ALL).title("HelloGitHub"))
    .alignment(tui::layout::Alignment::Left);
    f.render_widget(paragraph, chunks[0]);

    let paragraph = Paragraph::new("分享 GitHub 上有趣、入门级的开源项目")
        .style(Style::default().bg(Color::White).fg(Color::Black))
        .block(Block::default().borders(Borders::ALL).title("宗旨"))
        .alignment(Alignment::Center);
    f.render_widget(paragraph, chunks[1]);
}
```

![image-20220226184137749](E:\Article\contents\Rust\tui.rs\images\2.png)

**这些代码可能看起来不少，但大部分都是固定的模板，不需要我们每次的重新构思**。下面，就让我们来详细了解其中的细节

### 2.2 创作模板

官方通过 example 给出了使用 ``tui.rs`` 进行设计的模板，我希望各位读者在使用时也能遵守这套模板以保证程序的可读性。

一个使用 ``tui.rs`` 程序的一生大概是这样的：



![未命名绘图](E:\Article\contents\Rust\tui.rs\images\1.png)

其模块可以大致分为：

- ``app.rs`` 实现 App 结构体，用于处理 UI 逻辑，保存 UI 状态
- ``ui.rs``   实现 UI 渲染功能

但对于小型程序来讲，也可以都写在 ``main.rs`` 之中。

首先来看开始和结束部分关于 Terminal 的操作，每次运行都会保存原始 Terminal 界面内容并在一个新的窗体上运行，在结束后又会恢复到原来的 Terminal 窗体中，有效地防止了搞乱原来的窗口内容。**这部分代模板码官方已经给出，基本无需修改**：

```rust
fn main() -> Result<(), io::Error> {
    // 配置 Terminal
    enable_raw_mode()?; // 启动命令行的 raw 模式
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?; // 在一个新的界面上运行 UI，保存原终端内容，并开启鼠标捕获
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;
    // 初始化 app 资源
    let mut app = App {
        url: String::from(r"https://hellogithub.com/"),
    };
 	// 程序主要逻辑循环 …… //
    run_app(&mut terminal, app)?;
    // 恢复 Terminal
    disable_raw_mode()?;	// 禁用 raw 模式
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,	// 恢复到原来的命令行窗口
        DisableMouseCapture		// 禁用鼠标捕获
    )?;
    terminal.show_cursor()?; // 显示光标

    Ok(())
}
```

接下来是处理 UI 逻辑的 ``run_app`` 函数，我们在此处理诸如 用户按键、UI 状态更改等逻辑

```rust
fn run_app<B: Backend>(terminal: &mut Terminal<B>, mut app: App) -> io::Result<()> {
    loop {
        // 渲染 UI
        terminal.draw(|f| ui(f, &mut app))?;
        // 处理按键事件
        if crossterm::event::poll(Duration::from_secs(1))? { // poll 方法非阻塞轮询
            if let Event::Key(key) = event::read()? { // 直接 read 如果没有事件到来则会阻塞等待
                match key.code { // 判断用户按键
                    KeyCode::Char(ch) => {
                        if 'q' == ch {
                            break;
                        }
                    }
                    _ => {}
                }
            }
        }
        // 处理其他逻辑
    }
    Ok(())
}
```

对于功能简单的界面来讲，这个函数作用不大。但如果我们的程序需要更新一些组件状态（比如列表选中项、用户输入、外界数据交互等）则应在此通统一处理。

之后，我们会使用 ``terminal.draw()`` 方法绘制界面，其接受一个闭包：

```rust
fn ui<B: Backend>(f: &mut Frame<B>, app: &mut App) {
    // 获取分割后的窗口
    let chunks = Layout::default() // 首先获取默认构造
        .constraints([Constraint::Length(3), Constraint::Min(3)].as_ref()) // 按照 3 行 和 最小 3 行的规则分割区域
        .direction(Direction::Vertical) // 垂直方向分割
        .split(f.size()); // 分割整块 Terminal 区域
    let paragraph = Paragraph::new(Span::styled(
        app.url.as_str(),
        Style::default().add_modifier(Modifier::BOLD),
    ))
    .block(Block::default().borders(Borders::ALL).title("HelloGitHub"))
    .alignment(tui::layout::Alignment::Left);
    f.render_widget(paragraph, chunks[0]);

    let paragraph = Paragraph::new("分享 GitHub 上有趣、入门级的开源项目")
        .style(Style::default().bg(Color::White).fg(Color::Black))
        .block(Block::default().borders(Borders::ALL).title("宗旨"))
        .alignment(Alignment::Center);
    f.render_widget(paragraph, chunks[1]);
}
```

在这里，有如下流程：

1. 使用 ``Layout`` 按照需求给定 ``Constraint`` 切分窗体，获取 chunks，每个 chunk 也可以利用 ``Layout`` 继续进行分割
2. 实例化组件，每个组件都实现了 ``default`` 方法，在使用时我们应该先使用 ``xxx::default()`` 获取默认对象，再利用默认对象更新组件样式。例如 ``Block::default().borders(Borders::ALL)`` 、``Style::default().bg(Color::White)`` 等。这也是官方推荐做法。
3. 使用 ``f.render_widget`` 渲染组件到窗体上，对于类似 列表 等存在状态（比如当前选中元素）的组件，则使用 ``f.render_stateful_widget`` 进行渲染

关于 ``tui.rs`` 其他内置组件的使用方法，可以查看官方的 example 文件，**编写套路是一样的，可以根据需要直接复制粘贴**。

需要注意到是，**在此我们只关心 UI 组件的显示方式和内容，有关程序逻辑的内容应放在 ``run_app`` 中处理**以免打乱程序架构或影响 UI 绘制效果（你总不希望 UI 绘制到一半的时候因为进行了某些 IO 操作而卡住了对吧？）

## 三、结尾

到这里对于 ``tui.rs`` 的介绍就结束了，实际上使用 ``tui.rs`` 编写 UI 界面很简单，**只要根据创作模板结合官方例子一步步构建**，任何人都可以很快上手。

最后，感谢您的阅读。这里是 HelloGitHub 分享 GitHub 上有趣、入门级的开源项目。您的每个点赞、留言、分享都是对我们最大的鼓励!