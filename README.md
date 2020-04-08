# lovePi

lovePi是一个使用pygame开发的恋爱养成游戏模版，支持使用者通过脚本文件自行更改故事。



![demo](assets/demo.jpeg)


# How to run

### 方式 1. pc local

```
git clone https://github.com/xfangfang/lovePi.git
pip3 install pyyaml pygame
python3 main.py PC
```

### 方式 2 raspberry pi zero + LCD HAT

材料：树莓派 zero（其实任何带有40pin GPIO的树莓派均可）、微雪1.3 inch LCD HAT（1.44 inch那个也可以，不过分辨率有些低还没有对应的外壳，不推荐）、PiSugar3D外壳及电池

1. 配置树莓派驱动LCD HAT

   参考微雪的官方说明（地址见参考链接）

   步骤：开启SPI、安装BCM2835、添加fbtft驱动配置（1.44 inch的官方配置中 rotate=180 改为 rotate=90）、添加开机启动图（使用FBI，splashscreen.service已经存放于本项目的根目录使用者根据个人需求自行配置）

2. 拉取仓库和配置依赖

  ```
cd /home/pi
git clone https://github.com/xfangfang/lovePi.git
sudo pip3 install pyyaml
  ```

<!--默认分辨率为 240*240 适配waveshare 1.3 inch LCD HAT，如需更改分辨率请到 var.py 文件修改 HEIGHT 与 WIDTH 到新的值。-->

1. 脚本开机自启

`nano /etc/rc.local`

在exit 0前面一行添加：

```
cd /home/pi/lovePi
sudo /usr/bin/python3 /home/pi/lovePi/main.py PI >> /home/pi/my.log  2>&1 &
```

配置好后，重启即可自动运行



# Keys

微雪LCD HAT 支持 上下左右中，A B C共八个按键

对应于PC键盘为：

```
           ________
  w       |        |      u
a s d     |        |      i
  x       |________|      o

```



# Edit the story

本项目支持用户通过脚本快捷的添加新的故事，提供了基础的显示类，用户也可以基于现有的基础类自行深度定制新的组件。

### 目录结构

1. conf 目录：存放用户的故事，开始游戏时默认调用该目录下的start.yaml中的第一个场景。存放在该目录下的文件可以在脚本中使用，文件 conf/fang-end.yaml 使用时名称为 CONF_FANG_END

2. assets 目录：存放用户的图片素材，图片素材支持 png 与 jpg，存放于该目录下的文件可以在脚本中使用，文件 assets/pic-speek-b-left.png 使用时名称为 PIC_SPEEK_B_LEFT

### 配置文件

```yaml
gameloop:
- type: activity
  tag: start
  activity: Text
  background: BROWN
  texts:
  - content: HELLO WORLD ~
- type: goto
  if: True
  goto_tag: start

```

每个配置文件均由若干个 **activity组件** 或 **goto组件** 组成。

### activity

##### 基础 activity——Text & Choice

基础 activity 有 Text 和 Choice两大类：在Text activity 中，通过在配置文件中加入pics 与 texts，并配置对应的颜色与位置，即可在屏幕中显示对应的文字或图片，点击按键A（pc中为按键U）顺次跳转到下一个activity组件或根据goto规则进行跳转。

Choice activity唯一与Text不同的是，他支持按键A与按键B两种输入，按键输入后顺次跳转到下一个activity组件或根据goto规则进行跳转。不过他修改了当前的游戏状态，将游戏状态修改为 CHOICE_NO 或 CHOICE_YES，后续可以通过goto组件根据这个状态进行跳转，我们在goto组件部分再详细说明。

##### 元素大小与位置

使用 0-1的浮点数来标示屏幕中的位置或元素大小，以左上角为坐标起点(0,0)右下角为坐标最大值(1,1)，横向为X轴纵向为Y轴。

##### 动画

activity还支持animateIn 和 animateOut （入场与离场）时选择动画，目前实现了 activityLinearMove 动画，可以配置每个activity的入场与离场时Activity的线形运动。

##### 自定义组件

用户可继承Text组件实现自定义的Activity，参考 activity/mainActivity.py 中的 class TanTan。或者直接继承 Activity 实现更大灵活性的组件，参考 activity/cat.py 中的 class CatGame

### goto

goto组件支持通过判断游戏状态来进行跳转，

 ```yaml
- type: activity
  activity: balabala
  tag: before
- type: goto
  if: CHOICE_NO
  goto_tag: before
 ```

游戏状态由 activity 进行设定，例如Choice可以设定游戏状态为 CHOICE_YES 或 CHOICE_NO ，自定义组件如何修改游戏状态请参考  activity/mainActivity.py 中的 class Choice。如果游戏状态为指定值，那么游戏就会按照goto组件的标示进行故事的跳转，如果出现 if: True 那么游戏将无条件进行跳转

通过在activity中设定tag，可以使用goto组件跳转到当前文件的指定tag，除了跳转到制定tag，goto还支持其他三种跳转方式。

```yaml
- type: goto
  if: True
  conf: CONF_FANG_BOYFRIEND
  state: 0
- type: goto
  if: CHOICE_NO
  goto: 12
- type: goto
  if: CHOICE_NO
  goto_tag: before
- type: goto
  if: CHOICE_NO
  step: -2
```

第一种方式指定了跳转的故事文件(conf/fang-boyfriend.yaml)，跳转到这个文件的第0个组件；第二种方式跳转到当前故事文件的第12个组件；第四种方式跳转到以当前组件为起点的前两个组件。






# 参考链接

[1.44inch_LCD_HAT](http://www.waveshare.net/wiki/1.44inch_LCD_HAT)

[1.3inch_LCD_HAT](http://www.waveshare.net/wiki/1.3inch_LCD_HAT)

[树莓派修改启动界面](https://www.cnblogs.com/Java-Script/p/11095826.html)

