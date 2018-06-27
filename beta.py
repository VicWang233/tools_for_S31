# -*- coding: utf-8 -*-
"""
coding by VicWang

This is a temporary script file.
"""
import serial
import tkinter as tk
import func_def as func
from queue import Queue
import share_variable
import time
#from flask import Flask

#

#func.new_threading(flask_test)
#实例化cfg工具
object_cfg_tool = func.cfg_tool('ToolsDebugChs.cfg')
'''
~~~~~~~~~~~~~~~~~~~~定义串口实例~~~~~~~~~~~~~~~~~~~~~
'''
ser = serial.Serial()
'''
~~~~~~~~~~~~~~~~~~~~定义窗口实例~~~~~~~~~~~~~~~~~~~~~
'''
software =tk.Tk() 
software.geometry('700x600')  #窗口大小 
'''
~~~~~~~~~~~~~~~~~~~~定义窗口内部的两个框架,frame_2为主界面左边框架，frame_3为主界面右边框架~~~~~~~~~~~~
'''
frame_2 = tk.Frame(software,width=100,height = 100,borderwidth = 2,relief = 'sunken') #框架2,[Analog2_Data]						
frame_2.grid(row=0,column = 0,rowspan = 2,sticky = 'N')
frame_3 = tk.Frame(software,width=100,height = 100,borderwidth = 2,relief = 'sunken') #框架3，电池等信息[Analog2_Data]					
frame_3.grid(row=0,column = 1,sticky = 'N')
frame_4 = tk.Frame(software,width =100,height = 50,borderwidth = 2,relief = 'sunken')
frame_4.grid(row=1,column = 1,sticky = 'N')


'''
~~~~~~~~~~~~~~~~~~~~调用func下的Common_label_for_setting类完成固定标签显示~~~~~~~~~~~~~~~~~~~~~
'''
common_label_frame2 = func.Common_label_for_setting(frame_2)
common_label_frame3 = func.Common_label_for_setting(frame_3)
common_label_frame2.common_label('ID',0,0,5,'raised')
common_label_frame2.common_label('名称',0,1,20,'raised')
common_label_frame2.common_label('A相',0,2,10,'raised')
common_label_frame2.common_label('B相',0,3,10,'raised')
common_label_frame2.common_label('C相',0,4,10,'raised')
common_label_frame3.common_label('ID',0,0,5,'raised')
common_label_frame3.common_label('名称',0,1,20,'raised')
common_label_frame3.common_label('值',0,2,10,'raised')
'''
~~~~~~~~~~~~~~~~~~~加载图片~~~~~~~~~~~~~~~~~~~~
'''
photo = tk.PhotoImage(file = "5.png")
imgLabel = tk.Label(frame_4,image = photo,relief = 'raised')
imgLabel.grid(row=0,column=0)
'''
~~~~~~~~~~~~线程传递变量定义，使用queue包解决模拟量传递问题。~~~~~~~~~~~~~~~~~~~~~
'''
common_label_queue = Queue(5)
history_queue = Queue()
fault_queue = Queue(9)
'''
~~~~~~~~~~~~~~模拟量刷新线程~~~~~~~~~~~~~~~~~
'''
set_analog_quantity = func.set_analog_quantity(frame_2,frame_3)
quantity_value_timer = func.RepeatTimer(0.4,lambda:set_analog_quantity.reflash_analog_quantity(common_label_queue.get()))
quantity_value_timer.start()
'''
~~~~~~~~~~~~~~设置窗口线程~~~~~~~~~~~~~~~~~~~
'''
'''系统设置窗口线程'''
def Setting_Sysdata_Window():
    setting_sysdata_window = func.Setting_window('SYSData_Num','SYSData_List','sys')
    sysdata_value_timer = func.RepeatTimer(1,lambda:setting_sysdata_window.reflash_data('系统设置--获取数据中','系统设置--已获取数据',share_variable.receive_sysdata_str))
    sysdata_value_timer.start()
    
