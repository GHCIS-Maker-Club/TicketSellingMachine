#include<bits/stdc++.h>
#include <Wire.h>
#include <Arduino.h>
#include "Data.h"
#include "ESP32-HUB75-VirtualMatrixPanel_T.hpp"
//Dummy function
#define NONE_COMMAND "none"
#define CHANGE_COMMAND "change"
#define CONFIRM_COMMAND "confirm"
#define INIT_MAX_INDEX 1
#define CHECK_MAX_INDEX 21
#define PICK_MAX_INDEX 21 //注意是Index不是大小
#define INIT 0
#define CHECK 1
#define PICK 2

//#define I2C_MASTER 0x20 //主控模块的地址, 需要所有代码中的地址均保持一致
#define I2C_SLAVE 0x03 //本地址
/*
 * Interfaces: "init", "check", "pick"
 */

#define RL1 25
#define GL1 26
#define BL1 27
#define RL2 14
#define GL2 12
#define BL2 13
#define CH_A 23
#define CH_B 19
#define CH_C 5
#define CH_D 18
#define CH_E 32 // assign to any available pin if using two panels or 64x64 panels with 1/32 scan
#define CLK 33
#define LAT 4
#define OE  15
#define LED_IN_PIN_1 34 //TODO
#define LED_IN_PIN_2 35
#define LED_OUT_PIN_1 21
#define LED_OUT_PIN_2 22

#define PANEL_RES_X     64     // Number of pixels wide of each INDIVIDUAL panel module. 
#define PANEL_RES_Y     64     // Number of pixels tall of each INDIVIDUAL panel module.
 
#define VDISP_NUM_ROWS      2 // Number of rows of individual LED panels 
#define VDISP_NUM_COLS      2 // Number of individual LED panels per row
 
#define PANEL_CHAIN_LEN     (VDISP_NUM_ROWS*VDISP_NUM_COLS)  // Don't change
 
 
#define PANEL_CHAIN_TYPE CHAIN_TOP_RIGHT_DOWN
#define PANEL_SCAN_TYPE  FOUR_SCAN_32PX_HIGH
MatrixPanel_I2S_DMA *dma_display = nullptr;

VirtualMatrixPanel_T<PANEL_CHAIN_TYPE>* virtualDisp = nullptr;

int return_random_integer() {
    /*
    // thread_local so each thread gets its own generator (safe in multithreaded code)
    static thread_local std::mt19937 rng{ std::random_device{}() };

    // uniform_int_distribution with inclusive bounds
    static thread_local std::uniform_int_distribution<int> dist{800, 4000};

    return dist(rng);
    */
    randomSeed(millis());
    return random(200) + 300;
}


void setup_display(){
  HUB75_I2S_CFG mxconfig(
    PANEL_RES_X,   
    PANEL_RES_Y,  
    PANEL_CHAIN_LEN
    //, _pins
  );
  mxconfig.i2sspeed = HUB75_I2S_CFG::HZ_10M;
  mxconfig.clkphase = false;
  mxconfig.gpio.r1 = RL1;
  mxconfig.gpio.g1 = GL1;
  mxconfig.gpio.b1 = BL1;
  mxconfig.gpio.r2 = RL2;
  mxconfig.gpio.g2 = GL2;
  mxconfig.gpio.b2 = BL2;
  mxconfig.gpio.a = CH_A;
  mxconfig.gpio.b = CH_B;
  mxconfig.gpio.c = CH_C;
  mxconfig.gpio.d = CH_D;
  mxconfig.gpio.e = CH_E;
  mxconfig.gpio.lat = LAT;
  mxconfig.gpio.oe  = OE;
  mxconfig.gpio.clk = CLK;
  mxconfig.driver = HUB75_I2S_CFG::FM6126A;
  //mxconfig.driver = HUB75_I2S_CFG::FM6126A;
  /**
  * Setup physical DMA LED display output.
  */
  dma_display = new MatrixPanel_I2S_DMA(mxconfig);
  dma_display->begin();
  dma_display->setBrightness8(128); //0-255
  dma_display->clearScreen();
  virtualDisp = new VirtualMatrixPanel_T<PANEL_CHAIN_TYPE>(VDISP_NUM_ROWS, VDISP_NUM_COLS, PANEL_RES_X, PANEL_RES_Y);
  virtualDisp->setDisplay(*dma_display);
}
void mirror_drawPixel(int x, int y, uint16_t color){
  virtualDisp -> drawPixel(128 - x, y, color);
}

