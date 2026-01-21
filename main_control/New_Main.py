"""以下函数请勿修改或删减"""
"""要修改请拉到最底下的函数进行修改
"""
from machine import UART, Pin
from dfplayermini import Player

# 设置对齐方式(不要修改！！！！)
left = bytes([0x1B, 0x61, 0x00])
middle = bytes([0x1B, 0x61, 0x01])
right = bytes([0x1B, 0x61, 0x02])

#设置汉字模式(不要修改！！！！)
Set_Chinese_Mode = bytes([0x1C,0x26])
Set_no_Chinese_Mode = bytes([0x1C,0x2E])

#支持unicode模式(不要修改！！！！)
open_support_unicode = bytes([0x1E,0x21,0x43,0x4F,0x44,0x45,0x3D,0x31,0x3B])
close_support_unicode = bytes([0x1E,0x21,0x43,0x4F,0x44,0x45,0x3D,0x30,0x3B])

#设置加粗(不要修改！！！！)
NO_Bold_Mode = bytes([0x1B,0x45,0x00]) #取消加粗
YES_Bold_Mode = bytes([0x1B,0x45,0x01])  #加粗

#设置黑白反显打印(不要修改！！！！)
NO_Black_White_Mode = bytes([0x1D,0x42,0x00]) #取消黑白反显
YES_Black_White_Mode = bytes([0x1D,0x42,0x01]) #黑白反显

#设置下划线打印(不要修改！！！！)
NO_Underline_printing = bytes([0x1B, 0x2D, 0x00]) #取消下划线
Underline_printing_1  = bytes([0x1B, 0x2D, 0x01])
Underline_printing_2  = bytes([0x1B, 0x2D, 0x02])

#设置汉字字符下划线(不要修改！！！！)
NO_Chinese_Underline_printing = bytes([0x1C, 0x2D, 0x00]) #取消下划线
Chinese_Underline_printing_1  = bytes([0x1C, 0x2D, 0x01])
Chinese_Underline_printing_2  = bytes([0x1C, 0x2D, 0x02])

#设置字符大小(不要修改！！！！)
Set_character_size_1x1 = bytes([0x1D,0x21,0x00])
Set_character_size_2x1 = bytes([0x1D,0x21,0x10])
Set_character_size_3x1 = bytes([0x1D,0x21,0x20])
Set_character_size_4x1 = bytes([0x1D,0x21,0x30])
Set_character_size_5x1 = bytes([0x1D,0x21,0x40])
Set_character_size_6x1 = bytes([0x1D,0x21,0x50])
Set_character_size_7x1 = bytes([0x1D,0x21,0x60])
Set_character_size_8x1 = bytes([0x1D,0x21,0x70])
Set_character_size_1x2 = bytes([0x1D,0x21,0x01])
Set_character_size_2x2 = bytes([0x1D,0x21,0x11])
Set_character_size_3x2 = bytes([0x1D,0x21,0x21])
Set_character_size_4x2 = bytes([0x1D,0x21,0x31])
Set_character_size_5x2 = bytes([0x1D,0x21,0x41])
Set_character_size_6x2 = bytes([0x1D,0x21,0x51])
Set_character_size_7x2 = bytes([0x1D,0x21,0x61])
Set_character_size_8x2 = bytes([0x1D,0x21,0x71])

#设置默认打印并走纸距离
Set_feed_print_after = bytes([0x1B, 0x4A, 0x64])

#打印机清空(不要修改！！！！)
paper_init = bytes([0x1B, 0x40])

#设置打印对齐方式(不要修改！！！！)
def setAlignment(align):
    if align == 'l' or align == 'L':
        return left
    elif align == 'm' or align == 'M':
        return middle
    elif align == 'r' or align == 'R':
        return right
    
# 设置汉字模式(不要修改！！！！)
def setChineseMode(chinese_mode):
    if chinese_mode == 'y' or chinese_mode == 'Y':
        return Set_Chinese_Mode
    elif chinese_mode == 'n' or chinese_mode == 'N':
        return Set_no_Chinese_Mode

#设置加粗模式(不要修改！！！！)
def setBold(Bold_mode):
    if Bold_mode == 'n' or Bold_mode == 'N':
        return NO_Bold_Mode
    elif Bold_mode == 'y' or Bold_mode == 'Y':
        return YES_Bold_Mode

