# 用这个库 3 分钟实现让你满意的表格功能：Bootstrap-Table

![](images/1.png)

<p align="center">本文作者：HelloGitHub-<strong>kalifun</strong></p>

这是 HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，今天给大家推荐一个基于 Bootstrap 和 jQuery 的表格插件：Bootstrap-Table

## 一、介绍

从项目名称就可以知道，这是一款 Bootstrap 的表格插件。表格的展示的形式所有的前端几乎在工作中都有涉及过，Bootstrap Table 提供了快速的建表、查询、分页、排序等一系列功能。

> 项目地址：https://github.com/wenzhixin/bootstrap-table

可能 Bootstrap 和 jQuery 技术有些过时了，但如果因为历史的技术选型或者旧的项目还在用这两个库的话，那这个项目一定会让你的嘴角慢慢上扬，拿下表格展示方面的需求易如反掌！

## 二、模式

Boostatrp Table 分为两种模式：客户端（client）模式、服务端（server）模式。

- **客户端**：通过数据接口将服务器需要加载的数据一次性展现出来，然后装换成 json 然后生成 table。我们可以自己定义显示行数，分页等，此时就不再会向服务器发送请求了。

- **服务器**：根据设定的每页记录数和当前显示页，发送数据到服务器进行查询。

## 三、实战操作
> **Tips：** 解释说明均在代码中以注释方式展示，请大家注意阅读。

我们采用的是最简单的 CDN 引入方式，代码可直接运行。复制代码并将配置好 json 文件的路径即可看到效果。

### 3.1 快速上手

注释中的星号表示该参数必写，话不多说上代码。示例代码：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hello, Bootstrap Table!</title>
    // 引入 css
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.3/css/all.css" integrity="sha384-UHRtZLI+pbxtHCWp1t77Bi1L4ZtiqrqD80Kn4Z8NTSRyMA2Fd33n5dQ8lWUE00s/" crossorigin="anonymous">
    <link rel="stylesheet" href="https://unpkg.com/bootstrap-table@1.15.3/dist/bootstrap-table.min.css">
</head>
<body>
    // 需要填充的表格
    <table id="tb_departments" data-filter-control="true" data-show-columns="true"></table>
// 引入js
<script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js" integrity="sha384-wHAiFfRlMFy6i5SRaxvfOCifBUQy1xHdJ/yoi7FRNXMRBu5WHdZYu1hA6ZOblgut" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js" integrity="sha384-B0UglyR+jN6CkvvICOB2joaf5I4l3gm9GU6Hc1og6Ls7i6U/mkkaduKaBhlAXv9k" crossorigin="anonymous"></script>
<script src="https://unpkg.com/bootstrap-table@1.15.3/dist/bootstrap-table.min.js"></script>
<script>
        window.operateEvents = {
            // 当点击 class=delete 时触发
            'click .delete': function (e,value,row,index) {
                // 在 console 打印出整行数据
                console.log(row);
            }
        };

        $('#tb_departments').bootstrapTable({
            url: '/frontend/bootstrap-table/user.json',         //请求后台的 URL（*）
            method: 'get',                      //请求方式（*）
            // data: data,                      //当不使用上面的后台请求时，使用data来接收数据
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为 true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                    //是否启用排序
            sortOrder: "asc",                   //排序方式
            sidePagination: "client",           //分页方式：client 客户端分页，server 服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 6,                        //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以个人感觉意义不大
            strictSearch: true,                 //启用严格搜索。禁用比较检查。
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置 height 属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                  //是否显示父子表
            showExport: true,                   //是否显示导出
            exportDataType: "basic",            //basic', 'all', 'selected'.
            columns: [{
                checkbox: true     //复选框标题，就是我们看到可以通过复选框选择整行。
            }, {
                field: 'id', title: 'ID'       //我们取json中id的值，并将表头title设置为ID
            }, {
                field: 'username', title: '用户名'         //我们取 json 中 username 的值，并将表头 title 设置为用户名
            },{
                field: 'sex', title: '性别'                //我们取 json 中 sex 的值，并将表头 title 设置为性别
            },{
                field: 'city', title: '城市'               //我们取 json 中 city 的值，并将表头 title 设置为城市
            },{
                field: 'sign', title: '签名'               //我们取 json 中 sign 的值，并将表头 title 设置为签名
            },{
                field: 'classify', title: '分类'           //我们取 json 中 classify 的值，并将表头 title 设置为分类
            },{
                //ormatter:function(value,row,index) 对后台传入数据 进行操作 对数据重新赋值 返回 return 到前台
                // events 触发事件
                field: 'Button',title:"操作",align: 'center',events:operateEvents,formatter:function(value,row,index){
                    var del = '<button type="button" class="btn btn-danger delete">删除</button>'
                    return del;
                }
            }
            ],
            responseHandler: function (res) {
                return res.data      //在加载远程数据之前，处理响应数据格式.
                // 我们取的值在data字段中，所以需要先进行处理，这样才能获取我们想要的结果
            }
        });