void draw_initInterface_DefaultText(){
  uint16_t color = virtualDisp -> color565(255, 0, 0);
  for(auto u: NiHaoLvXingZhe_Red){
    mirror_drawPixel(u / 1000, u % 1000, color);
  }
  //画出绿色部分
  color = virtualDisp -> color565(0, 255, 0);
  for(auto u: NiHaoLvXingZhe_Green){
    mirror_drawPixel(u / 1000, u % 1000, color);
  }
  //画出红底白字部分
  color = virtualDisp -> color565(255, 0, 0);
  for(int x = 32; x<=47; x++) for(int y = 0; y<=127; y++) mirror_drawPixel(x, y, color); //红底
  color = virtualDisp -> color565(255, 255, 255);
  for(auto u: NiHaoLvXingZhe_WhiteOnRed){
    mirror_drawPixel (u/1000, u%1000, color);// 白字
  }
}

void draw_init_0() {
    //画初始界面的第一个图像, 即查看
    draw_initInterface_DefaultText();
    uint16_t color = virtualDisp -> color565(0, 0, 255);
    for(int x = 60; x<=75; x++)for(int y = 0; y<=56; y++) mirror_drawPixel(x, y, color);
    //有什么的字
    color = virtualDisp -> color565(0, 255, 0);
    for(auto u: NiHaoLvXingZhe_Blue){
      mirror_drawPixel (u/1000, u%1000, color);
    }

}
void draw_init_1() {
    //确认
    draw_initInterface_DefaultText();
    uint16_t color = virtualDisp -> color565(0, 0, 255);
    for(int x = 60; x<=75; x++)for(int y = 80; y<=126; y++) mirror_drawPixel(x, y, color);
    //来一发的字
    color = virtualDisp -> color565(0, 255, 0);
    for(auto u: NiHaoLvXingZhe_Blue){
      mirror_drawPixel (u/1000, u%1000, color);
    }
}
void draw_picked_image(int &stationID) {
    uint16_t color = virtualDisp->color565(0, 255, 0);
    for(int x=63; x<=127; x++)for(int y=0; y<=127; y++)mirror_drawPixel(x, y, color);
    color = virtualDisp -> color565(255, 0, 0);
    for(auto u: Print_Red){
        mirror_drawPixel(u%1000, u/1000+63 , color);
    }
    for(auto u: Print_Red){
        mirror_drawPixel(u%100+16, u/1000+63,  color);
        mirror_drawPixel(u%1000+32, u/1000+63,  color);
        mirror_drawPixel(u%1000+48, u/1000+63, color);
        mirror_drawPixel(u%1000+64, u/1000+63, color);
        mirror_drawPixel(u%1000+80, u/1000+63, color);
        mirror_drawPixel(u%1000+96, u/1000+63, color);
        mirror_drawPixel(u%1000+112, u/1000+63, color);
    }
    delay(5000);
}


int cur_interface = INIT; //一开始用户界面为init, 即初始界面
int cur_init_param = 0, cur_check_param = 0, cur_pick_param = 0;

void send_message_to_control(bool is_pass, bool is_change, bool is_confirm){
    String interface_str;//Dummy, 通过I2C把当前interface名称加上" choose"或者"confirm"或者"pass"发送过去, 比如
    switch(cur_interface) {
        case INIT: interface_str = "init"; break;
        case CHECK: interface_str = "chck"; break;
        case PICK: interface_str = "pick"; break;
        default: interface_str = "unkn";
    }
    
    // 根据参数拼接操作类型
    String action;
    if (is_pass) {
        action = "pass";
    } else if (is_change) {
        action = "chse";
    } else if (is_confirm) {
        action = "cfrm";
    } else {
        action = "none";
    }
    String i2c_msg = interface_str + " " + action;
    if(i2c_msg == "pick pass"){
      //把第一根线写高10微秒
      digitalWrite(LED_OUT_PIN_1, HIGH);
      delay(50); //为了让主控模块运行完sleep_ms(10)以及剩下的代码, 不会影响后续因为主控每次执行完毕会delay个50毫秒左右
      digitalWrite(LED_OUT_PIN_1, LOW);
    }
}


void send_confirm_message() {
  Serial.print("Picked ");
  Serial.println(cur_pick_param);
  for(int i=1; i<=cur_pick_param; i++){
    digitalWrite(LED_OUT_PIN_1, HIGH);
    delay(50);
    digitalWrite(LED_OUT_PIN_1, LOW);
    delay(50);
    Serial.print("Writing HIGH AND LOW at ");
    Serial.println(i);
  }
  digitalWrite(LED_OUT_PIN_2, HIGH);
  delay(50);
  digitalWrite(LED_OUT_PIN_2, LOW);
}

