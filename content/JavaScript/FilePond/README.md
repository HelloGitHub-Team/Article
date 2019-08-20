# JavaScript上传库：FilePond

> Filepond是一个JavaScript文件上传库，可以上传你投入的任何内容，优化图像以加快上传速度，并提供出色的，可访问的，如丝般顺畅的用户体验。

![](filepond.png)

**HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，今天给大家带来JavaScript开源项目——FilePond**

> **FilePond项目地址https://github.com/pqina/filepond**

## FilePond吸引点

**不重复叙述官方给出的优点：**

- **功能丰富**

  **FilePond是由多个插件组合而成。**

  

- **多平台**

  **支持多平台总能满足你（React，Vue，Angular，jQuery）**

## FilePond插件

* File Rename  (重命名客户端上的文件)
* File Encode (将文件编码为base64数据)
* File size Validation   (文件大小验证工具) 
* File Type Validation  （文件类型验证工具）
* File Metadata    （限制要添加的文件类型）
* File Poster  （在文件项目中显示图像）
* Image Preview  (显示图像文件的预览)
* Image Edit   （手动编辑图像文件）
* Image Crop  （设置图像文件的裁剪比例）
* Image Resize  （设置图像文件的输出尺寸）
* Image Transform  （上传之前在客户端上图像变换）
* Image EXIF Orientation (提取[EXIF](https://baike.baidu.com/item/Exif/422825?fr=aladdin)方向信息)
* Image Size Validation (限制要添加的图像的尺寸)
* Image Filter  (将颜色矩阵应用于图像像素)

## FilePond使用

> 我们这里只使用CND引入方法，后期开展了其他系列（React，Vue，Angular）再将其补全。

```html
<!DOCTYPE html>
<html>
<head>
  <title>FilePond from CDN</title>

  <!-- Filepond stylesheet -->
  <link href="https://unpkg.com/filepond/dist/filepond.css" rel="stylesheet">

</head>
<body>

  <!-- We'll transform this input into a pond -->
  <input type="file" class="filepond">

  <!-- Load FilePond library -->
  <script src="https://unpkg.com/filepond/dist/filepond.js"></script>

  <!-- Turn all file input elements into ponds -->
  <script>
  FilePond.parse(document.body);
  </script>

</body>
</html>
```

![](WX.png)

### 引入插件

```html
<!-- add before </body> -->
<script src="https://unpkg.com/filepond-plugin-file-encode/dist/filepond-plugin-file-encode.js"></script>
<script src="https://unpkg.com/filepond/dist/filepond.js"></script>

<script>
// Register the plugin
FilePond.registerPlugin(FilePondPluginFileEncode);

// ... FilePond initialisation code here
</script>
```

### 结合插件

```html
<!DOCTYPE html>
<html>
<head>
    <title>FilePond from CDN</title>

    <!-- Filepond stylesheet -->
    <link href="https://unpkg.com/filepond/dist/filepond.css" rel="stylesheet">
    <link href="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css" rel="stylesheet">
    <link href="https://unpkg.com/filepond-plugin-image-edit/dist/filepond-plugin-image-edit.css" rel="stylesheet">


</head>
<body>

<!-- We'll transform this input into a pond -->
<input type="file" class="filepond">

<!-- Load FilePond library -->
<script src="https://unpkg.com/filepond-plugin-image-preview/dist/filepond-plugin-image-preview.js"></script>
<script src="https://unpkg.com/filepond-plugin-image-edit/dist/filepond-plugin-image-edit.js"></script>
<script src="https://unpkg.com/filepond-plugin-file-validate-size/dist/filepond-plugin-file-validate-size.js"></script>
<script src="https://unpkg.com/filepond-plugin-file-validate-type/dist/filepond-plugin-file-validate-type.js"></script>
<script src="https://unpkg.com/filepond-plugin-image-crop/dist/filepond-plugin-image-crop.js"></script>
<script src="https://unpkg.com/filepond-plugin-image-exif-orientation/dist/filepond-plugin-image-exif-orientation.js"></script>

<script src="https://unpkg.com/filepond/dist/filepond.js"></script>

<!-- Turn all file input elements into ponds -->
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

![](upload.png)

### 推荐其他组件

> Doka.js -- A JavaScript Image Editor for your Website

![](doka.png)

**由于是需要付费的所有和代码就不附上，如果感兴趣的可以去官网了解一下。**

**Doka.js官网地址：https://pqina.nl/doka/#pricing**

## 总结

**这是一款很轻便的上传插件，并没有太多繁琐的配置，这里并没有针对所以插件引入进行演示，FilePond还是一款很值得参考使用的JavaScript库，如果想让自己网站快速加入上传功能，不妨试试它吧。还有这款插件最值得称赞的就是和Doka.js图像编辑库结合，可惜是需要付费使用，企业级可以去感受一下吧，极其舒服。**

## 参考资料

- **[FilePond 官方文档](https://pqina.nl/filepond/docs/)**
- **[FilePond Plugins List](https://pqina.nl/filepond/plugins.html)**