#设置黑白反显打印(不要修改！！！！)
def setBlackWhite(blcak_white_mode):
    if blcak_white_mode == 'n' or blcak_white_mode == 'N':
        return NO_Black_White_Mode
    elif blcak_white_mode == 'y' or blcak_white_mode == 'Y':    
        return YES_Black_White_Mode

# 设置下划线打印(不要修改！！！！)
def setUnderlinePrinting(underline_printing):
    if underline_printing == 'n' or underline_printing == 'N':
        return NO_Underline_printing + NO_Chinese_Underline_printing
    elif underline_printing == '1':
        return Underline_printing_1 + Chinese_Underline_printing_1
    elif underline_printing == '2':
        return Underline_printing_2 + Chinese_Underline_printing_2
    
#设置字符大小(不要修改！！！！)
def set_character_size(character_size):
    if character_size == '1x1':
        return Set_character_size_1x1
    elif character_size == '2x1':
        return Set_character_size_2x1
    elif character_size == '3x1':
        return Set_character_size_3x1
    elif character_size == '4x1':
        return Set_character_size_4x1
    elif character_size == '5x1':
        return Set_character_size_5x1
    elif character_size == '6x1':
        return Set_character_size_6x1
    elif character_size == '7x1':
        return Set_character_size_7x1
    elif character_size == '8x1':
        return Set_character_size_8x1
    elif character_size == '1x2':
        return Set_character_size_1x2
    elif character_size == '2x2':
        return Set_character_size_2x2
    elif character_size == '3x2':
        return Set_character_size_3x2
    elif character_size == '4x2':
        return Set_character_size_4x2
    elif character_size == '5x2':
        return Set_character_size_5x2
    elif character_size == '6x2':
        return Set_character_size_6x2
    elif character_size == '7x2':
        return Set_character_size_7x2
    elif character_size == '8x2':
        return Set_character_size_8x2

#设置走纸距离(不要修改！！！！)
def feed_paper(n):
    if 0<= n <= 255:
        return bytes([0x1B,0x4A,n])
    else:
        return Set_feed_print_after

#将UTF-8文本转换为Unicode码点序列(不要修改！！！！)
def utf8_to_unicode(utf8_text):
    if isinstance(utf8_text, bytes):
        try:
            utf8_text = utf8_text.decode('utf-8')
        except:
            return []
    unicode_points = []
    for char in utf8_text:
        unicode_points.append(ord(char))
    return unicode_points
#将Unicode码点转换为字节表示(不要修改！！！！)
def unicode_to_bytes(unicode_points):
    result_bytes = b''
    for code_point in unicode_points:
        if code_point <= 0xFFFF:
            result_bytes += bytes([(code_point >> 8) & 0xFF, code_point & 0xFF])
        else:
            code_point -= 0x10000
            high_surrogate = 0xD800 + (code_point >> 10)
            low_surrogate = 0xDC00 + (code_point & 0x3FF)
            result_bytes += bytes([(high_surrogate >> 8) & 0xFF, high_surrogate & 0xFF])
            result_bytes += bytes([(low_surrogate >> 8) & 0xFF, low_surrogate & 0xFF])  
    return result_bytes

#传入文本字符(不要修改！！！！)
def send_text(text):
    unicode_points = utf8_to_unicode(text)
    return unicode_to_bytes(unicode_points)
   