void draw_LeftStationList(int &centeredAt){ //省空间
  //CenteredAt应当从0开始.
  //先清屏
  virtualDisp -> fillScreenRGB888 (0, 0, 0);
  int cur_y = -13*(centeredAt - 1);
  int cur_x = 0; //一行应当有4个字符, 用52个index, 0-51
  uint16_t color = virtualDisp -> color565(255, 0, 0);
  //先把选中范围画上颜色块, 应当从y=65画到y=77
  for(int y=65; y<=77; y++){
    for(int x=0; x<=50; x++){
      mirror_drawPixel(y, x, color); //历史遗留问题
    }
  }
  color = virtualDisp -> color565(255, 255, 255);
  for(auto cur_byte : station_list_matrixData){
    if(cur_y >= 128)break;
    //一次解码一个byte, 8个bit
    for(int i=8; i>=1; i--){
      int val = (1 << (i-1));
      if(val & cur_byte)mirror_drawPixel(cur_y, cur_x, color); //历史遗留问题
      //否则不用画
      cur_x ++;
      if(cur_x >= 51){
        cur_x = 0;
        cur_y ++;
      }
    }

    /*
    while(cur_byte > 0){
      if(cur_byte & 1){
        //这一位是1, 可以画
        if(cur_y >= 0 && cur_y < 128) mirror_drawPixel(cur_x, cur_y, color);
      }
      //否则不用画, 然后移位
      cur_byte >>= 1; //移到下一个byte
      cur_x ++; //移到下一个像素
      if(cur_x >= 52){
        cur_x = 0;
        cur_y ++;
      }
    }
    */
  }
  
}

void draw_station_description(int &station_no){
  //应当从x=58开始画到x=122
  //station_no可以从0到21
  uint16_t color = virtualDisp -> color565(150, 255, 150);
  int cur_x = 58, cur_y = 0;
  for(int i=0; i<MAX_INDEX_PER_DESCRIPTION; i++){
    //解码一个byte
    auto cur_byte = station_description[station_no][i];
    for(int i=8; i>=1; i--){
      int val = (1 << (i-1));
      if (val & cur_byte){
        //这一位是1, 可以画
        mirror_drawPixel(cur_y, cur_x, color); //历史遗留问题
      }
      //否则不用画
      cur_x ++;
      if(cur_x >= 123){
        cur_x = 58;
        cur_y ++;
      }
    }
    /*
    while(cur_byte > 0){
      if(cur_byte & 1){
        //这一位是1, 可以画
        mirror_drawPixel(cur_x, cur_y, color);
      }
      //否则不用画, 然后移位
      cur_byte >>= 1; //移到下一个byte
      cur_x ++; //移到下一个像素
      if(cur_x >= 128){
        cur_x = 63;
        cur_y ++;
      }
    }
    */
  }
}

void draw_ticket_interface(int &station_no){
  draw_LeftStationList(station_no);
  uint16_t color = virtualDisp -> color565(150, 255, 150);
  int cur_x = 58, cur_y = 0;
  for(int i=0; i<MAX_INDEX_PER_DESCRIPTION; i++){
    //解码一个byte
    auto cur_byte = station_description[station_no][i];
    for(int i=8; i>=1; i--){
      int val = (1 << (i-1));
      if (val & cur_byte){
        //这一位是1, 可以画
        mirror_drawPixel(cur_y, cur_x, color);
      }
      //否则不用画
      cur_x ++;
      if(cur_x >= 123){
        cur_x = 58;
        cur_y ++;
      }
    }
    /*
     * while(cur_byte > 0){
     *   if(cur_byte & 1){
     *     //这一位是1, 可以画
     *     mirror_drawPixel(cur_x, cur_y, color);
  }
  //否则不用画, 然后移位
  cur_byte >>= 1; //移到下一个byte
  cur_x ++; //移到下一个像素
  if(cur_x >= 128){
    cur_x = 63;
    cur_y ++;
  }
  }
  */
  }
}
int rounds_until_finishing_pick;
void (*draw_init_interfaces[])() = {draw_init_0, draw_init_1};
void determine_for_init_interface(String input) {
    if (input == NONE_COMMAND) {
        draw_init_interfaces[cur_init_param]();
        /*
        String ans = "nothing00";
        for(auto u: ans){
          Wire.write(u);
        }
        return;
        */
    }
    else if (input == CHANGE_COMMAND) {
        //换到下一个按钮
        send_message_to_control(false, true, false);
        cur_init_param ++;
        if (cur_init_param > INIT_MAX_INDEX) cur_init_param = 0;
        //清屏重画
        virtualDisp -> fillScreenRGB888(0, 0, 0);
        draw_init_interfaces[cur_init_param]();
    }
    else {
        //CONFIRM_COMMAND
        //切换到对应状态
        if (cur_init_param == 0) {
            //对应查看状态
            send_message_to_control(false, false, true);
            virtualDisp -> fillScreenRGB888(0, 0, 0);
            //画出第一个界面
            draw_ticket_interface(cur_check_param);
            //跳转到查看状态
            cur_interface = CHECK;
            Serial.println("Switching to check");
            return;
        }
        else {
            //对应来一发状态
            send_message_to_control(false, false, true);
            cur_interface = PICK;
            //设定一个随机量
            rounds_until_finishing_pick = return_random_integer();
            virtualDisp -> fillScreenRGB888(0, 0, 0);
            draw_ticket_interface(cur_pick_param);
            Serial.println("Switching to pick");
            return;
        }
    }
    
}

