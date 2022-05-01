# 想学嵌入式？我教你啊

![Arduino Board](E:\Article\contents\Other\Arduino\Arduino introduce\images\cover.png)

本文作者 HelloGitHub-Anthony

HelloGitHub 推出的[《讲解开源项目》](https://github.com/HelloGitHub-Team/Article)系列，本期介绍开源硬件平台 **Arduino** 的中级应用。

> 项目地址：https://github.com/arduino/Arduino



书接上回，我们了解了什么是 Arduino，它能做什么以及它的`Hello World`。接下来我们将更进一步学习 Arduino，通过两个例子做一个有意思的温湿度显示器。1

## 温湿度传感器

本节我们会用到名为 `DHT 11` 的温湿度传感器，`DHT 11` 是一款常用的温湿度数字传感器，其虽然精度不是很高但价格低廉且只用三根线（`VCC` `GND` `DATA`）即可工作，是我们学习使用传感器的不二之选

> DHT 11 数据手册：https://cdn-shop.adafruit.com/datasheets/DHT11-chinese.pdf

在这里，笔者使用的是进行过二次封装的 `DHT 11` 传感器，它长这个样子：

***图片***

> 根据购买的店铺不同，最总实物可能会有所不同，如果您无法分辨每个引脚具体含义一定要先咨询卖家再进行接线以防烧坏传感器

读取 `DHT 11` 数据的方式也非常简单，我们可以根据 ``数据手册`` 中 ``4、串行接口`` 一节提供的信息自行编写数据解析的程序，**但我认为这明显超出了初学者的能力范围**且实现起来也要花上不少功夫，**这时候我们就需要 `Arduino` 的 `Libraries` 功能出场了**。Arduino 官方提供了一个 `Library` 平台搜集了很多开发者提供的开源支持库，灵活使用这些库进行开发可以节省我们大量的时间以及头发。

### DHT 11 支持库

在这里我们选择 `Adafruit` 提供的 `DHT sensor library` 支持库，其还依赖 `Adafruit Unified Sensor` 库，下面我们详细操作：

#### Arduino IDE

##### 安装

点击左侧 Libraries 栏目，在搜索框中输入 `DHT11` 找到 `DHT sensor library by Adafruit`，点击 `INSTALL` 进行安装，然后会提示我们需要安装一些依赖项目：

![2](E:\Article\contents\Other\Arduino\Arudino media\images\2.png)

![3](E:\Article\contents\Other\Arduino\Arudino media\images\3.png)

这里 Arduino IDE 自动提示我们想要使用 `DHT sensor library` 还需要安装 `Adafruit Unified Sensor`，我们直接点击 `Install all` 让它自动安装，成功后可以在输出界面看到这样的提示：

![4](E:\Article\contents\Other\Arduino\Arudino media\images\4.png)

##### 使用

安装好之后我们找到 Arduino IDE 上方选项卡打开 `File->Examples->DHT sensor library->DHTtester`

即可打开 `DHT sensor library` 使用例程，这里我们只需要根据实际情况修改开头几行配置即可直接编译到开发板上进行测试：

![5](E:\Article\contents\Other\Arduino\Arudino media\images\5.png)

上传到开发板后打开我们的 `Serial Monitor`即可看到 Arduino 正在回传温湿度信息：

![image-20220502004533140](E:\Article\contents\Other\Arduino\Arudino media\images\6.png)

#### PlatformIO

##### 安装

相比于 Arduino IDE 能自动帮我们检索依赖库，`Platform IO` 则需要我们分别安装两个库。

首先新建一个工程，然后打开 `Libraries` 页面搜索 `DHT11`，找到 `DHT sensor library by Adafruit`，点进去：

![7](E:\Article\contents\Other\Arduino\Arudino media\images\7.png)

点击 `Add to Project`：

![8](E:\Article\contents\Other\Arduino\Arudino media\images\8.png)

选择好要安装的工程，点击 `Add`

![9](E:\Article\contents\Other\Arduino\Arudino media\images\9.png)

稍等片刻即可成功安装。这时候如果我们尝试进行编译，编译器会提示如下错误：

![image-20220502013219374](E:\Article\contents\Other\Arduino\Arudino media\images\10.png)

说明我们缺少一个依赖项目，按照安装 `DHT sensor library` 的方法，我们搜索 `Adafruit_Sensor` 进行安装，即可正常编译：

![11](E:\Article\contents\Other\Arduino\Arudino media\images\11.png)

##### 使用

打开项目中 `.pio/libdeps/uno/DHT sensor library/examples/DHTtester/DHTtester.ino` 即可看到 `DHT11` 的使用例程，

我们将其内容复制到 `src/main.cpp`

![12](E:\Article\contents\Other\Arduino\Arudino media\images\12.png)

修改一下配置参数，然后连接我们的 Arduino 将程序进行烧录：

![image-20220502013953368](E:\Article\contents\Other\Arduino\Arudino media\images\13.png)

完成后打开我们的`Serial monitor` 查看串口输出：

![image-20220502014142645](E:\Article\contents\Other\Arduino\Arudino media\images\14.png)

可以成功看到的串口输出传感器数据。

#### DH11 库使用简单说明

首先需要初始化一个全局变量，输入 DHT 连接的引脚编号和 DHT 的类型：

```cpp
DHT dht(DHTPIN, DHTTYPE)
```

这里，DHT 有以下几种方法（函数）可供使用：

```cpp
  // 使用方法见上文中的例子
  void begin(uint8_t usec = 55); // 初始化类中的一些参数
  float readTemperature(bool S = false, bool force = false); // 读取温度，不传参数返回 摄氏度，传入一个 true 返回 华摄氏度
  float convertCtoF(float); // 摄氏度转华摄氏度
  float convertFtoC(float); // 华摄氏度转摄氏度
  float computeHeatIndex(bool isFahrenheit = true); // 计算体感温度，参数为 传入的温度是否是华摄氏度，这里温湿度会自动读取
  float computeHeatIndex(float temperature, float percentHumidity, // 功能同上，是面那个函数的具体实现，多了温度和湿度两个参数
                         bool isFahrenheit = true);
  float readHumidity(bool force = false); // 读取湿度
  bool read(bool force = false); // 读取数据（内部使用，一般不主动调用）
```

> 需要注意的是 DHT11 刷新频率并不高，所以在例程中会存在一些延迟函数防止刷新过快出现读取问题。

###　小结

本节我们简单学习了如何安装 Arduino 的支持库以及如何查看支持库提供的例程，进一步了解了 DHT11 库的使用方法，下一节我们将学习如何使用 LCD 屏幕显示字符，组后将两者组合起来实现一个迷你温度显示器。