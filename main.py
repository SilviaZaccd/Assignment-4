import os, sys, io
import M5
from M5 import *
from hardware import I2C, Pin, ADC
from unit import IMUUnit
from time import sleep_ms, ticks_ms
from neopixel import NeoPixel
import m5utils  # 用于数值映射

# 初始化 M5 硬件
M5.begin()

# 配置 I2C 端口
i2c = I2C(0, scl=Pin(21), sda=Pin(25), freq=100000)

# 配置 IMU 传感器
imu = IMUUnit(i2c)

# 配置 NeoPixel LED（30 颗灯珠）
np = NeoPixel(Pin(23), 30)

# 配置 ADC（光传感器）
adc = ADC(Pin(32))
adc.atten(ADC.ATTN_11DB)  # 设置 ADC 灵敏度

# **阈值设定**
TILT_THRESHOLD_X = 500  # **前后倾斜 ±50° 才变红**
TILT_THRESHOLD_Y = 500  # **左右倾斜 ±50° 才变蓝**
LIGHT_THRESHOLD = 70  # **光传感器作弊点阈值**

# 变量初始化
imu_timer, adc_timer = 0, 0
r, g, b = 0, 0, 0
r_final, g_final, b_final = 0, 0, 0

while True:
    # **读取光传感器**
    light_val = adc.read()  # 立即读取光线数据
    lightLevel = int(m5utils.remap(light_val, 0, 4095, 0, 100))
    #print(f'lightLevel||{lightLevel}')  # **发送光照值到 ProtoPie**

    # **🟢 光传感器作弊点：手遮住传感器 → 立即变绿**
    if lightLevel > LIGHT_THRESHOLD:
        r, g, b = 0, 255, 0  # **强制绿色**
        print("cheat")
        #print('color||0,255,0')  # **发送绿色到 ProtoPie**
        
        
        # **立即更新 LED**
        for i in range(30):
            np[i] = (r, g, b)
        np.write()

        sleep_ms(50)  # **确保 LED 立即变色**
        continue  # **跳过 IMU 逻辑，防止颜色被覆盖**

    # **读取 IMU 传感器**
    if ticks_ms() > imu_timer + 100:
        imu_timer = ticks_ms()
        
        imu_val = imu.get_accelerometer()
        imu_x, imu_y = imu_val[0] * 90, imu_val[1] * 90  # **转换为角度**

        imu_x_protopie = int(m5utils.remap(imu_x, -90, 90, 0, 300))
        #print(f'imu_x||{imu_x_protopie}')  # **发送 IMU 数据到 ProtoPie**

        # **🟢 低于 ±50° → 绿色**
        if abs(imu_x) <= TILT_THRESHOLD_X and abs(imu_y) <= TILT_THRESHOLD_Y:
            r_final, g_final, b_final = 0, 255, 0
            print('green')  # **发送绿色到 ProtoPie**

        # **🔴 前后倾斜超 ±50° → 红色**
        elif abs(imu_x) > TILT_THRESHOLD_X:
            r_final, g_final, b_final = 255, 0, 0
            print(imu_x)
            print('red')  # **发送红色到 ProtoPie**

        # **🔵 左右倾斜超 ±50° → 蓝色**
        elif abs(imu_y) > TILT_THRESHOLD_Y:
            r_final, g_final, b_final = 0, 0, 255
            print('blue')  # **发送蓝色到 ProtoPie**

    # **平滑调整 RGB 值，防止颜色跳变**
    if r < r_final:
        r += 1
    elif r > r_final:
        r -= 1
    if g < g_final:
        g += 1
    elif g > g_final:
        g -= 1
    if b < b_final:
        b += 1
    elif b > b_final:
        b -= 1

    # **计算 LED 亮度**
    red = int(r * lightLevel / 100)
    green = int(g * lightLevel / 100)
    blue = int(b * lightLevel / 100)

    # **更新 LED 颜色**
    for i in range(30):
        np[i] = (red, green, blue)
    np.write()  # **刷新 LED**

    sleep_ms(10)
