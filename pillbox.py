#!/usr/bin/python3

import json
import time
import os.path
import RPi.GPIO as GPIO
import subprocess

primary_file='the_data.txt'
#need to modify the ssh location like bobjones@bobjones.com
ssh_location='######:html/'

def main_function():
 GPIO.setmode(GPIO.BCM)
 check_for_file()
 switch=read_data_from_file()
 board_set_up(switch)
 ts=time.time()
 while 2 > 1:
  check_switches(switch)
  time.sleep(2)

def board_set_up(switch):
	for key in switch:
		print("Working on ", switch[key]) 
		GPIO.setup(switch[key]['pinNum'],GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def check_switches(switch):
    print(switch['SatPM'])
    for key in switch:
        switch[key]['current']=GPIO.input(switch[key]['pinNum'])
        print("{} Pin {} has a current value of {} and was {}".format(key,switch[key]['pinNum'],switch[key]['current'],switch[key]['orig']))
        if switch[key]['current'] == switch[key]['orig']:
            pass
        else:
            print("There is a change!")
            switch[key]['orig'] = switch[key]['current']
            switch[key]['time'] = time.asctime(time.localtime(time.time()))
            with open(primary_file,'w') as outfile:
                json.dump(switch,outfile)
            print("Now I'm going to rsync the file...")
            subprocess.run(["rsync","-avzhe","ssh","the_data.txt",ssh_location])

def check_for_file():
        if os.path.exists(primary_file):
                pass
        else:
                switch={
                'MonAM':{'orig':0,'current':0,'pinNum':4,'time':12345678},
                'MonPM':{'orig':0,'current':0,'pinNum':17,'time':12345678},
                'TueAM':{'orig':0,'current':0,'pinNum':18,'time':12345678},
                'TuePM':{'orig':0,'current':0,'pinNum':27,'time':12345678},
                'WedAM':{'orig':0,'current':0,'pinNum':22,'time':12345678},
                'WedPM':{'orig':0,'current':0,'pinNum':23,'time':12345678},
                'ThuAM':{'orig':0,'current':0,'pinNum':24,'time':12345678},
                'ThuPM':{'orig':0,'current':0,'pinNum':25,'time':12345678},
                'FriAM':{'orig':0,'current':0,'pinNum':5,'time':12345678},
                'FriPM':{'orig':0,'current':0,'pinNum':6,'time':12345678},
                'SatAM':{'orig':0,'current':0,'pinNum':12,'time':12345678},
                'SatPM':{'orig':0,'current':0,'pinNum':13,'time':12345678},
                'SunAM':{'orig':0,'current':0,'pinNum':19,'time':12345678},
                'SunPM':{'orig':0,'current':0,'pinNum':26,'time':12345678},
                }

                with open('the_data.txt','w') as outfile:
                        json.dump(switch,outfile)

def read_data_from_file():
        with open(primary_file) as json_file:
                switch=json.load(json_file)
                return switch

main_function()

