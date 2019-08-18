为了让博客文章具有良好的排版，显示更加丰富的格式，我们使用 Markdown 语法来书写博文。Markdown 是一种 HTML 文本标记语言，只要遵循它约定的语法格式，Markdown 的解析工具就能够把 Markdown 文档转换为标准的 HTML 文档，从而使文章呈现更加丰富的格式，例如标题、列表、代码块等等 HTML 元素。由于 Markdown 语法简单直观，不用超过 5 分钟就可以轻松掌握常用的标记语法，因此大家青睐使用 Markdown 书写 HTML 文档。下面让我们的博客也支持使用 Markdown 写作。

## 安装 Python Markdown

将 Markdown 格式的文本解析成标准的 HTML 文档是一个复杂的工程，好在已有好心人帮我们完成了这些工作，直接拿来使用即可。首先安装 Markdown，这是一个 Python 第三方库，在**项目根目录**下运行命令 `pipenv install markdown`。

## 在 detail 视图中解析 Markdown 

将 Markdown 格式的文本解析成 HTML 文本非常简单，只需调用这个库的 `markdown` 方法。我们书写的博客文章内容存在 `Post` 的 `body` 属性里，回到我们的详情页视图函数，对 `post` 的 `body` 的值做一下解析，把 Markdown 文本转为 HTML 文本再传递给模板：

```python
blog/views.py

import markdown
from django.shortcuts import get_object_or_404, render

from .models import Post

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request, 'blog/detail.html', context={'post': post})
```

这样我们在模板中显示 `{{ post.body }}` 的时候，就不再是原始的 Markdown 文本了，而是解析过后的 HTML 文本。注意这里我们给 `markdown` 解析函数传递了额外的参数 `extensions`，它是对 Markdown 语法的拓展，这里使用了三个拓展，分别是 extra、codehilite、toc。extra 本身包含很多基础拓展，而 codehilite 是语法高亮拓展，这为后面的实现代码高亮功能提供基础，而 toc 则允许自动生成目录（在以后会介绍）。

来测试一下效果，进入后台，这次我们发布一篇用 Markdown 语法写的测试文章看看，你可以使用以下的 Markdown 测试代码进行测试，也可以自己书写你喜欢的 Markdown 文本。假设你是 Markdown 新手请参考一下这些教程，一定学一下，保证你可以在 5 分钟内掌握常用的语法格式，而以后对你写作受用无穷。可谓充电 5 分钟，通话 2 小时。以下是我学习中的一些参考资料：

- [Markdown——入门指南](http://www.jianshu.com/p/1e402922ee32/)
- [Markdown 语法说明 (简体中文版)](http://www.appinn.com/markdown/)

```markdown
# 一级标题

## 二级标题

### 三级标题

- 列表项1
- 列表项2
- 列表项3

> 这是一段引用

​```python
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request, 'blog/detail.html', context={'post': post})
​```
```

**如果你发现无法显示代码块，即代码无法换行，请检查代码块的语法是否书写有误。代码块的语法如上边的测试文本中最后一段所示。**

你可能想在文章中插入图片，目前能做的且推荐做的是使用外链引入图片。比如将图片上传到七牛云这样的云存储服务器，然后通过 Markdown 的图片语法将图片引入。Markdown 引入图片的语法为：`![图片说明](图片链接)`。

## safe 标签

我们在发布的文章详情页没有看到预期的效果，而是类似于一堆乱码一样的 HTML 标签，这些标签本应该在浏览器显示它自身的格式，但是 django 出于安全方面的考虑，任何的 HTML 代码在 django 的模板中都会被转义（即显示原始的 HTML 代码，而不是经浏览器渲染后的格式）。为了解除转义，只需在模板变量后使用 `safe` 过滤器即可，告诉 django，这段文本是安全的，你什么也不用做。在模板中找到展示博客文章内容的 `{{ post.body }}` 部分，为其加上 safe 过滤器：`{{ post.body|safe }}`，大功告成，这下看到预期效果了。

![Markdown 测试](/Users/yangxg/SpaceNut/12 - Writing - 写作/12A - Blog - 博客写作/12A.02 - Courses - 教程/HelloDjango/blog-tutorial/Pictures/post_markdown.png)

safe 是 django 模板系统中的过滤器（Filter），可以简单地把它看成是一种函数，其作用是作用于模板变量，将模板变量的值变为经过滤器处理过后的值。例如这里 `{{ post.body|safe }}`，本来 `{{ post.body }}`经模板系统渲染后应该显示 body 本身的值，但是在后面加上 safe 过滤器后，渲染的值不再是 body 本身的值，而是由 safe 函数处理后返回的值。过滤器的用法是在模板变量后加一个 | 管道符号，再加上过滤器的名称。可以连续使用多个过滤器，例如 {{ var|filter1|filter2 }}。

## 代码高亮

程序员写博客免不了要插入一些代码，Markdown 的语法使我们容易地书写代码块，但是目前来说，显示的代码块里的代码没有任何颜色，很不美观，也难以阅读，要是能够像代码编辑器里一样让代码高亮就好了。

代码高亮我们借助 js 插件来实现，其原理就是 js 解析整个 html 页面，然后找到代码块元素，为代码块中的元素添加样式。我们使用的插件叫做 highlight.js 和 highlightjs-line-numbers.js，前者提供基础的代码高亮，后者为代码块添加行号。

首先在 base.html 的 head 标签里引入代码高亮的样式，有多种样式供你选择，这里我们选择 Github 主题的样式。样式文件直接通过 CDN 引入，同时在 style 标签里自定义了一点元素样式，使得代码块的显示效果更加完美。

```html
<head>
  ...
  <link href="https://cdn.bootcss.com/highlight.js/9.15.8/styles/github.min.css" rel="stylesheet">

  <style>
    .codehilite {
      padding: 0;
    }

    /* for block of numbers */
    .hljs-ln-numbers {
      -webkit-touch-callout: none;
      -webkit-user-select: none;
      -khtml-user-select: none;
      -moz-user-select: none;
      -ms-user-select: none;
      user-select: none;

      text-align: center;
      color: #ccc;
      border-right: 1px solid #CCC;
      vertical-align: top;
      padding-right: 5px;
    }

    .hljs-ln-n {
      width: 30px;
    }

    /* for block of code */
    .hljs-ln .hljs-ln-code {
      padding-left: 10px;
      white-space: pre;
    }
  </style>
</head>
```

然后是引入 js 文件，因为应该等整个页面加载完，插件再去解析代码块，所以把 js 文件的引入放在 body 底部：

```html
<body>
  <script src="https://cdn.bootcss.com/highlight.js/9.15.8/highlight.min.js"></script>
  <script src="https://cdn.bootcss.com/highlightjs-line-numbers.js/2.7.0/highlightjs-line-numbers.min.js"></script>
  <script>
    hljs.initHighlightingOnLoad();
    hljs.initLineNumbersOnLoad();
  </script>
</body>
</body>
```

非常简单，通过 CDN 引入 highlight.js 和 highlightjs-line-numbers.js，然后初始化了两个插件。再来看下效果，非常完美！

![代码高亮](/Users/yangxg/SpaceNut/12 - Writing - 写作/12A - Blog - 博客写作/12A.02 - Courses - 教程/HelloDjango/blog-tutorial/Pictures/post_code_highlight.png)

