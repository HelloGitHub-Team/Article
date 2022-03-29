# Arduino 语言介绍

本文作者 HelloGitHub-Anthony

Arduino 库是使用 C++ 编写的，官方将很多功能包装成了一个个函数，但是对于初学者来讲不需要了解这么多，**只要有一点 C 语言基础即可流畅使用**。**Arduino 库屏蔽了 AVR 单片机的底层细节，让我们即使不了解模数电或者单片机相关知识也能轻松上手**，现在就让我们简单了解以下 Arduino 语言相关内容。

# 1. 启动流程

一般来讲，我们的 C 语言程序都是从一个 `main` 函数开始的，但是在之前的教程中我们发现 IDE 生成的文件中只有 `setup` 和 `loop` 两个函数，那么 Arduino 是如何使用他们的呢？

实际上，真正的 `main` 函数存在于我们的 Arduino 库文件中（位于 Arduino->main.cpp），其定义如下：

```c++
int main(void)
{
    // 进行一些硬件和变量初始化工作
	init();
	initVariant();
#if defined(USBCON)
	USBDevice.attach();
#endif
	// 调用我们编写的 setup() 函数
	setup();
    
	for (;;) {
        // 调用我们编写的 loop() 函数
		loop();
		if (serialEventRun) serialEventRun();
	}
	return 0;
}
```

可以看到我们编写的 `setup` 和 `loop` 两个函数会在 `main` 中进行调用。当然，相关文件是如何组织和编译的这就是 Arduino 工具链所提供的功能了，在这里我们不做深入了解，**在初学阶段我们只关心如何使用**。

# 2. 基础功能

Arduino 为我们提供了多种函数以供使用，具体细节可以查看 Arduino API 手册，其中常用功能如下：

> 不要浪费时间去背诵相关函数，善用 IDE 的智能补全和搜索引擎，使用多了自然可以记住

**常量**

- HIGH | LOW 表示数字IO口的电平，HIGH 表示高电平（1，即输出电压），LOW 表示低电平（0，即不输出电压）。 
- INPUT | OUTPUT 表示数字IO口的方向，INPUT 表示输入（高阻态，即相当于电阻极大可以读取输入电压信号），OUTPUT 表示（输出电压信号）

**结构**

- void setup() 初始化相关引脚和变量
- void loop()  开机后循环执行的函数

**数字 I/O**

- pinMode(pin, mode )数字IO口输入输出模式定义函数，pin表示为0～13， mode表示为INPUT或OUTPUT。 
- digitalWrite(pin, value)  数字IO口输出电平定义函数，pin表示为0～13，value 表示为HIGH或LOW。比如定义HIGH可以驱动LED。 
- int digitalRead(pin)   数字IO口读输入电平函数，pin表示为0～13，value 表示为HIGH或LOW。比如可以读数字传感器。  

**模拟 I/O**  

- int analogRead(pin) 模拟IO口读函数，pin表示为0～5。比如可以读模拟传感器（10位AD，0～5V表示为0～1023）。
- analogWrite(pin, value)  PWM 数字IO口PWM输出函数，Arduino数字IO口 标注了PWM的IO口可使用该函数，pin表示3, 5, 6, 9, 10, 11，value表示为0～255。  

**时间函数**  

- delay(ms)   延时函数（单位ms）。 
- delayMicroseconds(us)  延时函数（单位us）。  

**数学函数** 

- z  min(x, y)  求最小值 
- max(x, y)   求最大值 
- abs(x)    计算绝对值 
- constrain(x, a, b)   约束函数，下限a，上限b，x必须在ab之间才能返回。 
- map(value, fromLow, fromHigh, toLow, toHigh)  约束函数，value必须在fromLow与toLow之间和fromHigh与toHigh之间。 
- pow(base, exponent) 开方函数，base的exponent次方。
- sq(x) 平方 
- sqrt(x) 开根号

# 3. 万物始于点灯

 Arduino 中程序运行时将首先调用 setup() 函数。用于初始化变量、设置针脚的输出 \输入类型、配置串口、引入类库文件等等。每次 Arduino 上电或重启后，setup 函数只运 行一次，例如：

```c++
void setup()
{
  pinMode(LED_BUILTIN, OUTPUT); // 设置内置 LED 端口为输出模式
}
```

之后会执行 loop() 函数。顾名思义,该函数在程序运行过程中不断的循环，直到芯片断电为止：

```C++
void loop()
{
  delay(300); // 等待 300ms
  digitalWrite(LED_BUILTIN, HIGH);// 内置 LED 输出高电平
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);// 内置 LED 输出低电平
}
```