int delayRound = 0;

void determine_for_check_interface(String input) {
    if (input == NONE_COMMAND) {
        /*
        String ans = "nothing00";
        for(auto u: ans){
          Wire.write(u);
        }
        //draw_ticket_interface(cur_check_param);
        */
        return;
    }
    else if (input == CHANGE_COMMAND) {
        send_message_to_control(false, true, false);
        virtualDisp -> fillScreenRGB888(0, 0, 0);
        cur_check_param ++;
        if (cur_check_param > CHECK_MAX_INDEX) cur_check_param = 0;
        draw_ticket_interface(cur_check_param);
    }
    else {
        //CONFIRM_COMMAND
        //点到了返回按钮
        send_message_to_control(false, false, true);
        cur_interface = INIT;
        Serial.println("Switching to init");
        virtualDisp -> fillScreenRGB888(0, 0, 0);
        return;
    }
}

void determine_for_pick(String input){
    //Serial.println(rounds_until_finishing_pick);
    Serial.println(rounds_until_finishing_pick);
    if (rounds_until_finishing_pick) {
        //抽票, 所以下一个界面, 无论有没有按下"下一个"的按钮
        //Serial.println("Pick pass");
        rounds_until_finishing_pick --;
       // send_message_to_control(true, false, false);
        cur_pick_param ++;
        if (cur_pick_param > PICK_MAX_INDEX) cur_pick_param = 0;
        draw_ticket_interface(cur_pick_param);
    }
    else {
        //到了
        //Serial.println("Pick confirm");
        send_confirm_message(); //打印是主控模块的事情
        //draw_picked_image(cur_pick_param); //播放结算画面
        delayRound = 15000;
        cur_interface = INIT; //返回初始界面
        //virtualDisp -> fillScreenRGB888(0, 0, 0);
        cur_init_param = 0;
        //draw_init_0();
        return;
    }
}
bool st = 0;
String input = "";
int invalid_round = 0;
void Determine_Input(){
  if(invalid_round){
    invalid_round --;
    if(invalid_round < 0)invalid_round = 0;
    input = NONE_COMMAND;
    return;
  }
  int pin1_st = digitalRead(LED_IN_PIN_1);
  int pin2_st = digitalRead(LED_IN_PIN_2);
  //pin1和python文件中的pin1内容一致, 均代表"下一个"按钮; pin2代表"确认"按钮
  if (pin1_st) input = CONFIRM_COMMAND;
  else if(pin2_st) input = CHANGE_COMMAND;
  else input = NONE_COMMAND;
  if(input != NONE_COMMAND) {
    invalid_round = 15;
  }
  //Serial.println(input);
  
}


void Process_Data() {
    if(delayRound){
      delayRound --;
      if(delayRound < 0)delayRound = 0;
      if(delayRound == 0)virtualDisp -> fillScreenRGB888(0, 0, 0);
      return;
    }
    switch (cur_interface) {
        case INIT:
            //Serial.println("Determine for init");
            determine_for_init_interface(input);
            break;
        case CHECK:
            //Serial.println("Determine for check");
            determine_for_check_interface(input);
            break;
        case PICK:
            //Serial.println("Determine for pick");
            determine_for_pick(input);
            break;
    }
}

void setup(){
    pinMode(LED_IN_PIN_1, INPUT_PULLDOWN);
    pinMode(LED_IN_PIN_2, INPUT_PULLDOWN);
    pinMode(LED_OUT_PIN_1, OUTPUT);
    pinMode(LED_OUT_PIN_2, OUTPUT);
    Serial.begin(115200);
    setup_display();
    Serial.println("Set up display");
    //Wire.begin(I2C_SLAVE);
    //Wire.onReceive(I2C_OnReceive);
    //Wire.onRequest(I2C_OnRequest);
    //Serial.println("Set up I2C");
    draw_init_0();
}
void loop(){
    Determine_Input();
    Process_Data();
    delay(1);
}
