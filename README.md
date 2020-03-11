# lovePi
A galgame writen by pygame running on raspberry zero with waveshare lcd hat.


# 首先对树莓派进行配置

下载最全版本的树莓派系统


### 驱动屏幕与开机自启

sudo raspi-config
选择Interfacing Options -> SPI -> Yes 开启SPI接口

fbtft添加新的fb(waveshare 1.44inch LCD HAT 分辨率128*128)
sudo echo options fbtft_device name=adafruit18_green gpios=reset:27,dc:25,cs:8,led:24 speed=40000000 bgr=1 fps=60 custom=1 height=128 width=128 rotate=180 > /etc/modprobe.d/fbtft.conf
重启后 ls /dev 可以看到fb1

安装fbi——配置开机启动图片
sudo apt install fbi

配置开机自启pygame

### pygame开发



# 参考

http://www.waveshare.net/wiki/1.44inch_LCD_HAT
