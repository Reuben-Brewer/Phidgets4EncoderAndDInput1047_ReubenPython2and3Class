# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 03/13/2022

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

from LowPassFilter_ReubenPython2and3Class import *

import os, sys, platform
import time, datetime
import math
import collections
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback

###############
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###############

###############
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###############

###############
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
############### #"sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###############
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###############

###########################################################
###########################################################
#To install Phidget22, enter folder "Phidget22Python_1.0.0.20190107\Phidget22Python" and type "python setup.py install"
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.DigitalInput import *
###########################################################
###########################################################

class Phidgets4EncoderAndDInput1047_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__ starting. ####################")

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = -1
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################

        #########################################################
        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"
        #########################################################

        self.EncodersList_PhidgetsEncoderObjects = list()

        self.EncodersList_AttachedAndOpenFlag = [0.0] * 4
        self.EncodersList_NeedsToBeHomedFlag = [0] * 4
        self.EncodersList_UpdateDeltaTseconds = [0.0] * 4
        self.EncodersList_UpdateFrequencyHz = [0.0] * 4
        self.EncodersList_ErrorCallbackFiredFlag = [0.0] * 4

        self.EncodersList_Position_EncoderTicks = [0.0] * 4
        self.EncodersList_Position_Rev = [0.0] * 4
        self.EncodersList_Position_Degrees = [0.0] * 4

        self.EncodersList_IndexPosition_EncoderTicks = [-11111.0] * 4
        self.EncodersList_IndexPosition_Rev = [-11111.0] * 4
        self.EncodersList_IndexPosition_Degrees = [-11111.0] * 4

        self.EncodersList_HomingOffsetPosition_EncoderTicks = [0.0] * 4

        self.EncodersList_Speed_EncoderTicksPerSecond_Raw = [-11111.0] * 4
        self.EncodersList_Speed_RPM_Raw = [-11111.0] * 4
        self.EncodersList_Speed_RPS_Raw = [-11111.0] * 4
        self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject = list()
        self.EncodersList_Speed_EncoderTicksPerSecond_Filtered = [-11111.0] * 4
        self.EncodersList_Speed_RPM_Filtered = [-11111.0] * 4
        self.EncodersList_Speed_RPS_Filtered = [-11111.0] * 4

        self.DigitalInputsList_PhidgetsDIobjects = list()

        self.DigitalInputsList_AttachedAndOpenFlag = [0.0] * 4
        self.DigitalInputsList_ErrorCallbackFiredFlag = [0.0] * 4
        self.DigitalInputsList_State = [-1] * 4

        self.MostRecentDataDict = dict([("EncodersList_Position_EncoderTicks", self.EncodersList_Position_EncoderTicks),
                                             ("EncodersList_Position_Rev", self.EncodersList_Position_Rev),
                                             ("EncodersList_Position_Degrees", self.EncodersList_Position_Degrees),
                                             ("EncodersList_IndexPosition_EncoderTicks", self.EncodersList_IndexPosition_EncoderTicks),
                                             ("EncodersList_IndexPosition_Rev", self.EncodersList_IndexPosition_Rev),
                                             ("EncodersList_IndexPosition_Degrees", self.EncodersList_IndexPosition_Degrees),
                                             ("EncodersList_Speed_EncoderTicksPerSecond_Raw", self.EncodersList_Speed_EncoderTicksPerSecond_Raw),
                                             ("EncodersList_Speed_RPM_Raw", self.EncodersList_Speed_RPM_Raw),
                                             ("EncodersList_Speed_RPS_Raw", self.EncodersList_Speed_RPS_Raw),
                                             ("EncodersList_Speed_EncoderTicksPerSecond_Filtered", self.EncodersList_Speed_EncoderTicksPerSecond_Filtered),
                                             ("EncodersList_Speed_RPM_Filtered", self.EncodersList_Speed_RPM_Filtered),
                                             ("EncodersList_Speed_RPS_Filtered", self.EncodersList_Speed_RPS_Filtered),
                                             ("EncodersList_ErrorCallbackFiredFlag", self.EncodersList_ErrorCallbackFiredFlag),
                                             ("DigitalInputsList_State", self.DigitalInputsList_State),
                                             ("DigitalInputsList_ErrorCallbackFiredFlag", self.DigitalInputsList_ErrorCallbackFiredFlag),
                                             ("Time", self.CurrentTime_CalculatedFromMainThread)])

        ##########################################
        ##########################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("The OS platform is: " + self.my_platform)
        ##########################################
        ##########################################

        ##########################################
        ##########################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            ##########################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))
            ##########################################

            ##########################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
                self.RootIsOwnedExternallyFlag = 1
            else:
                self.root = None
                self.RootIsOwnedExternallyFlag = 0

            print("RootIsOwnedExternallyFlag = " + str(self.RootIsOwnedExternallyFlag))
            ##########################################

            ##########################################
            if "GUI_RootAfterCallbackInterval_Milliseconds" in self.GUIparametersDict:
                self.GUI_RootAfterCallbackInterval_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_RootAfterCallbackInterval_Milliseconds", self.GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds"], 0.0, 1000.0))
            else:
                self.GUI_RootAfterCallbackInterval_Milliseconds = 30

            print("GUI_RootAfterCallbackInterval_Milliseconds = " + str(self.GUI_RootAfterCallbackInterval_Milliseconds))
            ##########################################

            ##########################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            ##########################################

            ##########################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            ##########################################

            ##########################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("NumberOfPrintLines = " + str(self.NumberOfPrintLines))
            ##########################################

            ##########################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            ##########################################

            ##########################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("GUI_ROW = " + str(self.GUI_ROW))
            ##########################################

            ##########################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("GUI_COLUMN = " + str(self.GUI_COLUMN))
            ##########################################

            ##########################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("GUI_PADX = " + str(self.GUI_PADX))
            ##########################################

            ##########################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("GUI_PADY = " + str(self.GUI_PADY))
            ##########################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 0.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 0

            print("GUI_ROWSPAN = " + str(self.GUI_ROWSPAN))
            ##########################################

            ##########################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 0

            print("GUI_COLUMNSPAN = " + str(self.GUI_COLUMNSPAN))
            ##########################################

            ##########################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("GUI_STICKY = " + str(self.GUI_STICKY))
            ##########################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        print("GUIparametersDict = " + str(self.GUIparametersDict))
        ##########################################
        ##########################################

        ##########################################
        if "DesiredSerialNumber" in setup_dict:
            try:
                self.DesiredSerialNumber = int(setup_dict["DesiredSerialNumber"])
            except:
                print("ERROR: DesiredSerialNumber invalid.")
        else:
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__ ERROR: Must initialize object with 'DesiredSerialNumber' argument.")
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
            return
        
        print("DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        ##########################################

        ##########################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""
        ##########################################

        ##########################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        ##########################################

        ##########################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        ##########################################

        ##########################################
        if "EncoderUpdateDeltaT_ms" in setup_dict:
            self.EncoderUpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncoderUpdateDeltaT_ms", setup_dict["EncoderUpdateDeltaT_ms"], 8.0, 60000.0))
        else:
            self.EncoderUpdateDeltaT_ms = 8

        print("EncoderUpdateDeltaT_ms: " + str(self.EncoderUpdateDeltaT_ms))
        ##########################################

        ##########################################
        if "EncodersList_ChannelsBeingWatchedList" in setup_dict:
            EncodersList_ChannelsBeingWatchedList_TEMP = setup_dict["EncodersList_ChannelsBeingWatchedList"]
            if self.IsInputList(EncodersList_ChannelsBeingWatchedList_TEMP) == 1 and len(EncodersList_ChannelsBeingWatchedList_TEMP) == 4:
                self.EncodersList_ChannelsBeingWatchedList = list()
                for EncoderChannel, EnabledState_TEMP in enumerate(EncodersList_ChannelsBeingWatchedList_TEMP):
                    EnabledState = self.PassThrough0and1values_ExitProgramOtherwise("EncodersList_ChannelsBeingWatchedList, EncoderChannel " + str(EncoderChannel), EnabledState_TEMP)
                    self.EncodersList_ChannelsBeingWatchedList.append(EnabledState)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: ERROR, 'EncodersList_ChannelsBeingWatchedList' must be a length of length 4 with values of 0 or 1.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return
        else:
            self.EncodersList_ChannelsBeingWatchedList = [1, 1, 1, 1]

        print("EncodersList_ChannelsBeingWatchedList: " + str(self.EncodersList_ChannelsBeingWatchedList))
        ##########################################

        ##########################################
        if "EncodersList_CPR" in setup_dict:
            EncodersList_CPR_TEMP = setup_dict["EncodersList_CPR"]
            if self.IsInputList(EncodersList_CPR_TEMP) == 1 and len(EncodersList_CPR_TEMP) == 4:
                self.EncodersList_CPR = list()
                for EncoderChannel, CPR_TEMP in enumerate(EncodersList_CPR_TEMP):
                    CPR = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_CPR, EncoderChannel " + str(EncoderChannel), CPR_TEMP, 0, 250000)
                    self.EncodersList_CPR.append(CPR)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: ERROR, 'EncodersList_CPR' must be a length of length 4 with values of 0 or 1.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return
        else:
            self.EncodersList_CPR = [1, 1, 1, 1]

        print("EncodersList_CPR: " + str(self.EncodersList_CPR))
        ##########################################

        ##########################################
        if "EncodersList_SpeedExponentialFilterLambda" in setup_dict:
            EncodersList_SpeedExponentialFilterLambda_TEMP = setup_dict["EncodersList_SpeedExponentialFilterLambda"]
            if self.IsInputList(EncodersList_SpeedExponentialFilterLambda_TEMP) == 1 and len(EncodersList_SpeedExponentialFilterLambda_TEMP) == 4:
                self.EncodersList_SpeedExponentialFilterLambda = list()
                for EncoderChannel, SpeedExponentialFilterLambda_TEMP in enumerate(EncodersList_SpeedExponentialFilterLambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_SpeedExponentialFilterLambda, EncoderChannel " + str(EncoderChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.EncodersList_SpeedExponentialFilterLambda.append(SpeedExponentialFilterLambda)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: ERROR, 'EncodersList_SpeedExponentialFilterLambda' must be a length of length 4 with values of 0 or 1.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return
        else:
            self.EncodersList_SpeedExponentialFilterLambda = [1.0, 1.0, 1.0, 1.0]

        print("EncodersList_SpeedExponentialFilterLambda: " + str(self.EncodersList_SpeedExponentialFilterLambda))
        ##########################################

        ##########################################
        if "DigitalInputsList_ChannelsBeingWatchedList" in setup_dict:
            DigitalInputsList_ChannelsBeingWatchedList_TEMP = setup_dict["DigitalInputsList_ChannelsBeingWatchedList"]
            if self.IsInputList(DigitalInputsList_ChannelsBeingWatchedList_TEMP) == 1 and len(DigitalInputsList_ChannelsBeingWatchedList_TEMP) == 4:
                self.DigitalInputsList_ChannelsBeingWatchedList = list()
                for DigitalInputChannel, EnabledState_TEMP in enumerate(DigitalInputsList_ChannelsBeingWatchedList_TEMP):
                    EnabledState = self.PassThrough0and1values_ExitProgramOtherwise("DigitalInputsList_ChannelsBeingWatchedList, DigitalInputChannel " + str(DigitalInputChannel), EnabledState_TEMP)
                    self.DigitalInputsList_ChannelsBeingWatchedList.append(EnabledState)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: ERROR, 'DigitalInputsList_ChannelsBeingWatchedList' must be a length of length 4 with values of 0 or 1.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return
        else:
            self.DigitalInputsList_ChannelsBeingWatchedList = [1, 1, 1, 1]

        print("DigitalInputsList_ChannelsBeingWatchedList: " + str(self.DigitalInputsList_ChannelsBeingWatchedList))
        ##########################################

       ##########################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        ##########################################

        #########################################################
        try:
            
            for EncoderChannel in range(0, 4):
                self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                                                ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                ("ExponentialSmoothingFilterLambda", self.EncodersList_SpeedExponentialFilterLambda[EncoderChannel])])))
                time.sleep(0.1)
                LOWPASSFILTER_OPEN_FLAG = self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject[EncoderChannel].OBJECT_CREATED_SUCCESSFULLY_FLAG
    
                if LOWPASSFILTER_OPEN_FLAG != 1:
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to open LowPassFilter_ReubenPython2and3ClassObject.")
                    self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                    return

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
        #########################################################

        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            if self.EncodersList_ChannelsBeingWatchedList[0] == 1:
                self.Encoder0object = Encoder()
                self.EncodersList_PhidgetsEncoderObjects.append(self.Encoder0object)
                self.Encoder0object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.Encoder0object.setChannel(0)
                self.Encoder0object.setOnPositionChangeHandler(self.Encoder0onPositionChangeCallback)
                self.Encoder0object.setOnAttachHandler(self.Encoder0onAttachCallback)
                self.Encoder0object.setOnDetachHandler(self.Encoder0onDetachCallback)
                self.Encoder0object.setOnErrorHandler(self.Encoder0onErrorCallback)
                self.Encoder0object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            else:
                self.EncodersList_PhidgetsEncoderObjects.append("NULL")
            #########################################################

            #########################################################
            if self.EncodersList_ChannelsBeingWatchedList[1] == 1:
                self.Encoder1object = Encoder()
                self.EncodersList_PhidgetsEncoderObjects.append(self.Encoder1object)
                self.Encoder1object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.Encoder1object.setChannel(1)
                self.Encoder1object.setOnPositionChangeHandler(self.Encoder1onPositionChangeCallback)
                self.Encoder1object.setOnAttachHandler(self.Encoder1onAttachCallback)
                self.Encoder1object.setOnDetachHandler(self.Encoder1onDetachCallback)
                self.Encoder1object.setOnErrorHandler(self.Encoder1onErrorCallback)
                self.Encoder1object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            else:
                self.EncodersList_PhidgetsEncoderObjects.append("NULL")
            #########################################################
            
            #########################################################
            if self.EncodersList_ChannelsBeingWatchedList[2] == 1:
                self.Encoder2object = Encoder()
                self.EncodersList_PhidgetsEncoderObjects.append(self.Encoder2object)
                self.Encoder2object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.Encoder2object.setChannel(2)
                self.Encoder2object.setOnPositionChangeHandler(self.Encoder2onPositionChangeCallback)
                self.Encoder2object.setOnAttachHandler(self.Encoder2onAttachCallback)
                self.Encoder2object.setOnDetachHandler(self.Encoder2onDetachCallback)
                self.Encoder2object.setOnErrorHandler(self.Encoder2onErrorCallback)
                self.Encoder2object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            else:
                self.EncodersList_PhidgetsEncoderObjects.append("NULL")
            #########################################################
            
            #########################################################
            if self.EncodersList_ChannelsBeingWatchedList[3] == 1:
                self.Encoder3object = Encoder()
                self.EncodersList_PhidgetsEncoderObjects.append(self.Encoder3object)
                self.Encoder3object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.Encoder3object.setChannel(3)
                self.Encoder3object.setOnPositionChangeHandler(self.Encoder3onPositionChangeCallback)
                self.Encoder3object.setOnAttachHandler(self.Encoder3onAttachCallback)
                self.Encoder3object.setOnDetachHandler(self.Encoder3onDetachCallback)
                self.Encoder3object.setOnErrorHandler(self.Encoder3onErrorCallback)
                self.Encoder3object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            else:
                self.EncodersList_PhidgetsEncoderObjects.append("NULL")
            #########################################################

            #########################################################
            if self.DigitalInputsList_ChannelsBeingWatchedList[0] == 1:
                self.DigitalInput0object = DigitalInput()
                self.DigitalInputsList_PhidgetsDIobjects.append(self.DigitalInput0object)
                self.DigitalInput0object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.DigitalInput0object.setChannel(0)
                self.DigitalInput0object.setOnStateChangeHandler(self.DigitalInput0onStateChangeCallback)
                self.DigitalInput0object.setOnAttachHandler(self.DigitalInput0onAttachCallback)
                self.DigitalInput0object.setOnDetachHandler(self.DigitalInput0onDetachCallback)
                self.DigitalInput0object.setOnErrorHandler(self.DigitalInput0onErrorCallback)
                self.DigitalInput0object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            else:
                self.DigitalInputsList_PhidgetsDIobjects.append("NULL")
            #########################################################

            #########################################################
            if self.DigitalInputsList_ChannelsBeingWatchedList[1] == 1:
                self.DigitalInput1object = DigitalInput()
                self.DigitalInputsList_PhidgetsDIobjects.append(self.DigitalInput1object)
                self.DigitalInput1object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.DigitalInput1object.setChannel(1)
                self.DigitalInput1object.setOnStateChangeHandler(self.DigitalInput1onStateChangeCallback)
                self.DigitalInput1object.setOnAttachHandler(self.DigitalInput1onAttachCallback)
                self.DigitalInput1object.setOnDetachHandler(self.DigitalInput1onDetachCallback)
                self.DigitalInput1object.setOnErrorHandler(self.DigitalInput1onErrorCallback)
                self.DigitalInput1object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            else:
                self.DigitalInputsList_PhidgetsDIobjects.append("NULL")
            #########################################################
            
            #########################################################
            if self.DigitalInputsList_ChannelsBeingWatchedList[2] == 1:
                self.DigitalInput2object = DigitalInput()
                self.DigitalInputsList_PhidgetsDIobjects.append(self.DigitalInput2object)
                self.DigitalInput2object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.DigitalInput2object.setChannel(2)
                self.DigitalInput2object.setOnStateChangeHandler(self.DigitalInput2onStateChangeCallback)
                self.DigitalInput2object.setOnAttachHandler(self.DigitalInput2onAttachCallback)
                self.DigitalInput2object.setOnDetachHandler(self.DigitalInput2onDetachCallback)
                self.DigitalInput2object.setOnErrorHandler(self.DigitalInput2onErrorCallback)
                self.DigitalInput2object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            else:
                self.DigitalInputsList_PhidgetsDIobjects.append("NULL")
            #########################################################
            
            #########################################################
            if self.DigitalInputsList_ChannelsBeingWatchedList[3] == 1:
                self.DigitalInput3object = DigitalInput()
                self.DigitalInputsList_PhidgetsDIobjects.append(self.DigitalInput3object)
                self.DigitalInput3object.setDeviceSerialNumber(self.DesiredSerialNumber)
                self.DigitalInput3object.setChannel(3)
                self.DigitalInput3object.setOnStateChangeHandler(self.DigitalInput3onStateChangeCallback)
                self.DigitalInput3object.setOnAttachHandler(self.DigitalInput3onAttachCallback)
                self.DigitalInput3object.setOnDetachHandler(self.DigitalInput3onDetachCallback)
                self.DigitalInput3object.setOnErrorHandler(self.DigitalInput3onErrorCallback)
                self.DigitalInput3object.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            else:
                self.DigitalInputsList_PhidgetsDIobjects.append("NULL")
            #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\Phidgets4EncoderAndDInput1047_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.Encoder0object.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceSerialNumber = self.Encoder0object.getDeviceSerialNumber()
                print("DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.Encoder0object.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.Encoder0object.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.Encoder0object.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                print("The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                input("Press any key (and enter) to exit.")
                sys.exit()
            #########################################################

            ##########################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            ##########################################

            ##########################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            ##########################################

            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        dummy_var = 0
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber):

        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be 0 or 1 (value was " +
                          str(InputNumber_ConvertedToFloat) +
                          "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue):
        try:
            InputNumber_ConvertedToFloat = float(InputNumber)
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()

        try:
            if InputNumber_ConvertedToFloat >= RangeMinValue and InputNumber_ConvertedToFloat <= RangeMaxValue:
                return InputNumber_ConvertedToFloat
            else:
                input("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                          InputNameString +
                          "' must be in the range [" +
                          str(RangeMinValue) +
                          ", " +
                          str(RangeMaxValue) +
                          "] (value was " +
                          str(InputNumber_ConvertedToFloat) + "). Press any key (and enter) to exit.")

                sys.exit()
        except:
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            input("Press any key to continue")
            sys.exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonAttachCallback(self, EncoderChannel):

        try:
            ##############################
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setDataInterval(self.EncoderUpdateDeltaT_ms)
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setPositionChangeTrigger(0) #Setting the trigger to 0 makes the onPositionChange callback fire every self.EncoderUpdateDeltaT_ms
            self.MyPrint_WithoutLogFile("EncoderGENERALonAttachCallback event, EncoderChannel " + str(EncoderChannel) + " currently has DataInterval: " + str(self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getDataInterval()))
            ##############################

            self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ EncoderGENERALonAttachCallback event for EncoderChannel " + str(EncoderChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 0
            self.MyPrint_WithoutLogFile("EncoderGENERALonAttachCallback event for EncoderChannel " + str(EncoderChannel) + ", ERROR: Failed to attach Encoder0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonDetachCallback(self, EncoderChannel):

        self.EncodersList_AttachedAndOpenFlag[EncoderChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ EncoderGENERALonDetachCallback event for EncoderChannel " + str(EncoderChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("EncoderGENERALonDetachCallback event for Encoder Channel " + str(EncoderChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def EncoderGENERALonPositionChangeCallback(self, EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered):

        ################################
        self.EncodersList_Position_EncoderTicks[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel] + positionChange
        self.EncodersList_Position_Rev[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
        self.EncodersList_Position_Degrees[EncoderChannel] = 360.0*self.EncodersList_Position_Rev[EncoderChannel]
        ################################

        ################################
        if indexTriggered == 1:
            self.EncodersList_IndexPosition_EncoderTicks[EncoderChannel] = self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].getIndexPosition()
            self.EncodersList_IndexPosition_Rev[EncoderChannel] = self.EncodersList_IndexPosition_EncoderTicks[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_IndexPosition_Degrees[EncoderChannel] = 360.0 * self.EncodersList_IndexPosition_Rev[EncoderChannel]
        ################################

        ################################
        if timeChangeInMilliseconds > 0.0:
            self.EncodersList_UpdateDeltaTseconds[EncoderChannel] = timeChangeInMilliseconds/1000.0
            self.EncodersList_UpdateFrequencyHz[EncoderChannel] = 1.0/self.EncodersList_UpdateDeltaTseconds[EncoderChannel]
            self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel] = positionChange/self.EncodersList_UpdateDeltaTseconds[EncoderChannel]
            self.EncodersList_Speed_RPS_Raw[EncoderChannel] = self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_Speed_RPM_Raw[EncoderChannel] = self.EncodersList_Speed_RPS_Raw[EncoderChannel]*60.0

            self.EncodersList_Speed_EncoderTicksPerSecond_Filtered[EncoderChannel] = self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject[EncoderChannel].AddDataPointFromExternalProgram(self.EncodersList_Speed_EncoderTicksPerSecond_Raw[EncoderChannel])["SignalOutSmoothed"]
            self.EncodersList_Speed_RPS_Filtered[EncoderChannel] = self.EncodersList_Speed_EncoderTicksPerSecond_Filtered[EncoderChannel]/(4.0*self.EncodersList_CPR[EncoderChannel])
            self.EncodersList_Speed_RPM_Filtered[EncoderChannel] = self.EncodersList_Speed_RPS_Filtered[EncoderChannel] * 60.0
        ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderGENERALonErrorCallback(self, EncoderChannel, code, description):

        self.EncodersList_ErrorCallbackFiredFlag[EncoderChannel] = 1

        self.MyPrint_WithoutLogFile("EncoderGENERALonErrorCallback event for Encoder Channel " + str(EncoderChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onAttachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.EncoderGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onDetachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.EncoderGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onPositionChangeCallback(self, HandlerSelf, positionChange, timeChangeInMilliseconds, indexTriggered):

        EncoderChannel = 0
        self.EncoderGENERALonPositionChangeCallback(EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder0onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 0
        self.EncoderGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder1onAttachCallback(self, HandlerSelf):

        EncoderChannel = 1
        self.EncoderGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder1onDetachCallback(self, HandlerSelf):

        EncoderChannel = 1
        self.EncoderGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder1onPositionChangeCallback(self, HandlerSelf, positionChange, timeChangeInMilliseconds, indexTriggered):

        EncoderChannel = 1
        self.EncoderGENERALonPositionChangeCallback(EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder1onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 1
        self.EncoderGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def Encoder2onAttachCallback(self, HandlerSelf):

        EncoderChannel = 2
        self.EncoderGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder2onDetachCallback(self, HandlerSelf):

        EncoderChannel = 2
        self.EncoderGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder2onPositionChangeCallback(self, HandlerSelf, positionChange, timeChangeInMilliseconds, indexTriggered):

        EncoderChannel = 2
        self.EncoderGENERALonPositionChangeCallback(EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder2onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 2
        self.EncoderGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder3onAttachCallback(self, HandlerSelf):

        EncoderChannel = 3
        self.EncoderGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder3onDetachCallback(self, HandlerSelf):

        EncoderChannel = 3
        self.EncoderGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder3onPositionChangeCallback(self, HandlerSelf, positionChange, timeChangeInMilliseconds, indexTriggered):

        EncoderChannel = 3
        self.EncoderGENERALonPositionChangeCallback(EncoderChannel, positionChange, timeChangeInMilliseconds, indexTriggered)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Encoder3onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 3
        self.EncoderGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInputGENERALonAttachCallback(self, DIchannel):

        try:
            self.DigitalInputsList_AttachedAndOpenFlag[DIchannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalInputGENERALonAttachCallback event for DIchannel " + str(DIchannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.DigitalInputsList_AttachedAndOpenFlag[DIchannel] = 0
            self.MyPrint_WithoutLogFile("DigitalInputGENERALonAttachCallback event for DIchannel " + str(DIchannel) + ", ERROR: Failed to attach DigitalInput0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInputGENERALonDetachCallback(self, DIchannel):

        self.DigitalInputsList_AttachedAndOpenFlag[DIchannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ DigitalInputGENERALonDetachCallback event for DIchannel " + str(DIchannel) + ", Detached! $$$$$$$$$$")

        try:
            self.DigitalInputsList_PhidgetsDIobjects[DIchannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("DigitalInputGENERALonDetachCallback eent for DIchannel " + str(DIchannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInputGENERALonStateChangeCallback(self, DIchannel, state):

        self.DigitalInputsList_State[DIchannel] = state

        #self.MyPrint_WithoutLogFile("DigitalInputGENERALonStateChangeCallback event for DIchannel " + str(DIchannel) + ", State: " + str(state))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInputGENERALonErrorCallback(self, DIchannel, code, description):
        self.MyPrint_WithoutLogFile("DigitalInputGENERALonErrorCallback event for DIchannel " + str(DIchannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput0onAttachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.DigitalInputGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput0onDetachCallback(self, HandlerSelf):

        EncoderChannel = 0
        self.DigitalInputGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput0onStateChangeCallback(self, HandlerSelf, state):

        EncoderChannel = 0
        self.DigitalInputGENERALonStateChangeCallback(EncoderChannel, state)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput0onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 0
        self.DigitalInputGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput1onAttachCallback(self, HandlerSelf):

        EncoderChannel = 1
        self.DigitalInputGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput1onDetachCallback(self, HandlerSelf):

        EncoderChannel = 1
        self.DigitalInputGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput1onStateChangeCallback(self, HandlerSelf, state):

        EncoderChannel = 1
        self.DigitalInputGENERALonStateChangeCallback(EncoderChannel, state)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput1onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 1
        self.DigitalInputGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput2onAttachCallback(self, HandlerSelf):

        EncoderChannel = 2
        self.DigitalInputGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput2onDetachCallback(self, HandlerSelf):

        EncoderChannel = 2
        self.DigitalInputGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput2onStateChangeCallback(self, HandlerSelf, state):

        EncoderChannel = 2
        self.DigitalInputGENERALonStateChangeCallback(EncoderChannel, state)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput2onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 2
        self.DigitalInputGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput3onAttachCallback(self, HandlerSelf):

        EncoderChannel = 3
        self.DigitalInputGENERALonAttachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput3onDetachCallback(self, HandlerSelf):

        EncoderChannel = 3
        self.DigitalInputGENERALonDetachCallback(EncoderChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput3onStateChangeCallback(self, HandlerSelf, state):

        EncoderChannel = 3
        self.DigitalInputGENERALonStateChangeCallback(EncoderChannel, state)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DigitalInput3onErrorCallback(self, HandlerSelf, code, description):

        EncoderChannel = 3
        self.DigitalInputGENERALonErrorCallback(EncoderChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncoderHome(self, EncoderChannel, PositionToSetAsZero_EncoderTicks = -11111.0):

        if EncoderChannel in [0, 1, 2, 3]:

            ###########################
            if PositionToSetAsZero_EncoderTicks == -11111.0:
                PositionToSetAsZero_EncoderTicks = self.EncodersList_Position_EncoderTicks[EncoderChannel]
            ###########################

            self.EncodersList_HomingOffsetPosition_EncoderTicks[EncoderChannel] = PositionToSetAsZero_EncoderTicks
            self.EncodersList_Position_EncoderTicks[EncoderChannel] = self.EncodersList_Position_EncoderTicks[EncoderChannel] - self.EncodersList_HomingOffsetPosition_EncoderTicks[EncoderChannel]
            return 1

        else:
            self.MyPrint_WithoutLogFile("EncoderHome ERORR: EncoderChannel must be in set [0, 1, 2, 3].")
            return 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        self.MostRecentDataDict = dict([("EncodersList_Position_EncoderTicks", self.EncodersList_Position_EncoderTicks),
                                             ("EncodersList_Position_Rev", self.EncodersList_Position_Rev),
                                             ("EncodersList_Position_Degrees", self.EncodersList_Position_Degrees),
                                             ("EncodersList_IndexPosition_EncoderTicks", self.EncodersList_IndexPosition_EncoderTicks),
                                             ("EncodersList_IndexPosition_Rev", self.EncodersList_IndexPosition_Rev),
                                             ("EncodersList_IndexPosition_Degrees", self.EncodersList_IndexPosition_Degrees),
                                             ("EncodersList_Speed_EncoderTicksPerSecond_Raw", self.EncodersList_Speed_EncoderTicksPerSecond_Raw),
                                             ("EncodersList_Speed_RPM_Raw", self.EncodersList_Speed_RPM_Raw),
                                             ("EncodersList_Speed_RPS_Raw", self.EncodersList_Speed_RPS_Raw),
                                             ("EncodersList_Speed_EncoderTicksPerSecond_Filtered", self.EncodersList_Speed_EncoderTicksPerSecond_Filtered),
                                             ("EncodersList_Speed_RPM_Filtered", self.EncodersList_Speed_RPM_Filtered),
                                             ("EncodersList_Speed_RPS_Filtered", self.EncodersList_Speed_RPS_Filtered),
                                             ("EncodersList_ErrorCallbackFiredFlag", self.EncodersList_ErrorCallbackFiredFlag),
                                             ("DigitalInputsList_State", self.DigitalInputsList_State),
                                             ("DigitalInputsList_ErrorCallbackFiredFlag", self.DigitalInputsList_ErrorCallbackFiredFlag),
                                             ("Time", self.CurrentTime_CalculatedFromMainThread)])

        return self.MostRecentDataDict
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ###############################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ###############################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ###############################################

            ###############################################
            for EncoderChannel, NeedsToBeHomedFlag in enumerate(self.EncodersList_NeedsToBeHomedFlag):
                if NeedsToBeHomedFlag == 1:
                    SuccessFlag = self.EncoderHome(EncoderChannel)

                    if SuccessFlag == 1:
                        self.EncodersList_NeedsToBeHomedFlag[EncoderChannel] = 0
            ###############################################

            ############################################### USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            ###############################################
            ###############################################
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)

            ###############################################
            ###############################################
            ###############################################

        ###############################################

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartGUI(self, GuiParent=None):

        GUI_Thread_ThreadingObject = threading.Thread(target=self.GUI_Thread, args=(GuiParent,))
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent=None):

        print("Starting the GUI_Thread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")

        ###################################################
        if parent == None:  #This class object owns root and must handle it properly
            self.root = Tk()
            self.parent = self.root

            ################################################### SET THE DEFAULT FONT FOR ALL WIDGETS CREATED AFTTER/BELOW THIS CALL
            default_font = tkFont.nametofont("TkDefaultFont")
            default_font.configure(size=8)
            self.root.option_add("*Font", default_font)
            ###################################################

        else:
            self.root = parent
            self.parent = parent
        ###################################################

        ###################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        ###################################################

        ###################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        ###################################################

        #################################################
        self.device_info_label = Label(self.myFrame, text="Device Info", width=50) #, font=("Helvetica", 16)


        self.device_info_label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                         "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.device_info_label.grid(row=0, column=0, padx=5, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Encoders_Label = Label(self.myFrame, text="Encoders_Label", width=120)
        self.Encoders_Label.grid(row=0, column=1, padx=5, pady=1, columnspan=1, rowspan=10)
        #################################################
        
        #################################################

        self.EncoderHomingButtonsFrame = Frame(self.myFrame)

        #if self.UseBorderAroundThisGuiObjectFlag == 1:
        #    self.myFrame["borderwidth"] = 2
        #    self.myFrame["relief"] = "ridge"

        self.EncoderHomingButtonsFrame.grid(row = 1, column = 0, padx = 1, pady = 1, rowspan = 1, columnspan = 1)

        self.EncodersList_HomingButtonObjects = []
        for EncoderChannel in range(0, 4):
            self.EncodersList_HomingButtonObjects.append(Button(self.EncoderHomingButtonsFrame, text="Home Encoder " + str(EncoderChannel), state="normal", width=15, command=lambda i=EncoderChannel: self.EncodersList_HomingButtonObjectsResponse(i)))
            self.EncodersList_HomingButtonObjects[EncoderChannel].grid(row=1, column=EncoderChannel, padx=1, pady=1)
        #################################################

        ########################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=10)
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.protocol("WM_DELETE_WINDOW", self.ExitProgram_Callback)

            self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
            self.GUI_ready_to_be_updated_flag = 1
            self.root.mainloop()
        else:
            self.GUI_ready_to_be_updated_flag = 1
        ########################

        ########################
        if self.RootIsOwnedExternallyFlag == 0: #This class object owns root and must handle it properly
            self.root.quit()  # Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
            self.root.destroy()  # Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
        ########################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #######################################################
                    self.Encoders_Label["text"] = "Encoder Position Ticks: " + str(self.EncodersList_Position_EncoderTicks) + \
                                                "\nEncoder Position Degrees: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Position_Degrees, 0, 3) + \
                                                "\nIndex Pos: " + str(self.EncodersList_IndexPosition_EncoderTicks) + \
                                                "\nSpeed Ticks/S Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_EncoderTicksPerSecond_Raw, 0, 5)+ \
                                                "\nSpeed RPM Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPM_Raw, 0, 5) + \
                                                "\nSpeed RPS Raw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPS_Raw, 0, 5) + \
                                                "\nSpeed Ticks/S Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_EncoderTicksPerSecond_Filtered, 0, 5)+ \
                                                "\nSpeed RPM Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPM_Filtered, 0, 5) + \
                                                "\nSpeed RPS Filtered: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_Speed_RPS_Filtered, 0, 5) + \
                                                "\nDigital States: " + str(self.DigitalInputsList_State) + \
                                                "\nEncodersList_UpdateDeltaTseconds: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_UpdateDeltaTseconds, 0, 5) + \
                                                "\nEncodersList_CPR: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EncodersList_CPR, 0, 5) + \
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                                "\nMain Thread Frequency: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################

                #######################################################
                #######################################################
                if self.RootIsOwnedExternallyFlag == 0:  # This class object owns root and must handle it properly
                    self.root.after(self.GUI_RootAfterCallbackInterval_Milliseconds, self.GUI_update_clock)
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, input, print_result_flag = 0):

        result = isinstance(input, list)

        if print_result_flag == 1:
            self.MyPrint_WithoutLogFile("IsInputList: " + str(result))

        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers=4, number_of_decimal_places=3):
        IsListFlag = self.IsInputList(input)

        if IsListFlag == 0:
            float_number_list = [input]
        else:
            float_number_list = list(input)

        float_number_list_as_strings = []
        for element in float_number_list:
            try:
                element = float(element)
                prefix_string = "{:." + str(number_of_decimal_places) + "f}"
                element_as_string = prefix_string.format(element)
                float_number_list_as_strings.append(element_as_string)
            except:
                self.MyPrint_WithoutLogFile(self.TellWhichFileWereIn() + ": ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput ERROR: " + str(element) + " cannot be turned into a float")
                return -1

        StringToReturn = ""
        if IsListFlag == 0:
            StringToReturn = float_number_list_as_strings[0].zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
        else:
            StringToReturn = "["
            for index, StringElement in enumerate(float_number_list_as_strings):
                if float_number_list[index] >= 0:
                    StringElement = "+" + StringElement  # So that our strings always have either + or - signs to maintain the same string length

                StringElement = StringElement.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place

                if index != len(float_number_list_as_strings) - 1:
                    StringToReturn = StringToReturn + StringElement + ", "
                else:
                    StringToReturn = StringToReturn + StringElement + "]"

        return StringToReturn
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncodersList_HomingButtonObjectsResponse(self, EncoderChannelNumber):

        self.EncodersList_NeedsToBeHomedFlag[EncoderChannelNumber] = 1
        #self.MyPrint_WithoutLogFile("EncodersList_HomingButtonObjectsResponse: Event fired for EncoderChannelNumber " + str(EncoderChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################