"""
    参数:
    1、text:文本内容字符串
    2、align: 对齐方式 
    3、chinese_mode:汉字模式
    4、feed_after_paper: 打印后走纸距离 
    5、character_size:字符大小
    6、Bold_mode:加粗模式
    7、black_white_mode:黑白反显打印
    8、underline_printing:下划线打印
"""  
def print_text(text="",align='l',chinese_mode='Y',feed_after_paper=100,character_size='1x1',Bold_mode='N',black_white_mode='N',underline_printing='n'):
    alignment = setAlignment(align)
    chinese_mode_commond = setChineseMode(chinese_mode)
    character_size_commond = set_character_size(character_size)
    bold_mode_commond = setBold(Bold_mode)
    black_white_mode_commond = setBlackWhite(black_white_mode)
    underline_printing_commond = setUnderlinePrinting(underline_printing)
    text_bytes = send_text(text)
    
    uart.write(alignment)
    uart.write(chinese_mode_commond)
    uart.write(character_size_commond)
    uart.write(bold_mode_commond)
    uart.write(black_white_mode_commond)
    uart.write(underline_printing_commond)
    
    uart.write(open_support_unicode)
    uart.write(text_bytes)
    uart.write(b'\n')
    uart.write(close_support_unicode)

    feed_command = feed_paper(feed_after_paper)
    uart.write(feed_command)  
    uart.write(paper_init)
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"""=========请在下面修改========="""
#串口初始化，波特率115200，引脚为PG0,PG1
uart = UART(1, baudrate=115200, tx=Pin(16), rx=Pin(17))
"""打印文本
    参数:
    1、text:文本内容字符串
    2、align: 对齐方式 
        'l'或者'L'=左对齐 <---------- 默认
        'm'或者'M'=居中对齐
        'r'或者'R'=右对齐
    3、chinese_mode:汉字模式(默认开启汉字模式)
        'Y'或者'y'=开启汉字模式 <---------- 默认
        'N'或者'n'=关闭汉字模式
    4、feed_after_paper: 打印后走纸距离 (1-255)(不输入，使用默认值100)
    5、character_size:字符大小(默认1x1)
        1x1 1x2 1x3 1x4 1x5 1x6 1x7 1x8
        2x1 2x2 2x3 2x4 2x5 2x6 2x7 2x8
    6、Bold_mode:加粗模式
        'Y'或者'y'=开启加粗模式 
        'N'或者'n'=关闭加粗模式  <---------- 默认
    7、black_white_mode:黑白反显打印
        'Y'或者'y'=开启黑白反显打印
        'N'或者'n'=关闭黑白反显打印  <---------- 默认
    8、underline_printing:下划线打印
        'N'或者'n'=关闭下划线打印  <---------- 默认
        '1' = 开启下划线打印模式1
        '2' = 开启下划线打印模式2
"""
'''
引脚连接方式：
TBD
'''
from time import localtime
from time import sleep
import time
def get_time_cn(offset_minutes : int) -> str:
    local_time = time.localtime(time.mktime(time.localtime()) + offset_minutes * 60)
    text_time = str(local_time[0]) + '年'
    if local_time[1] < 10: text_time += '0' + str(local_time[1]) + '月'
    else: text_time += str(local_time[1]) + '月'
    if local_time[2] < 10: text_time += '0' + str(local_time[2]) + '日'
    else: text_time += str(local_time[2]) + '日'
    for i in range(3, 6):
        if i != 3:
            text_time += ":"
        if local_time[i] < 10:
            text_time += '0'
        text_time += str(local_time[i])
    return text_time
def get_time_jp(offset_minutes : int) -> str:
    local_time = time.localtime(time.mktime(time.localtime()) + offset_minutes * 60)
    text_time = '令和' + str(local_time[0] - 2019 + 1) + '年'
    if local_time[1] < 10: text_time += '0' + str(local_time[1]) + '月'
    else: text_time += str(local_time[1]) + '月'
    if local_time[2] < 10: text_time += '0' + str(local_time[2]) + '日'
    else: text_time += str(local_time[2]) + '日'
    for i in range(3, 6):
        if i != 3:
            text_time += ":"
        if local_time[i] < 10:
            text_time += '0'
        text_time += str(local_time[i])
    return text_time
def get_time_en(offset_minutes : int) -> str:
    local_time = time.localtime(time.mktime(time.localtime()) + offset_minutes * 60)
    text_time = str(local_time[0])
    for i in range(1, 3):
        if local_time[i] < 10:
            text_time += '-0' + str(local_time[i])
        else:
            text_time += '-' + str(local_time[i])
    text_time += " "
    for i in range(3, 6):
        if i != 3:
            text_time += ":"
        if local_time[i] < 10:
            text_time += '0'
        text_time += str(local_time[i])
    return text_time

    
