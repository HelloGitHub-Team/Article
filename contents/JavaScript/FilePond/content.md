# 功能强大的 JS 文件上传库：FilePond

![](images/0.png)

<p align="center">本文作者：HelloGitHub-<strong>kalifun</strong></p>

这是 HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，今天给大家推荐一个 JavaScript 开源的文件上传库项目——FilePond

## 一、介绍

### 1.1 FilePond
它是一个 JavaScript 文件上传库。可以拖入上传文件，并且会对图像进行优化以加快上传速度。让用户体验到出色、进度可见、如丝般顺畅的用户体验。

> FilePond 项目地址：https://github.com/pqina/filepond

![](images/1.gif)

### 1.2 特点和优势
- 上传内容：支持目录、文件、多个文件、本地路径、远程 URL 等。
- 文件管理：删除文件、选择文件、复制和粘贴文件、或使用 API 方式添加文件。
- 上传方式：使用 AJAX 进行异步上传、或将文件编码为 base64 数据用表单发送。
- 图像优化：自动调整图像大小、裁剪和修复 EXIF 方向。
- 响应式：可在移动和桌面设备上使用。

看了效果图和功能介绍，是不是有些手痒了。接下来就是实战操作部分，大家可以跟着文章一步步的把这个库使用起来，点亮你的文件上传技能点！


## 二、实战操作

下面我们将一步步的讲解如何使用 FilePond 这个库。我们采用的是最简单的 CDN 引用方式，方便大家能够快速体检其魅力（复制代码便可查看效果），接着会深入讲解每个插件的功能，最终编写了一个组合了几个插件的示例及运行效果展示。

**Tips：** 解释说明均在代码中以注释方式展示，请大家注意阅读。

### 2.1 快速使用（CDN）
示例代码：

```html
<!DOCTYPE html>
<html>
<head>
    <!-- html 标题 -->
    <title>FilePond from CDN</title>

    <!-- 引入Filepond的css -->
    <link href="https://unpkg.com/filepond/dist/filepond.css" rel="stylesheet">

</head>
<body>

<!-- input标签作为文件上传入口 -->
<input type="file" class="filepond">

<!-- 引入FilePond的js -->
<script src="https://unpkg.com/filepond/dist/filepond.js"></script>


<script>
  // FilePond.parse 使用类.filepond解析DOM树的给定部分，并将它们转换为FilePond元素。
  FilePond.parse(document.body);

</script>

</body>
</html>
```

展示效果：

![](images/3.png)

### 2.2 引入插件