'''整流设置窗口线程'''
def Setting_Recdata_Window():
    setting_recdata_window = func.Setting_window('RECData_Num','RECData_List','rec')
    recdata_value_timer = func.RepeatTimer(1,lambda:setting_recdata_window.reflash_data('整流设置--获取数据中','整流设置--已获取数据',share_variable.receive_recdata_str))
    recdata_value_timer.start()

'''逆变设置窗口线程'''    
def Setting_Invdata_Window():
    setting_invdata_window = func.Setting_window('INVData_Num','INVData_List','inv')
    invdata_value_timer = func.RepeatTimer(1,lambda:setting_invdata_window.reflash_data('逆变设置--获取数据中','逆变设置--已获取数据',share_variable.receive_invdata_str))
    invdata_value_timer.start()

'''电池设置窗口线程'''
def Setting_Batdata_Window():
    setting_batdata_window = func.Setting_window('BattData_Num','BattData_List','bat')
    batdata_value_timer = func.RepeatTimer(1,lambda:setting_batdata_window.reflash_data('电池设置--获取数据中','电池设置--已获取数据',share_variable.receive_batdata_str))
    batdata_value_timer.start()
'''
~~~~~~~~~~~~~~~开关量窗口线程~~~~~~~~~~~~~~~~
'''
def Switching_Value_Window():         #开关量窗口及数值定义，为方便调用，定义于此。
   '''初始化开关量窗口属性'''
   switching_window = func.Switching_Value_Window('Switching_Value_Num','Switching_Value_list')
   switching_value_timer = func.RepeatTimer(1,switching_window.reflash_switching_value)
   switching_value_timer.start()

'''
~~~~~~~~~~~~~告警量窗口线程~~~~~~~~~~~~~~~~~~
''' 
def Warning_Value_Window():         #告警量窗口及数值定义，为方便调用，定义于此。
    warning_window = func.Warning_Value_Window()
    warning_value_timer = func.RepeatTimer(1,warning_window.reflash_Warning_value)
    warning_value_timer.start()  
'''
~~~~~~~~~~~~~~主界面菜单~~~~~~~~~~~~~~~~~~~~
'''
'''实例化菜单'''
menu_main_button = func.main_menu(software)
'''单个菜单内的下拉列表按钮'''
menulist_file =  ['模拟量数据保存','故障点数据保存','历史记录数据保存','退出']
menulist_config =  ['系统参数设置','整流参数设置','逆变参数设置','电池参数设置','输入密码']
menulist_advanced =  ['修改密码','修改电池曲线','序列号','调试诊断','软件升级']
menulist_help =  ['关于']
menulist_Switching_and_Warning =  ['开关量状态','报警量状态']
menulist_Assist = ['计算CHKSUM','计算FLOAT值']

'''每个按钮绑定的命令'''
commandlist_file = [func.donothing,func.request_for_fault_event,func.request_for_history_event,lambda:func.destory(software)]
commandlist_config = [Setting_Sysdata_Window,Setting_Recdata_Window,Setting_Invdata_Window,Setting_Batdata_Window,func.Setting_the_password]
commandlist_advanced = [func.donothing,func.donothing,func.donothing,func.donothing,func.donothing]
commandlist_help = [func.Easter_egg]
commandlist_Switching_and_Warning = [Switching_Value_Window,Warning_Value_Window]
commandlist_Assist = [func.calc_chksum,func.calc_Single_float]

'''调用func下的set_the_menu完成属性附体'''
menu_main_button.set_the_menu('文件',menulist_file,commandlist_file)
menu_main_button.set_the_menu('设置',menulist_config,commandlist_config)
menu_main_button.set_the_menu('高级操作',menulist_advanced,commandlist_advanced)
menu_main_button.set_the_menu('帮助',menulist_help,commandlist_help)
menu_main_button.set_the_menu('开关与报警',menulist_Switching_and_Warning,commandlist_Switching_and_Warning)
menu_main_button.set_the_menu('辅助功能',menulist_Assist,commandlist_Assist)

'''
~~~~~~~~~~~~~~~~~主界面名称及ID~~~~~~~~~~~~~~~~
'''