</script>
</body>
</html>
```

![](images/2.png)

上面的代码展示通过基本 API 实现基础的功能，示例代码并没有罗列所有的 API。该库还有很多好玩的功能等着大家去发现，正所谓师父领进门修行靠个人～

### 3.2 拆解讲解

下面对关键点进行阐述，为了更方便使用的小伙伴清楚插件的用法。

#### 3.2.1 初始化部分

```
选择需要初始化表格。
$('#tb_departments').bootstrapTable({})
这个就像table的入口一样。
<table id="tb_departments" data-filter-control="true" data-show-columns="true"></table>
```

#### 3.2.2 阅读数据部分

```javascript
columns:[{field: 'Key', title: '文件路径',formatter: function(value,row,index){} }]
```

- field json 中键值对中的 Key
- title 是表格头显示的内容
- formatter 是一个函数类型，当我们对数据内容需要修改时会用它。例：编码转换

#### 3.2.3 事件触发器

```javascript
events:operateEvents
 window.operateEvents = {
        'click .download': function (e,value,row,index) {
            console.log(row);
        }
   }
```

因为很多时候我们需要针对表格进行处理，所以事件触发器是一个不错的选择。比如：它可以记录我们的行数据，可以利用触发器进行定制函数的执行等。

## 四、扩展
介绍几个扩展可以让我们便捷的实现更多的表格功能，而不需要自己造轮子让我们的工作更加高效（也可以进入官网查看扩展的具体使用方法，官方已经收集了大量的扩展）。老规矩直接上代码：

### 4.1 表格导出

```javascript
<script src="js/bootstrap-table-export.js"></script> 
showExport: true,                                           //是否显示导出
exportDataType: basic,								        //导出数据类型，支持：'基本'，'全部'，'选中'
exportTypes:['json', 'xml', 'csv', 'txt', 'sql', 'excel']   //导出类型
```

### 4.2 自动刷新

```javascript
<script src="extensions/auto-refresh/bootstrap-table-auto-refresh.js"></script>
autoRefresh: true, 							    //设置 true 为启用自动刷新插件。这并不意味着启用自动刷新
autoRefreshStatus: true,						//设置 true 为启用自动刷新。这是表加载时状态自动刷新
autoRefreshInterval: 60,						//每次发生自动刷新的时间（以秒为单位）
autoRefreshSilent: true							//设置为静默自动刷新
```

### 4.3 复制行

```javascript
<script src="extensions/copy-rows/bootstrap-table-copy-rows.js"></script>
showCopyRows: true,									//设置 true 为显示复制按钮。此按钮将所选行的内容复制到剪贴板
copyWithHidden: true,								//设置 true 为使用隐藏列进行复制
copyDelimiter: ', ',								//复制时，此分隔符将插入列值之间
copyNewline: '\n'									//复制时，此换行符将插入行值之间
```

## 五、总结

本篇文章只是简单的阐述 Bootstrap-Table 如何使用，正在对表格功能实现而忧愁的小伙伴，可以使用 HelloGitHub 推荐的这款插件。你会发现网页制作表格还可以如此快捷，期待小伙伴挖掘出更加有意思的功能哦。

注：上面 js 部分并没有采用函数形式，建议在使用熟悉之后还是采用函数形式，这样也方便复用及让代码看起来更加规范。

## 六、参考资料

[Bootstrap-Table 项目地址](https://github.com/wenzhixin/bootstrap-table)

[Bootstrap-Table 官方文档](https://bootstrap-table.com/docs/getting-started/introduction/)