似乎单纯的上传功能是否无法满足我们的需求，FilePond 该库拥有多样、强大的插件部分，可以根据自己的需求选择插件组合起来使用哦。​下面先简单的了解一下每个插件的功能：
* File Rename：重命名客户端上的文件
* File Encode：将文件编码为 base64 数据
* File size Validation：文件大小验证工具
* File Type Validation：文件类型验证工具
* File Metadata：限制要添加的文件类型
* File Poster：在文件项目中显示图像
* Image Preview：显示图像文件的预览
* Image Edit：手动编辑图像文件
* Image Crop：设置图像文件的裁剪比例
* Image Resize：设置图像文件的输出尺寸
* Image Transform：上传之前在客户端上图像变换
* Image EXIF Orientation：提取 [EXIF](https://baike.baidu.com/item/Exif/422825?fr=aladdin) 方向信息
* Image Size Validation：限制要添加的图像的尺寸
* Image Filter：将颜色矩阵应用于图像像素

下面我来介绍如何引入插件吧！

**坑！：** 使用插件前，一定要查阅清楚该插件是否有 CSS 文件，如果有请在`<head><link href="xxx.css" rel="stylesheet"></head>`标签中引入哦。

```html
<head>
  <!-- 引入图像预览插件的css文件 -->
  <link href="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css" rel="stylesheet">
</head>
<!-- 引入图像预览插件的js文件 -->
<script src="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js"></script>

<script>

// 注册插件 FilePondPluginImagePreview 图像预览插件为已上传的图像呈现缩小的预览。
FilePond.registerPlugin(FilePondPluginImagePreview);
</script>
```

我们梳理一下引入插件的步骤：
1. 引入 CSS 文件（部分插件有 CSS 文件）
2. 引入 JS 文件
3. 注册插件
4. 配置插件（部分插件需配置）

### 2.3 配合插件使用

完整示例代码：

```html
<!DOCTYPE html>
<html>
<head>
    <title>FilePond from CDN</title>

    <!-- Filepond CSS -->
    <link href="https://unpkg.com/filepond/dist/filepond.css" rel="stylesheet">
    <!--    FilePondPluginImagePreview 插件 CSS-->
    <link href="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css" rel="stylesheet">
    <!--    FilePondPluginImageEdit 插件 CSS-->
    <link href="https://unpkg.com/filepond-plugin-image-edit/dist/filepond-plugin-image-edit.css" rel="stylesheet">
</head>

<body>

<!-- 我们将把这个输入框变成上传文件框 -->
<input type="file" class="filepond">

<!-- FilePondPluginImagePreview 插件js-->
<script src="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js"></script>
<!--FilePondPluginImageEdit 插件js-->
<script src="https://unpkg.com/filepond-plugin-image-edit/dist/filepond-plugin-image-edit.js"></script>
<!--FilePondPluginFileValidateSize 插件js-->
<script src="https://unpkg.com/filepond-plugin-file-validate-size/dist/filepond-plugin-file-validate-size.js"></script>
<!--FilePondPluginFileValidateType 插件js-->
<script src="https://unpkg.com/filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.js"></script>
<!--FilePondPluginImageCrop 插件js-->
<script src="https://unpkg.com/filepond-plugin-image-crop/dist/filepond-plugin-image-crop.js"></script>
<!--FilePondPluginImageExifOrientation 插件js-->
<script src="https://unpkg.com/filepond-plugin-image-exif-orientation/dist/filepond-plugin-image-exif-orientation.js"></script>
<!--引入Filepond的js-->
<script src="https://unpkg.com/filepond/dist/filepond.js"></script>

<script>
    // querySelector() 方法返回文档中匹配指定 CSS 选择器的一个元素。
    var inputElement = document.querySelector('input[type="file"]');

    // 注册插件
    // FilePondPluginImagePreview  上传时可以预览到上传的图片等
    // FilePondPluginImageEdit   由于doka收费，所以编辑功能就不演示了。
    // FilePondPluginFileValidateType  图片类型
    // FilePondPluginImageCrop 图像裁剪
    // FilePondPluginFileValidateSize   文件大小验证插件处理阻止太大的文件。
    FilePond.registerPlugin(
        FilePondPluginImagePreview,
        FilePondPluginImageEdit,
        FilePondPluginFileValidateSize,
        FilePondPluginImageCrop,
        FilePondPluginFileValidateType,
        FilePondPluginImageExifOrientation

    );

    FilePond.setOptions({
        // 设置单个URL是定义服务器配置的最基本形式。
        server: '/upload',
        // 设置图片类型只能为png才能上传
        allowFileTypeValidation: false,
        acceptedFileTypes: "image/jpg",
        // 启用或禁用图像裁剪
        allowImageCrop: true,

        // 启用或禁用文件大小验证
        allowFileSizeValidation: true,
        maxFileSize: null,

        // 启用或禁用提取EXIF信息
        allowImageExifOrientation: true

    });

    // 使用create方法逐步增强基本文件输入到FilePond元素。
    FilePond.create(inputElement)
</script>

</body>
</html>
```

上面的示例展示了 FilePond 常用插件的方法，效果展示如下：
![](images/4.png)

当然还有其它方法如：
- destroys：销毁实例
- find：返回附加提供的元素的实例
- getOptions：返回当前的配置项
- supported：鉴别浏览器是否支持 FilePond

这里就不做完整的讲解了，有兴趣的可以自行尝试使用这些方法。

## 三、总结

以上就是讲解的全部内容，FilePond 是一款很轻便的上传插件。并没有太多繁琐的配置，这里我并没有逐一针对每个插件引入进行演示，只展示了常用的部分。留意上面提示的坑，掌握上面讲解的方法，其它的插件你便可自行学习。

FilePond 是一款很值得参考和使用的 JavaScript 库，如果想让自己网站快速加入上传功能，不妨试试它吧。


## 四、参考资料

- [FilePond 官方文档](https://pqina.nl/filepond/docs/)
- [FilePond Plugins List](https://pqina.nl/filepond/plugins.html)