#设定Analog1_data面板ID名称值等
for i in range(0,int(object_cfg_tool.Pick_Option_In_Section('Analog1_Num',0,0))):
    name_id = object_cfg_tool.Pick_Option_In_Section('Analog1_Data',i,0)
    common_label_frame2.common_label(name_id,i+1,0,5,'groove')  #ID   
    name_left = object_cfg_tool.Pick_Option_In_Section('Analog1_Data',i,1)
    common_label_frame2.common_label(name_left,i+1,1,20,'groove')  #名称    
#设定Analog2_data面板ID名称值等
for i in range(0,int(object_cfg_tool.Pick_Option_In_Section('Analog2_Num',0,0))):
    name_right = object_cfg_tool.Pick_Option_In_Section('Analog2_Data',i,0)
    common_label_frame3.common_label(name_right,i+1,0,5,'groove')  #ID
    name_right = object_cfg_tool.Pick_Option_In_Section('Analog2_Data',i,1)
    common_label_frame3.common_label(name_right,i+1,1,20,'groove')  #名称
    
#B、C两相数据设定为'\'
for i in range(0,int(object_cfg_tool.Pick_Option_In_Section('Analog1_Num',0,0))):
    if i == 8 or i == 16 or i == 20:
        common_label_frame2.common_label('',i+1,3,10,'groove') 
        common_label_frame2.common_label('',i+1,4,10,'groove') 

    elif i>=2 and i!=21 and i!=22 and i!=23:
        common_label_frame2.common_label('\\',i+1,3,10,'groove') 
        common_label_frame2.common_label('\\',i+1,4,10,'groove')

'''
~~~~~~~~~后台串口通信收发数据线程(所谓的主线程)~~~~~~~~~
'''
def send_massage():
    send_to_massage = func.send_message(ser,software)
    status = send_to_massage.judge_ser_status(frame_2,frame_3)
    if status:  
        try:
            if ser.inWaiting() == 0:
                '''assemble_commmand_and_send：负责组成完成命令组织并循环发送，循环顺序写死。'''
                send_to_massage.assemble_commmand_and_send()
                '''如果串口有等待数据,使用read_the_response_data_str进行处理,参数common_label_queue用于传递模拟量队列'''
            while ser.inWaiting()>0:                 #串口等待数据的数量                 
                if share_variable.polling_status == '3':   #读历史数据单独搞
                    send_to_massage.read_history_event(history_queue)                 
                elif share_variable.polling_status == '4':   #故障点数据单独
                    time.sleep(0.4)  #与主循环(0.4S保持一致，若快了则会出现读取两次数据的情况)
                    send_to_massage.read_fault_event(fault_queue)                    
                else:                    
                    send_to_massage.read_the_response_data_str(common_label_queue) 
                #if share_variable.history_output_status == '1':
                    #send_massage_timer.start()
                '''处理完串口等待数据后，再次确认串口等待数据是否清空，如已清空，把返回值临时接收量response_data_str清空'''
            #if ser.inWaiting() == 0:      #串口中待处理的数据为0后，把响应字符串清0
            #end = time.clock()
            #print("执行时间:",end-start)
            share_variable.response_data_str = '' 
            '''监听系统异常(OSError)下的SerialException异常，如触发异常，则界面数据全部清零，并改变标签状态。'''
        except(OSError,serial.SerialException):
            ser.close()
            software.title('串口助手-通讯异常')
            func.set_analog_quantity_to_zero(frame_2,frame_3)
            send_to_massage.clear_the_value('12345') #系统设置清零          
'''
~~~~~~~~~~~~~~~~开启线程循环~~~~~~~~~~~~
'''
send_massage_timer = func.RepeatTimer(0.4,send_massage)
send_massage_timer.start()
'''
~~~~~~~~~~~~~~关闭窗口时触发清除所有后台线程指令~~~~~~~~~~~~
'''
software.protocol('WM_DELETE_WINDOW',lambda:func.destory(software))
'''
~~~~~~~~~~~~~~主界面消息循环~~~~~~~~~~~~
'''
if __name__ == '__main__':
    software.mainloop()
    






