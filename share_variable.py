# -*- coding: utf-8 -*-
"""
Created on Fri Jan  1 01:04:01 2010

@author: VicWang
"""


'''密码暂存'''
receive_password = ''
'''系统设置量暂存'''
receive_sysdata_str = ''
'''整流设置量暂存'''
receive_recdata_str = ''
'''逆变设置量暂存'''
receive_invdata_str = ''
'''电池设置量暂存'''
receive_batdata_str = ''
'''设置量窗口名称暂存（用于判断哪个窗口打开，然后好组织命令进行数据更新）'''
setting_window_name = ''
'''开关量窗口名称暂存'''
switching_window_name = ''
'''告警量窗口名称暂存'''
warning_window_name = ''
'''开关量暂存'''
receive_switch_data_str = ''
'''告警量暂存'''
receive_warning_data_str = ''
'''protocol接收暂存'''
response_data_str = ''
'''版本暂存'''
Device_VER = ''
'''设备号暂存'''
Device_ADR = ''
'''设备CID2暂存'''
Device_CID2 = ''
'''设备返回值暂存'''
Device_RTN = ''
'''设备DATAFLAG暂存'''
Device_DATAFLAG = ''
'''用户修改设置的值暂存'''
res = ''
'''用户修改系统设置对应的命令暂存'''
Sysdata_0 = ''
'''用户修改整流的值暂存'''
res_rec = ''
'''用户修改整流设置对应的命令暂存'''
Recdata_0 = ''
'''用户修改逆变的值暂存'''
res_inv = ''
'''用户修改逆变设置对应的命令暂存'''
Invdata_0 = ''
'''用户修改电池的值暂存'''
res_bat = ''
'''用户修改电池设置对应的命令暂存'''
Batdata_0 = ''
'''故障点整流数量暂存'''
fault_num_rec = ''
'''故障点整流数量暂存'''
fault_num_inv = ''
'''故障点cfg文件第5列读取整流name值'''
fault_namelist_for_rec = []
'''故障点cfg文件第5列读取逆变name值'''
fault_namelist_for_inv = []
'''故障点cfg文件第0列读取整流'''
fault_row0_list_for_rec = []
'''故障点cfg文件第0列读取逆变'''
fault_row0_list_for_inv = []
'''故障点cfg第2列整流计算标志'''
fault_row2_list_for_rec = []
'''故障点cfg第2列逆变计算标志'''
fault_row2_list_for_inv = []
'''故障点cfg第3列整流'''
fault_row3_list_for_rec = []
'''故障点cfg第3列逆变'''
fault_row3_list_for_inv = []
'''故障点cfg第4列整流'''
fault_row4_list_for_rec = []
'''故障点cfg第4列逆变'''
fault_row4_list_for_inv = []
'''故障点cfg第6列整流'''
fault_row6_list_for_rec = []
'''故障点cfg第6列逆变'''
fault_row6_list_for_inv = []
'''串口状态量暂存'''
serial_status = ''
'''轮询状态量暂存'''
polling_status = '0'
'''数据是否处于解析状态暂存'''
analyse_status = ''
'''历史记录指令导出过程中暂停外部循环状态暂存'''
history_output_status = ''
'''故障点(整流\逆变)请求状态暂存'''
fault_status = ''
'''故障点文件保存标志暂存'''
fault_file_status = ''