station_names_cn = ['地牢理工', '牛丼大学', '建桥学院', '麻瓜理工', '哈气大学', '米饭大学', '轮蹲大学', '项模湖', '铜锣湾', '东南山', '上海外滩', '穗织小镇', '奥木染', '新日暮里', '妖怪之山', '狗熊岭', '御茶之水', '魔法森林', '下北泽', '67', 'AMOGUS', '麦当劳']
station_names_jp = ['帝牢大学', '牛丼大学', '建橋学園', 'マグル技術大学', 'ハーファート大学', 'ご飯大学' ,'乱遯大学', '相模湖', '銅鑼湾', '東南山', '上海外灘', '穂織', '奥木染', '新日暮里', '妖怪ノ山', '熊山', '御茶ノ水', '魔法ノ森', '下北沢', '67', 'AMOGUS', 'マクドナルド']
station_names_en = ['Imperil College London', 'Oxbrush Uni.', 'Constbridge Uni.', 'Mugglechussets Inst of Tech', 'Harfart Uni.', '\'Rice\' Uni.', 'Londunk Uni.', 'Sagamiko', 'Tunglo Waan', 'East-South Mt.', 'Shanghai Bund', 'Hoori', 'Okukozome', 'Shin Nippori', 'Youkai Mountain', 'Gouxiong Ling', 'Ochanomizu', 'Forest of Magic', 'Shimokitazawa', '67', 'AMOGUS', 'McDonald\'s']
def delay_print_text(text="",align='l',chinese_mode='Y',feed_after_paper=100,character_size='1x1',Bold_mode='N',black_white_mode='N',underline_printing='n'):
    print_text(text, align, chinese_mode, feed_after_paper, character_size, Bold_mode, black_white_mode, underline_printing)
    sleep(0.7)
    
