# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision K, 11/10/2024

Verified working on: Python 2.7, 3.12 for Windows 8.1, 10, and 11 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

###########################################################
from LowPassFilter_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import traceback
###########################################################

###########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###########################################################

###########################################################
if sys.version_info[0] < 3:
    import Queue  # Python 2
else:
    import queue as Queue  # Python 3
###########################################################

###########################################################
if sys.version_info[0] < 3:
    from builtins import raw_input as input
else:
    from future.builtins import input as input
########################################################### "sudo pip3 install future" (Python 3) AND "sudo pip install future" (Python 2)

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.DigitalInput import *
###########################################################

class Phidgets4EncoderAndDInput1047_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    #######################################################################################################################
    #######################################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0
        #########################################################

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

        self.NumberOfEncoders = 4
        self.NumberOfDigitalInputs = 4

        self.EncodersList_PhidgetsEncoderObjects = list()

        self.EncodersList_AttachedAndOpenFlag = [0.0] * self.NumberOfEncoders
        self.EncodersList_NeedsToBeHomedFlag = [0] * self.NumberOfEncoders
        self.EncodersList_UpdateDeltaTseconds = [0.0] * self.NumberOfEncoders
        self.EncodersList_UpdateFrequencyHz = [0.0] * self.NumberOfEncoders
        self.EncodersList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfEncoders

        self.EncodersList_Position_EncoderTicks = [0.0] * self.NumberOfEncoders
        self.EncodersList_Position_Rev = [0.0] * self.NumberOfEncoders
        self.EncodersList_Position_Degrees = [0.0] * self.NumberOfEncoders

        self.EncodersList_IndexPosition_EncoderTicks = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_IndexPosition_Rev = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_IndexPosition_Degrees = [-11111.0] * self.NumberOfEncoders

        self.EncodersList_HomingOffsetPosition_EncoderTicks = [0.0] * self.NumberOfEncoders

        self.EncodersList_Speed_EncoderTicksPerSecond_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPM_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPS_Raw = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject = list()
        self.EncodersList_Speed_EncoderTicksPerSecond_Filtered = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPM_Filtered = [-11111.0] * self.NumberOfEncoders
        self.EncodersList_Speed_RPS_Filtered = [-11111.0] * self.NumberOfEncoders

        self.EncodersList_Speed_UpdateFilterParameters_EventNeedsToBeFiredFlag = 0

        self.DigitalInputsList_PhidgetsDIobjects = list()

        self.DigitalInputsList_AttachedAndOpenFlag = [0.0] * self.NumberOfDigitalInputs
        self.DigitalInputsList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfDigitalInputs
        self.DigitalInputsList_State = [-1] * self.NumberOfDigitalInputs

        self.EncodersList_SpeedUseMedianFilterFlag_Rx = [-1]*self.NumberOfEncoders
        self.EncodersList_SpeedMedianFilterKernelSize_Rx = [-1]*self.NumberOfEncoders
        self.EncodersList_SpeedUseExponentialFilterFlag_Rx = [-1]*self.NumberOfEncoders
        self.EncodersList_SpeedExponentialFilterLambda_Rx = [-1]*self.NumberOfEncoders

        self.MostRecentDataDict = dict()

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

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Error, must pass in 'root'")
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG = " + str(self.USE_GUI_FLAG))

        #print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSerialNumber" in setup_dict:
            try:
                self.DesiredSerialNumber = int(setup_dict["DesiredSerialNumber"])
            except:
                print("Error: DesiredSerialNumber invalid.")
        else:
            self.DesiredSerialNumber = -1
        
        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in setup_dict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", setup_dict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in setup_dict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", setup_dict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncoderUpdateDeltaT_ms" in setup_dict:
            self.EncoderUpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncoderUpdateDeltaT_ms", setup_dict["EncoderUpdateDeltaT_ms"], 8.0, 60000.0))
        else:
            self.EncoderUpdateDeltaT_ms = 8

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: EncoderUpdateDeltaT_ms: " + str(self.EncoderUpdateDeltaT_ms))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_ChannelsBeingWatchedList" in setup_dict:
            EncodersList_ChannelsBeingWatchedList_TEMP = setup_dict["EncodersList_ChannelsBeingWatchedList"]
            if self.IsInputList(EncodersList_ChannelsBeingWatchedList_TEMP) == 1 and len(EncodersList_ChannelsBeingWatchedList_TEMP)== self.NumberOfEncoders:
                self.EncodersList_ChannelsBeingWatchedList = list()
                for EncoderChannel, EnabledState_TEMP in enumerate(EncodersList_ChannelsBeingWatchedList_TEMP):
                    EnabledState = self.PassThrough0and1values_ExitProgramOtherwise("EncodersList_ChannelsBeingWatchedList, EncoderChannel " + str(EncoderChannel), EnabledState_TEMP)
                    self.EncodersList_ChannelsBeingWatchedList.append(EnabledState)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Error, 'EncodersList_ChannelsBeingWatchedList' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.EncodersList_ChannelsBeingWatchedList = [1]*self.NumberOfEncoders

        ######## We examine self.EncodersList_ChannelsBeingWatchedList[0] to obtain device information for the boardm so this channel must be watched.
        if self.EncodersList_ChannelsBeingWatchedList[0] != 1:
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Caution! 0th index of EncodersList_ChannelsBeingWatchedList must be 1!")
            self.EncodersList_ChannelsBeingWatchedList[0] = 1
        ########

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: EncodersList_ChannelsBeingWatchedList: " + str(self.EncodersList_ChannelsBeingWatchedList))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_CPR" in setup_dict:
            EncodersList_CPR_TEMP = setup_dict["EncodersList_CPR"]
            if self.IsInputList(EncodersList_CPR_TEMP) == 1 and len(EncodersList_CPR_TEMP)== self.NumberOfEncoders:
                self.EncodersList_CPR = list()
                for EncoderChannel, CPR_TEMP in enumerate(EncodersList_CPR_TEMP):
                    CPR = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_CPR, EncoderChannel " + str(EncoderChannel), CPR_TEMP, 0, 250000)
                    self.EncodersList_CPR.append(CPR)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Error, 'EncodersList_CPR' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.EncodersList_CPR = [1]*self.NumberOfEncoders

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: EncodersList_CPR: " + str(self.EncodersList_CPR))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.UpdateSpeedFilterParameters(setup_dict)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DigitalInputsList_ChannelsBeingWatchedList" in setup_dict:
            DigitalInputsList_ChannelsBeingWatchedList_TEMP = setup_dict["DigitalInputsList_ChannelsBeingWatchedList"]
            if self.IsInputList(DigitalInputsList_ChannelsBeingWatchedList_TEMP) == 1 and len(DigitalInputsList_ChannelsBeingWatchedList_TEMP)== self.NumberOfDigitalInputs:
                self.DigitalInputsList_ChannelsBeingWatchedList = list()
                for DigitalInputChannel, EnabledState_TEMP in enumerate(DigitalInputsList_ChannelsBeingWatchedList_TEMP):
                    EnabledState = self.PassThrough0and1values_ExitProgramOtherwise("DigitalInputsList_ChannelsBeingWatchedList, DigitalInputChannel " + str(DigitalInputChannel), EnabledState_TEMP)
                    self.DigitalInputsList_ChannelsBeingWatchedList.append(EnabledState)
            else:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Error, 'DigitalInputsList_ChannelsBeingWatchedList' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.DigitalInputsList_ChannelsBeingWatchedList = [1]*self.NumberOfDigitalInputs

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DigitalInputsList_ChannelsBeingWatchedList: " + str(self.DigitalInputsList_ChannelsBeingWatchedList))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in setup_dict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", setup_dict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            for EncoderChannel in range(0, self.NumberOfEncoders):
                self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", self.EncodersList_SpeedUseMedianFilterFlag[EncoderChannel]),
                                                                                                                                     ("MedianFilterKernelSize", self.EncodersList_SpeedMedianFilterKernelSize[EncoderChannel]),
                                                                                                                                     ("UseExponentialSmoothingFilterFlag", self.EncodersList_SpeedUseExponentialFilterFlag[EncoderChannel]),
                                                                                                                                     ("ExponentialSmoothingFilterLambda", self.EncodersList_SpeedExponentialFilterLambda[EncoderChannel])])))
                #time.sleep(0.1)
                LOWPASSFILTER_OPEN_FLAG = self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject[EncoderChannel].OBJECT_CREATED_SUCCESSFULLY_FLAG
    
                if LOWPASSFILTER_OPEN_FLAG != 1:
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to open LowPassFilter_ReubenPython2and3ClassObject.")
                    return

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.EncoderInputsList_ListOfOnAttachCallbackFunctionNames = [self.Encoder0onAttachCallback, self.Encoder1onAttachCallback, self.Encoder2onAttachCallback, self.Encoder3onAttachCallback]
        self.EncoderInputsList_ListOfOnDetachCallbackFunctionNames = [self.Encoder0onDetachCallback, self.Encoder1onDetachCallback, self.Encoder2onDetachCallback, self.Encoder3onDetachCallback]
        self.EncoderInputsList_ListOfOnErrorCallbackFunctionNames = [self.Encoder0onErrorCallback, self.Encoder1onErrorCallback, self.Encoder2onErrorCallback, self.Encoder3onErrorCallback]
        self.EncoderInputsList_ListOfOnEncoderOnPositionChangeCallbackFunctionNames = [self.Encoder0onPositionChangeCallback, self.Encoder1onPositionChangeCallback, self.Encoder2onPositionChangeCallback, self.Encoder3onPositionChangeCallback]

        self.DigitalInputsList_ListOfOnAttachCallbackFunctionNames = [self.DigitalInput0onAttachCallback, self.DigitalInput1onAttachCallback, self.DigitalInput2onAttachCallback, self.DigitalInput3onAttachCallback]
        self.DigitalInputsList_ListOfOnDetachCallbackFunctionNames = [self.DigitalInput0onDetachCallback, self.DigitalInput1onDetachCallback, self.DigitalInput2onDetachCallback, self.DigitalInput3onDetachCallback]
        self.DigitalInputsList_ListOfOnErrorCallbackFunctionNames = [self.DigitalInput0onErrorCallback, self.DigitalInput1onErrorCallback, self.DigitalInput2onErrorCallback, self.DigitalInput3onErrorCallback]
        self.DigitalInputsList_ListOfonStateChangeCallbackFunctionNames = [self.DigitalInput0onStateChangeCallback, self.DigitalInput1onStateChangeCallback, self.DigitalInput2onStateChangeCallback, self.DigitalInput3onStateChangeCallback]
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            #########################################################
            for EncoderChannel in range(0, self.NumberOfEncoders):
                if self.EncodersList_ChannelsBeingWatchedList[EncoderChannel] == 1:
                    self.EncodersList_PhidgetsEncoderObjects.append(Encoder())

                    if self.DesiredSerialNumber != -1:
                        self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setDeviceSerialNumber(self.DesiredSerialNumber)

                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setChannel(EncoderChannel)
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setOnPositionChangeHandler(self.EncoderInputsList_ListOfOnEncoderOnPositionChangeCallbackFunctionNames[EncoderChannel])
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setOnAttachHandler(self.EncoderInputsList_ListOfOnAttachCallbackFunctionNames[EncoderChannel])
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setOnDetachHandler(self.EncoderInputsList_ListOfOnDetachCallbackFunctionNames[EncoderChannel])
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].setOnErrorHandler(self.EncoderInputsList_ListOfOnErrorCallbackFunctionNames[EncoderChannel])
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

                else:
                    self.EncodersList_PhidgetsEncoderObjects.append("NULL")
            #########################################################

            #########################################################
            for DigitalInputChannel in range(0, self.NumberOfDigitalInputs):
                if self.DigitalInputsList_ChannelsBeingWatchedList[DigitalInputChannel] == 1:
                    self.DigitalInputsList_PhidgetsDIobjects.append(DigitalInput())

                    if self.DesiredSerialNumber != -1:
                        self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setDeviceSerialNumber(self.DesiredSerialNumber)

                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setChannel(DigitalInputChannel)
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setOnStateChangeHandler(self.DigitalInputsList_ListOfonStateChangeCallbackFunctionNames[DigitalInputChannel])
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setOnAttachHandler(self.DigitalInputsList_ListOfOnAttachCallbackFunctionNames[DigitalInputChannel])
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setOnDetachHandler(self.DigitalInputsList_ListOfOnDetachCallbackFunctionNames[DigitalInputChannel])
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].setOnErrorHandler(self.DigitalInputsList_ListOfOnErrorCallbackFunctionNames[DigitalInputChannel])
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
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
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Enabled Phidget Logging.")

                except PhidgetException as e:
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.EncodersList_PhidgetsEncoderObjects[0].getDeviceName()
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceSerialNumber = self.EncodersList_PhidgetsEncoderObjects[0].getDeviceSerialNumber()
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DetectedDeviceSerialNumber: " + str(self.DetectedDeviceSerialNumber))

            except PhidgetException as e:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceID = self.EncodersList_PhidgetsEncoderObjects[0].getDeviceID()
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceVersion = self.EncodersList_PhidgetsEncoderObjects[0].getDeviceVersion()
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.EncodersList_PhidgetsEncoderObjects[0].getLibraryVersion()
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################

            #########################################################
            if self.DesiredSerialNumber != -1:
                if self.DetectedDeviceSerialNumber != self.DesiredSerialNumber:
                    print("Phidgets4EncoderAndDInput1047_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.DetectedDeviceSerialNumber) + ").")
                    self.CloseAllEncoderChannels()
                    self.CloseAllDigitalInputChannels()
                    time.sleep(0.25)
                    return
            #########################################################

            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################

            #########################################################
            if self.USE_GUI_FLAG == 1:
                self.StartGUI(self.root)
            #########################################################

            #########################################################
            time.sleep(0.25)
            #########################################################

            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################

        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def __del__(self):
        pass
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def UpdateSpeedFilterParameters(self, setup_dict):

        #########################################################
        #########################################################
        if "EncodersList_SpeedUseMedianFilterFlag" in setup_dict:
            self.Process_EncodersList_SpeedUseMedianFilterFlag(setup_dict["EncodersList_SpeedUseMedianFilterFlag"])
        else:
            self.EncodersList_SpeedUseMedianFilterFlag = [1] * self.NumberOfEncoders
        #########################################################
        #########################################################
        
        #########################################################
        #########################################################
        if "EncodersList_SpeedMedianFilterKernelSize" in setup_dict:
            self.Process_EncodersList_SpeedMedianFilterKernelSize(setup_dict["EncodersList_SpeedMedianFilterKernelSize"])
        else:
            self.EncodersList_SpeedMedianFilterKernelSize = [5.0] * self.NumberOfEncoders
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_SpeedUseExponentialFilterFlag" in setup_dict:
            self.Process_EncodersList_SpeedUseExponentialFilterFlag(setup_dict["EncodersList_SpeedUseExponentialFilterFlag"])
        else:
            self.EncodersList_SpeedUseExponentialFilterFlag = [1] * self.NumberOfEncoders
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EncodersList_SpeedExponentialFilterLambda" in setup_dict:
            self.Process_EncodersList_SpeedExponentialFilterLambda(setup_dict["EncodersList_SpeedExponentialFilterLambda"])
        else:
            self.EncodersList_SpeedExponentialFilterLambda = [0.5] * self.NumberOfEncoders  #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        #########################################################
        #########################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def Process_EncodersList_SpeedUseMedianFilterFlag(self, EncodersList_SpeedUseMedianFilterFlag_TEMP=[]):

        try:
            
            #########################################################
            #########################################################
            if self.IsInputList(EncodersList_SpeedUseMedianFilterFlag_TEMP) == 1 and len(EncodersList_SpeedUseMedianFilterFlag_TEMP) == self.NumberOfEncoders:
                self.EncodersList_SpeedUseMedianFilterFlag = list()
                for EncoderChannel, UseMedianFilterFlag_TEMP in enumerate(EncodersList_SpeedUseMedianFilterFlag_TEMP):
                    UseMedianFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("EncodersList_SpeedUseMedianFilterFlag, EncoderChannel " + str(EncoderChannel), UseMedianFilterFlag_TEMP)
                    self.EncodersList_SpeedUseMedianFilterFlag.append(UseMedianFilterFlag)
            else:
                print("Process_EncodersList_SpeedUseMedianFilterFlag: Error, 'EncodersList_SpeedUseMedianFilterFlag' must be a length of length 4 with values of 0 or 1.")
                return

            print("Process_EncodersList_SpeedUseMedianFilterFlag: EncodersList_SpeedUseMedianFilterFlag: " + str(self.EncodersList_SpeedUseMedianFilterFlag))
            #########################################################
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Process_EncodersList_SpeedUseMedianFilterFlag Exceptions: %s" % exceptions)
            traceback.print_exc()

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def Process_EncodersList_SpeedMedianFilterKernelSize(self, EncodersList_SpeedMedianFilterKernelSize_TEMP=[]):

        try:
            #########################################################
            #########################################################
            if self.IsInputList(EncodersList_SpeedMedianFilterKernelSize_TEMP) == 1 and len(EncodersList_SpeedMedianFilterKernelSize_TEMP)== self.NumberOfEncoders:
                self.EncodersList_SpeedMedianFilterKernelSize = list()
                for EncoderChannel, SpeedMedianFilterKernelSize_TEMP in enumerate(EncodersList_SpeedMedianFilterKernelSize_TEMP):
                    SpeedMedianFilterKernelSize = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_SpeedMedianFilterKernelSize, EncoderChannel " + str(EncoderChannel), SpeedMedianFilterKernelSize_TEMP, 3.0, 100.0))
                    self.EncodersList_SpeedMedianFilterKernelSize.append(SpeedMedianFilterKernelSize)

                self.EncodersList_Speed_UpdateFilterParameters_EventNeedsToBeFiredFlag = 1
            else:
                print("Process_EncodersList_SpeedMedianFilterKernelSize: Error, 'EncodersList_SpeedMedianFilterKernelSize' must be a length of length 4 with values in [3, 100].")
                return

            print("Process_EncodersList_SpeedMedianFilterKernelSize: EncodersList_SpeedMedianFilterKernelSize: " + str(self.EncodersList_SpeedMedianFilterKernelSize))
            #########################################################
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Process_EncodersList_SpeedMedianFilterKernelSize Exceptions: %s" % exceptions)
            traceback.print_exc()

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def Process_EncodersList_SpeedUseExponentialFilterFlag(self, EncodersList_SpeedUseExponentialFilterFlag_TEMP=[]):

        try:
            
            #########################################################
            #########################################################
            if self.IsInputList(EncodersList_SpeedUseExponentialFilterFlag_TEMP) == 1 and len(EncodersList_SpeedUseExponentialFilterFlag_TEMP) == self.NumberOfEncoders:
                self.EncodersList_SpeedUseExponentialFilterFlag = list()
                for EncoderChannel, UseExponentialFilterFlag_TEMP in enumerate(EncodersList_SpeedUseExponentialFilterFlag_TEMP):
                    UseExponentialFilterFlag = self.PassThrough0and1values_ExitProgramOtherwise("EncodersList_SpeedUseExponentialFilterFlag, EncoderChannel " + str(EncoderChannel), UseExponentialFilterFlag_TEMP)
                    self.EncodersList_SpeedUseExponentialFilterFlag.append(UseExponentialFilterFlag)
            else:
                print("Process_EncodersList_SpeedUseExponentialFilterFlag: Error, 'EncodersList_SpeedUseExponentialFilterFlag' must be a length of length 4 with values of 0 or 1.")
                return

            print("Process_EncodersList_SpeedUseExponentialFilterFlag: EncodersList_SpeedUseExponentialFilterFlag: " + str(self.EncodersList_SpeedUseExponentialFilterFlag))
            #########################################################
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Process_EncodersList_SpeedUseExponentialFilterFlag Exceptions: %s" % exceptions)
            traceback.print_exc()

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    def Process_EncodersList_SpeedExponentialFilterLambda(self, EncodersList_SpeedExponentialFilterLambda_TEMP=[]):

        try:
            #########################################################
            #########################################################
            if self.IsInputList(EncodersList_SpeedExponentialFilterLambda_TEMP) == 1 and len(EncodersList_SpeedExponentialFilterLambda_TEMP)== self.NumberOfEncoders:
                self.EncodersList_SpeedExponentialFilterLambda = list()
                for EncoderChannel, SpeedExponentialFilterLambda_TEMP in enumerate(EncodersList_SpeedExponentialFilterLambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("EncodersList_SpeedExponentialFilterLambda, EncoderChannel " + str(EncoderChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.EncodersList_SpeedExponentialFilterLambda.append(SpeedExponentialFilterLambda)

                self.EncodersList_Speed_UpdateFilterParameters_EventNeedsToBeFiredFlag = 1
            else:
                print("Process_EncodersList_SpeedExponentialFilterLambda: Error, 'EncodersList_SpeedExponentialFilterLambda' must be a length of length 4 with values in [0.0, 1.0].")
                return

            print("Process_EncodersList_SpeedExponentialFilterLambda: EncodersList_SpeedExponentialFilterLambda: " + str(self.EncodersList_SpeedExponentialFilterLambda))
            #########################################################
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("Process_EncodersList_SpeedExponentialFilterLambda Exceptions: %s" % exceptions)
            traceback.print_exc()

    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
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
    ##########################################################################################################
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

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.
        
        else:
            return dict() #So that we're not returning variables during the close-down process.
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
    ##########################################################################################################
    ########################################################################################################## unicorn
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")
        
        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################

            ##########################################################################################################
            if self.EncodersList_Speed_UpdateFilterParameters_EventNeedsToBeFiredFlag == 1:

                for EncoderChannel in range(0, self.NumberOfEncoders):
                    self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject[EncoderChannel].UpdateFilterParameters(dict([("UseMedianFilterFlag", self.EncodersList_SpeedUseMedianFilterFlag[EncoderChannel]),
                                                                                                                                    ("MedianFilterKernelSize", self.EncodersList_SpeedMedianFilterKernelSize[EncoderChannel]),
                                                                                                                                    ("UseExponentialSmoothingFilterFlag", self.EncodersList_SpeedUseExponentialFilterFlag[EncoderChannel]),
                                                                                                                                    ("ExponentialSmoothingFilterLambda", self.EncodersList_SpeedExponentialFilterLambda[EncoderChannel])]))

            self.EncodersList_Speed_UpdateFilterParameters_EventNeedsToBeFiredFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            for EncoderChannel, NeedsToBeHomedFlag in enumerate(self.EncodersList_NeedsToBeHomedFlag):
                if NeedsToBeHomedFlag == 1:
                    SuccessFlag = self.EncoderHome(EncoderChannel)

                    if SuccessFlag == 1:
                        self.EncodersList_NeedsToBeHomedFlag[EncoderChannel] = 0
            ##########################################################################################################

            '''
            ########################################################################################################## For debugging only
            try:
                for EncoderChannel in range(0, self.NumberOfEncoders):
                    DictTemp = self.EncodersList_Speed_LowPassFilter_ReubenPython2and3ClassObject[EncoderChannel].GetMostRecentDataDict()
                    #print("DictTemp: " + str(DictTemp))

                    if "UseMedianFilterFlag" in DictTemp:
                        self.EncodersList_SpeedUseMedianFilterFlag_Rx[EncoderChannel] = DictTemp["UseMedianFilterFlag"]

                    if "MedianFilterKernelSize" in DictTemp:
                        self.EncodersList_SpeedMedianFilterKernelSize_Rx[EncoderChannel] = DictTemp["MedianFilterKernelSize"]

                    if "UseExponentialSmoothingFilterFlag" in DictTemp:
                        self.EncodersList_SpeedUseExponentialFilterFlag_Rx[EncoderChannel] = DictTemp["UseExponentialSmoothingFilterFlag"]

                    if "ExponentialSmoothingFilterLambda" in DictTemp:
                        self.EncodersList_SpeedExponentialFilterLambda_Rx[EncoderChannel] = DictTemp["ExponentialSmoothingFilterLambda"]

            except:
                exceptions = sys.exc_info()[0]
                print("Exceptions: %s" % exceptions)
                traceback.print_exc()
            ##########################################################################################################
            '''

            ##########################################################################################################
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
                                                 ("EncodersList_SpeedUseMedianFilterFlag", self.EncodersList_SpeedUseMedianFilterFlag),
                                                 ("EncodersList_SpeedMedianFilterKernelSize", self.EncodersList_SpeedMedianFilterKernelSize),
                                                 ("EncodersList_SpeedUseExponentialFilterFlag", self.EncodersList_SpeedUseExponentialFilterFlag),
                                                 ("EncodersList_SpeedExponentialFilterLambda", self.EncodersList_SpeedExponentialFilterLambda),
                                                 ("EncodersList_SpeedUseMedianFilterFlag_Rx", self.EncodersList_SpeedUseMedianFilterFlag_Rx),
                                                 ("EncodersList_SpeedMedianFilterKernelSize_Rx", self.EncodersList_SpeedMedianFilterKernelSize_Rx),
                                                 ("EncodersList_SpeedUseExponentialFilterFlag_Rx", self.EncodersList_SpeedUseExponentialFilterFlag_Rx),
                                                 ("EncodersList_SpeedExponentialFilterLambda_Rx", self.EncodersList_SpeedExponentialFilterLambda_Rx),
                                                 ("Time", self.CurrentTime_CalculatedFromMainThread)])
            ##########################################################################################################

            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        self.CloseAllEncoderChannels()
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        self.CloseAllDigitalInputChannels()
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")
        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseAllEncoderChannels(self):

        try:
            for EncoderChannel in range(0, self.NumberOfEncoders):
                if self.EncodersList_ChannelsBeingWatchedList[EncoderChannel] == 1:
                    self.EncodersList_PhidgetsEncoderObjects[EncoderChannel].close()

        except PhidgetException as e:
            print("CloseAllEncoderChannels, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseAllDigitalInputChannels(self):

        try:
            for DigitalInputChannel in range(0, self.NumberOfDigitalInputs):
                if self.DigitalInputsList_ChannelsBeingWatchedList[DigitalInputChannel] == 1:
                    self.DigitalInputsList_PhidgetsDIobjects[DigitalInputChannel].close()

        except PhidgetException as e:
            print("CloseAllDigitalInputChannels, Phidget Exception %i: %s" % (e.code, e.details))

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
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object.")

        ###################################################
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
        ###################################################

        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50) #, font=("Helvetica", 16)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nDevice Serial Number: " + str(self.DetectedDeviceSerialNumber) + \
                                         "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        
        #################################################
        self.EncoderHomingButtonsFrame = Frame(self.myFrame)
        self.EncoderHomingButtonsFrame.grid(row = 1, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 1)

        self.EncodersList_HomingButtonObjects = []
        for EncoderChannel in range(0, self.NumberOfEncoders):
            self.EncodersList_HomingButtonObjects.append(Button(self.EncoderHomingButtonsFrame, text="Home Encoder " + str(EncoderChannel), state="normal", width=15, command=lambda i=EncoderChannel: self.EncodersList_HomingButtonObjectsResponse(i)))
            self.EncodersList_HomingButtonObjects[EncoderChannel].grid(row=1, column=EncoderChannel, padx=1, pady=1, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################

        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
        #################################################

        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################

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
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 3,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 1)
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
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EncodersList_HomingButtonObjectsResponse(self, EncoderChannelNumber):

        self.HomeEncoder(EncoderChannelNumber)
        #self.MyPrint_WithoutLogFile("EncodersList_HomingButtonObjectsResponse: Event fired for EncoderChannelNumber " + str(EncoderChannelNumber))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def HomeEncoder(self, EncoderChannelNumber):

        self.EncodersList_NeedsToBeHomedFlag[EncoderChannelNumber] = 1
        print("HomeEncoder: Event fired for EncoderChannelNumber " + str(EncoderChannelNumber))

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

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################