def print_ticket(station_number: int):
    '''
    dep_time_cn = get_time_cn(30)
    dep_time_jp = get_time_jp(30)
    dep_time_en = get_time_en(30)
    arr_time_cn = get_time_cn(150)
    arr_time_jp = get_time_jp(150)
    arr_time_en = get_time_en(150)
    '''
    dep_time_cn = "哈姆历1145年1月4日19:19"
    arr_time_cn = "哈姆历1145年1月9日08:10"
    dep_time_jp = "ハム1145年1月4日19:19"
    arr_time_jp = "ハム1145年1月9日08:10"
    dep_time_en = "Hamund-1145 01-04 19:19"
    arr_time_en = "Hamund-1145 01-09 08:10"
    delay_print_text("================================", 'l', 'y', 30, '1x1', 'n', 'n', '1')
    delay_print_text("火车票・電車切符", 'm', 'y', 0, '2x2', 'n', 'n', 'n')
    delay_print_text("Train Ticket", 'm', 'y', 30, '2x2', 'n', 'n', 'n')
    delay_print_text("================================", 'l', 'y', 30, '1x1', 'n', 'n', '1')
    delay_print_text("粗糙牛津→", 'l', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text(station_names_cn[station_number], 'r', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text("单程票・当日有效", 'm', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·出发: " + dep_time_cn, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·到达: " + arr_time_cn, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·请妥善保管车票，出站需验票。", 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("================================", 'l', 'y', 30, '1x1', 'n', 'n', '1')
    delay_print_text("粗大牛津→", 'l', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text(station_names_jp[station_number], 'r', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text("片道・本日有効", 'm', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·出発: " + dep_time_jp, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·到着: " + arr_time_jp, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·この切符は駅を出るときに必要ですので安全に保管してください。", 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("================================", 'l', 'y', 30, '1x1', 'n', 'n', '1')
    delay_print_text("Rough Oxford → ", 'l', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text(station_names_en[station_number], 'r', 'y', 0, '2x2', 'n', 'n', '1')
    delay_print_text("One Way・Available for Today", 'm', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·Dep: " + dep_time_en, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·Arr: " + arr_time_en, 'l', 'y', 0, '1x1', 'n', 'n', 'n')
    delay_print_text("·Keep safe as this is required for exiting upon arrival.", 'l', 'y', 100, '1x1', 'n', 'n', 'n')


#----------SETUP----------
#主控模块 LED模块
#12 -> 34
#13 -> 35
#21 <- 21
#22 <- 22
LED_TO_PIN_1 = Pin(12, Pin.OUT) #往LED输出的第一个引脚
LED_TO_PIN_2 = Pin(13, Pin.OUT) #往LED输出的第二个引脚
LED_FROM_PIN_1 = Pin(21, Pin.IN, Pin.PULL_DOWN) #从LED输入的第一个引脚
LED_FROM_PIN_2 = Pin(22, Pin.IN, Pin.PULL_DOWN)#从LED输入的第二个引脚
BUTTON_PIN_1 = Pin(4, Pin.IN, Pin.PULL_DOWN) #"下一个"按钮的引脚
BUTTON_PIN_2 = Pin(5, Pin.IN, Pin.PULL_DOWN) #"确认"按钮的引脚
BUTTON_PIN_3 = Pin(25, Pin.IN, Pin.PULL_DOWN) #"直接抽奖"按钮的引脚
DFPLAYER_MINI_TX_PIN_NUMBER = 26
DFPLAYER_MINI_RX_PIN_NUMBER = 27
#----------DFPlayer Mini----------
music = Player(pin_TX = DFPLAYER_MINI_TX_PIN_NUMBER, pin_RX = DFPLAYER_MINI_RX_PIN_NUMBER)
music.volume(20)


def delay_time_short():
    time.sleep_ms(10)

def play_audio(audio_id: int):
    music.play(audio_id + 1)

cur_pick_param = 0
MAX_PICK_PARAM = 21
round_button_invalid = 0
while True:
   #读按钮引脚
    button_st_1 = BUTTON_PIN_1.value()
    button_st_2 = BUTTON_PIN_2.value()
    button_st_3 = BUTTON_PIN_3.value()
    if round_button_invalid == 0:
        if button_st_3 == 1:
            #直接抽奖按钮被按下, 往两根线写高, 并播放音效
            print("Button 3 (Direct Pick) pressed")
            LED_TO_PIN_1.on()
            LED_TO_PIN_2.on()
            delay_time_short()
            LED_TO_PIN_1.off()
            LED_TO_PIN_2.off()
            play_audio(0) # 播放简单的点击音效
            round_button_invalid = 6
            
        elif button_st_1 == 1:
            #下一个按钮被按下, 往LED的第一根线写高一会,并通知音响播放0
            print("Button 1 pressed")
            LED_TO_PIN_1.on()
            delay_time_short()
            LED_TO_PIN_1.off()
            play_audio(0)
            round_button_invalid = 6 #50*6 = 300ms, 如需变大自行修改, 同时也请修改下面if中的6; 50来源于循环末尾的delay 50ms
            
        elif button_st_2 == 1:
            #下一个按钮被按下，往LED的第二根线写高一会,并通知音响播放1
            print("Button 2 pressed")
            LED_TO_PIN_2.on()
            delay_time_short()
            LED_TO_PIN_2.off()
            play_audio(1)
            round_button_invalid = 6 #50*6 = 300ms, 如需变大自行修改, 同时也请修改上面if中的6; 50来源于循环末尾的delay 50ms
    else:
        round_button_invalid -= 1
        if round_button_invalid < 0: round_button_invalid = 0
    #读LED返回的消息
    led_st_1 = LED_FROM_PIN_1.value()
    led_st_2 = LED_FROM_PIN_2.value()
    #如果返回线2写高则打印且重置cur_pick_param, 此命令优先级高于第二个命令; 此外播放音效3
    if led_st_2 == 1:
        print("LED returned pick confirm, playing audio 3")
        play_audio(3)
        
        
        #请在正式测试中把这个改成print_ticket(cur_pick_param)
        #
        #
        print_ticket(cur_pick_param)
        #print("Test - Print ticket " + str(cur_pick_param)) #并注释掉这一行
        #time.sleep(3) #并注释掉这一行
        
        
        cur_pick_param = 0
    #如果返回线1写高则将cur_pick_param加一, 且播放音效2
    elif led_st_1 == 1:
        print("LED returned pick pass, playing audio 2 and adding pick param by 1")
        cur_pick_param += 1
        play_audio(2)
        if cur_pick_param > MAX_PICK_PARAM: cur_pick_param = 0
    time.sleep_ms(50)
    
    



