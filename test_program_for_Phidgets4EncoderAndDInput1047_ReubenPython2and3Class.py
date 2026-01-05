# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision L, 12/28/2025

Verified working on: Python 3.11/12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

#######################################################################################################################
#######################################################################################################################

###########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
###########################################################

###########################################################
from CSVdataLogger_ReubenPython3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from Phidgets4EncoderAndDInput1047_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import math
import traceback
import keyboard
###########################################################

###########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        traceback.print_exc()
        return ""
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global Phidgets4EncoderAndDInput1047_Object
    global Phidgets4EncoderAndDInput1047_OPEN_FLAG
    global SHOW_IN_GUI_Phidgets4EncoderAndDInput1047_FLAG
    global Phidgets4EncoderAndDInput1047_MostRecentDict_Label
    global Phidgets4EncoderAndDInput1047_MostRecentDict

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            Phidgets4EncoderAndDInput1047_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(Phidgets4EncoderAndDInput1047_MostRecentDict,
                                                                                                                         NumberOfDecimalsPlaceToUse=5,
                                                                                                                         NumberOfEntriesPerLine=1,
                                                                                                                         NumberOfTabsBetweenItems=1)
            #########################################################

            #########################################################
            if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1 and SHOW_IN_GUI_Phidgets4EncoderAndDInput1047_FLAG == 1:
                Phidgets4EncoderAndDInput1047_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if EntryListWithBlinking_OPEN_FLAG == 1:
                EntryListWithBlinking_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                CSVdataLogger_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    global Phidgets4EncoderAndDInput1047_Object
    global Phidgets4EncoderAndDInput1047_OPEN_FLAG

    global EntryListWithBlinking_Object
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_Object
    global CSVdataLogger_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_Phidgets4EncoderAndDInput1047_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_Phidgets4EncoderAndDInput1047
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_Phidgets4EncoderAndDInput1047 = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_Phidgets4EncoderAndDInput1047, text='   EncoderAndDI   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############

        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_Phidgets4EncoderAndDInput1047 = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global Phidgets4EncoderAndDInput1047_MostRecentDict_Label
    Phidgets4EncoderAndDInput1047_MostRecentDict_Label = Label(Tab_MainControls, text="Phidgets4EncoderAndDInput1047_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    Phidgets4EncoderAndDInput1047_MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1:
        Phidgets4EncoderAndDInput1047_Object.CreateGUIobjects(TkinterParent=Tab_Phidgets4EncoderAndDInput1047)
    #################################################
    #################################################

    #################################################
    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.CreateGUIobjects(TkinterParent=Tab_Phidgets4EncoderAndDInput1047)
    #################################################
    #################################################

    #################################################
    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.CreateGUIobjects(TkinterParent=Tab_Phidgets4EncoderAndDInput1047)
    #################################################
    #################################################

    #################################################
    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
if __name__ == '__main__':

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_Phidgets4EncoderAndDInput1047_FLAG
    USE_Phidgets4EncoderAndDInput1047_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 1

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 0

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_Phidgets4EncoderAndDInput1047_FLAG
    SHOW_IN_GUI_Phidgets4EncoderAndDInput1047_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_Phidgets4EncoderAndDInput1047
    global GUI_COLUMN_Phidgets4EncoderAndDInput1047
    global GUI_PADX_Phidgets4EncoderAndDInput1047
    global GUI_PADY_Phidgets4EncoderAndDInput1047
    global GUI_ROWSPAN_Phidgets4EncoderAndDInput1047
    global GUI_COLUMNSPAN_Phidgets4EncoderAndDInput1047
    GUI_ROW_Phidgets4EncoderAndDInput1047 = 0

    GUI_COLUMN_Phidgets4EncoderAndDInput1047 = 0
    GUI_PADX_Phidgets4EncoderAndDInput1047 = 1
    GUI_PADY_Phidgets4EncoderAndDInput1047 = 1
    GUI_ROWSPAN_Phidgets4EncoderAndDInput1047 = 1
    GUI_COLUMNSPAN_Phidgets4EncoderAndDInput1047 = 1

    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 1

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 2

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 3

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_Phidgets4EncoderAndDInput1047
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    #################################################
    #################################################

    #################################################
    #################################################
    global Phidgets4EncoderAndDInput1047_Object

    global Phidgets4EncoderAndDInput1047_OPEN_FLAG
    Phidgets4EncoderAndDInput1047_OPEN_FLAG = -1

    global Phidgets4EncoderAndDInput1047_MostRecentDict
    Phidgets4EncoderAndDInput1047_MostRecentDict = dict()

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_EncoderTicks
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_EncoderTicks = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Degrees
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Degrees = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_EncoderTicks
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_EncoderTicks = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Rev
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Rev = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Degrees
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Degrees = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Raw
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Raw = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Raw
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Raw = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Raw
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Raw = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Filtered
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Filtered = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Filtered
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Filtered = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered = [-11111.0] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_ErrorCallbackFiredFlag
    Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_ErrorCallbackFiredFlag = [-1] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_State
    Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_State = [-1] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_ErrorCallbackFiredFlag
    Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_ErrorCallbackFiredFlag = [-1] * 4

    global Phidgets4EncoderAndDInput1047_MostRecentDict_Time
    Phidgets4EncoderAndDInput1047_MostRecentDict_Time = -11111.0

    global EncodersList_SpeedUseExponentialFilterFlag_0
    EncodersList_SpeedUseExponentialFilterFlag_0 = 1

    global EncodersList_SpeedUseExponentialFilterFlag_1
    EncodersList_SpeedUseExponentialFilterFlag_1 = 1

    global EncodersList_SpeedUseExponentialFilterFlag_2
    EncodersList_SpeedUseExponentialFilterFlag_2 = 1

    global EncodersList_SpeedUseExponentialFilterFlag_3
    EncodersList_SpeedUseExponentialFilterFlag_3 = 1

    global EncodersList_SpeedExponentialFilterLambda_0
    EncodersList_SpeedExponentialFilterLambda_0 = 0.98
    
    global EncodersList_SpeedExponentialFilterLambda_1
    EncodersList_SpeedExponentialFilterLambda_1 = 0.98
    
    global EncodersList_SpeedExponentialFilterLambda_2
    EncodersList_SpeedExponentialFilterLambda_2 = 0.98
    
    global EncodersList_SpeedExponentialFilterLambda_3
    EncodersList_SpeedExponentialFilterLambda_3 = 0.98

    global Phidgets4EncoderAndDInput1047_NeedToUpdateSpeedFilterLambdaFlag
    Phidgets4EncoderAndDInput1047_NeedToUpdateSpeedFilterLambdaFlag = 0
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_Object

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 75
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_Object

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global Phidgets4EncoderAndDInput1047_GUIparametersDict
    Phidgets4EncoderAndDInput1047_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_Phidgets4EncoderAndDInput1047_FLAG),
                                                            ("EnableInternal_MyPrint_Flag", 0),
                                                            ("NumberOfPrintLines", 10),
                                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                                            ("GUI_ROW", GUI_ROW_Phidgets4EncoderAndDInput1047),
                                                            ("GUI_COLUMN", GUI_COLUMN_Phidgets4EncoderAndDInput1047),
                                                            ("GUI_PADX", GUI_PADX_Phidgets4EncoderAndDInput1047),
                                                            ("GUI_PADY", GUI_PADY_Phidgets4EncoderAndDInput1047),
                                                            ("GUI_ROWSPAN", GUI_ROWSPAN_Phidgets4EncoderAndDInput1047),
                                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_Phidgets4EncoderAndDInput1047)])

    global Phidgets4EncoderAndDInput1047_SetupDict
    Phidgets4EncoderAndDInput1047_SetupDict = dict([("GUIparametersDict", Phidgets4EncoderAndDInput1047_GUIparametersDict),
                                                    ("DesiredSerialNumber", -1), #-1 MEANS ANY SN, CHANGE THIS TO MATCH YOUR UNIQUE SERIAL NUMBER
                                                    ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                    ("NameToDisplay_UserSet", "Reuben's Test 1047 Board"),
                                                    ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                    ("EncoderUpdateDeltaT_ms", 8),
                                                    ("MainThread_TimeToSleepEachLoop", 0.001),
                                                    ("EncodersList_ChannelsBeingWatchedList", [1, 1, 1, 1]),
                                                    ("EncodersList_CPR", [1000, 128, 500, 8096]),
                                                    ("EncodersList_SpeedUseExponentialFilterFlag", [EncodersList_SpeedUseExponentialFilterFlag_0, EncodersList_SpeedUseExponentialFilterFlag_1, EncodersList_SpeedUseExponentialFilterFlag_2, EncodersList_SpeedUseExponentialFilterFlag_3]),
                                                    ("EncodersList_SpeedExponentialFilterLambda", [EncodersList_SpeedExponentialFilterLambda_0, EncodersList_SpeedExponentialFilterLambda_1, EncodersList_SpeedExponentialFilterLambda_2, EncodersList_SpeedExponentialFilterLambda_3]),
                                                    ("DigitalInputsList_ChannelsBeingWatchedList", [1, 1, 1, 1])])

    if USE_Phidgets4EncoderAndDInput1047_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            Phidgets4EncoderAndDInput1047_Object = Phidgets4EncoderAndDInput1047_ReubenPython2and3Class(Phidgets4EncoderAndDInput1047_SetupDict)
            Phidgets4EncoderAndDInput1047_OPEN_FLAG = Phidgets4EncoderAndDInput1047_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("Phidgets4EncoderAndDInput1047_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_Phidgets4EncoderAndDInput1047_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if Phidgets4EncoderAndDInput1047_OPEN_FLAG != 1:
                print("Failed to open Phidgets4EncoderAndDInput1047_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global EntryListWithBlinking_GUIparametersDict
    EntryListWithBlinking_GUIparametersDict = dict([("UseBorderAroundThisGuiObjectFlag", 0),
                                                    ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                                    ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                                    ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                                    ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                                    ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "EncodersList_SpeedUseExponentialFilterFlag_0"),("Type", "int"),("StartingVal", EncodersList_SpeedUseExponentialFilterFlag_0),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedUseExponentialFilterFlag_1"),("Type", "int"),("StartingVal", EncodersList_SpeedUseExponentialFilterFlag_1),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedUseExponentialFilterFlag_2"),("Type", "int"),("StartingVal", EncodersList_SpeedUseExponentialFilterFlag_2),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedUseExponentialFilterFlag_3"),("Type", "int"),("StartingVal", EncodersList_SpeedUseExponentialFilterFlag_3),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   
                                                   dict([("Name", "EncodersList_SpeedExponentialFilterLambda_0"),("Type", "float"),("StartingVal", EncodersList_SpeedExponentialFilterLambda_0),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedExponentialFilterLambda_1"),("Type", "float"),("StartingVal", EncodersList_SpeedExponentialFilterLambda_1),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedExponentialFilterLambda_2"),("Type", "float"),("StartingVal", EncodersList_SpeedExponentialFilterLambda_2),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "EncodersList_SpeedExponentialFilterLambda_3"),("Type", "float"),("StartingVal", EncodersList_SpeedExponentialFilterLambda_3),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

    global EntryListWithBlinking_SetupDict
    EntryListWithBlinking_SetupDict = dict([("GUIparametersDict", EntryListWithBlinking_GUIparametersDict),
                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                          ("DebugByPrintingVariablesFlag", 0),
                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])

    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_Object = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_SetupDict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open Phidgets4EncoderAndDInput1047_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global CSVdataLogger_GUIparametersDict
    CSVdataLogger_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                            ("EnableInternal_MyPrint_Flag", 1),
                                            ("NumberOfPrintLines", 10),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                            ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                            ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                            ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    global CSVdataLogger_SetupDict_VariableNamesForHeaderList
    CSVdataLogger_SetupDict_VariableNamesForHeaderList = ["Time",
                                                        "Pos_Rev_0",
                                                        "Pos_Rev_1",
                                                        "Pos_Rev_2",
                                                        "Pos_Rev_3",
                                                        "Speed_RPS_0",
                                                        "Speed_RPS_1",
                                                        "Speed_RPS_2",
                                                        "Speed_RPS_3"]

    print("CSVdataLogger_SetupDict_VariableNamesForHeaderList: " + str(CSVdataLogger_SetupDict_VariableNamesForHeaderList))

    global CSVdataLogger_SetupDict
    CSVdataLogger_SetupDict = dict([("GUIparametersDict", CSVdataLogger_GUIparametersDict),
                                    ("NameToDisplay_UserSet", "CSVdataLogger"),
                                    ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                    ("FileNamePrefix", "CSV_file_"),
                                    ("VariableNamesForHeaderList", CSVdataLogger_SetupDict_VariableNamesForHeaderList),
                                    ("MainThread_TimeToSleepEachLoop", 0.002),
                                    ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_Object = CSVdataLogger_ReubenPython3Class(CSVdataLogger_SetupDict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_Object_GUIparametersDict
    MyPrint_Object_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                            ("UseBorderAroundThisGuiObjectFlag", 0),
                                            ("GUI_ROW", GUI_ROW_MyPrint),
                                            ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                            ("GUI_PADX", GUI_PADX_MyPrint),
                                            ("GUI_PADY", GUI_PADY_MyPrint),
                                            ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                            ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_Object_SetupDict
    MyPrint_Object_SetupDict = dict([("NumberOfPrintLines", 10),
                                    ("WidthOfPrintingLabel", 200),
                                    ("PrintToConsoleFlag", 1),
                                    ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                    ("GUIparametersDict", MyPrint_Object_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_Object_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("GraphCanvasWidth", 900),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "My plotting example!"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])


    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Channel0", "Channel1", "Channel2", "Channel3"]),
                                                                                                        ("MarkerSizeList", [2, 2, 2, 2]),
                                                                                                        ("LineWidthList", [2, 2, 2, 2]),
                                                                                                        ("IncludeInXaxisAutoscaleCalculationList", [1, 1, 1, 1]),
                                                                                                        ("IncludeInYaxisAutoscaleCalculationList", [1, 1, 1, 1]),
                                                                                                        ("ColorList", ["Red", "Green", "Blue", "Purple"])])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 100),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 0),
                                                            ("X_min", 0.0),
                                                            ("X_max", 5.0),
                                                            ("Y_min", -5.0),
                                                            ("Y_max", 5.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("GraphNumberOfLeadingZeros", 0),
                                                            ("GraphNumberOfDecimalPlaces", 3),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder")),
                                                            ("KeepPlotterWindowAlwaysOnTopFlag", 0),
                                                            ("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", 0),
                                                            ("AllowResizingOfWindowFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ####################################################################################################################### KEY GUI LINE
    #######################################################################################################################
    #######################################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_Phidgets4EncoderAndDInput1047 = None
        Tab_MyPrint = None
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################
    print("Starting main loop 'test_program_for_Phidgets4EncoderAndDInput1047_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        #################################################
        #################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        #################################################
        #################################################

        ####################################################
        ####################################################

        ################################################### GET's
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_Object.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:
                    EncodersList_SpeedUseExponentialFilterFlag_0 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedUseExponentialFilterFlag_0"]
                    EncodersList_SpeedUseExponentialFilterFlag_1 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedUseExponentialFilterFlag_1"]
                    EncodersList_SpeedUseExponentialFilterFlag_2 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedUseExponentialFilterFlag_2"]
                    EncodersList_SpeedUseExponentialFilterFlag_3 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedUseExponentialFilterFlag_3"]

                    EncodersList_SpeedExponentialFilterLambda_0 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedExponentialFilterLambda_0"]
                    EncodersList_SpeedExponentialFilterLambda_1 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedExponentialFilterLambda_1"]
                    EncodersList_SpeedExponentialFilterLambda_2 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedExponentialFilterLambda_2"]
                    EncodersList_SpeedExponentialFilterLambda_3 = EntryListWithBlinking_MostRecentDict["EncodersList_SpeedExponentialFilterLambda_3"]

                    Phidgets4EncoderAndDInput1047_NeedToUpdateSpeedFilterLambdaFlag = 1

        ###################################################

        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################

        ####################################################
        ####################################################

        ################################################# GET's
        #################################################
        if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1:

            Phidgets4EncoderAndDInput1047_MostRecentDict = Phidgets4EncoderAndDInput1047_Object.GetMostRecentDataDict()

            if "Time" in Phidgets4EncoderAndDInput1047_MostRecentDict:
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_EncoderTicks = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Position_EncoderTicks"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Position_Rev"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Degrees = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Position_Degrees"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_EncoderTicks = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_IndexPosition_EncoderTicks"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Rev = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_IndexPosition_Rev"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_IndexPosition_Degrees = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_IndexPosition_Degrees"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Raw = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_EncoderTicksPerSecond_Raw"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Raw = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_RPM_Raw"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Raw = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_RPS_Raw"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_EncoderTicksPerSecond_Filtered = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_EncoderTicksPerSecond_Filtered"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Filtered = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_RPM_Filtered"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_Speed_RPS_Filtered"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_ErrorCallbackFiredFlag = Phidgets4EncoderAndDInput1047_MostRecentDict["EncodersList_ErrorCallbackFiredFlag"]

                Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_State = Phidgets4EncoderAndDInput1047_MostRecentDict["DigitalInputsList_State"]
                Phidgets4EncoderAndDInput1047_MostRecentDict_DigitalInputsList_ErrorCallbackFiredFlag = Phidgets4EncoderAndDInput1047_MostRecentDict["DigitalInputsList_ErrorCallbackFiredFlag"]

                Phidgets4EncoderAndDInput1047_MostRecentDict_Time = Phidgets4EncoderAndDInput1047_MostRecentDict["Time"]

                #print("Phidgets4EncoderAndDInput1047_MostRecentDict: " + str(Phidgets4EncoderAndDInput1047_MostRecentDict))
                #print("Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_EncoderTicks: " + str(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_EncoderTicks))
        #################################################
        #################################################

        ################################################# SET's
        #################################################
        if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1:

            if Phidgets4EncoderAndDInput1047_NeedToUpdateSpeedFilterLambdaFlag == 1:
                SpeedFilterDict = dict([("EncodersList_SpeedUseExponentialFilterFlag", [EncodersList_SpeedUseExponentialFilterFlag_0, EncodersList_SpeedUseExponentialFilterFlag_1, EncodersList_SpeedUseExponentialFilterFlag_2, EncodersList_SpeedUseExponentialFilterFlag_3]),
                                        ("EncodersList_SpeedExponentialFilterLambda", [EncodersList_SpeedExponentialFilterLambda_0, EncodersList_SpeedExponentialFilterLambda_1, EncodersList_SpeedExponentialFilterLambda_2, EncodersList_SpeedExponentialFilterLambda_3])])

                Phidgets4EncoderAndDInput1047_Object.UpdateSpeedFilterParameters(SpeedFilterDict)

                Phidgets4EncoderAndDInput1047_NeedToUpdateSpeedFilterLambdaFlag = 0
        #################################################
        #################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

            ####################################################
            ####################################################
            ListToWrite = []
            ListToWrite.append(CurrentTime_MainLoopThread)

            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev[0])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev[1])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev[2])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev[3])

            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered[0])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered[1])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered[2])
            ListToWrite.append(Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered[3])

            #print("ListToWrite: " + str(ListToWrite))
            ####################################################
            ####################################################

            CSVdataLogger_Object.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
            try:
                ####################################################
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= 0.030:

                            '''
                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1", "Channel2", "Channel3"],
                                                                                                                                    [CurrentTime_MainLoopThread]*4,
                                                                                                                                    [Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Raw[0],
                                                                                                                                     Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Filtered[0],
                                                                                                                                     Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Raw[1],
                                                                                                                                     Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPM_Filtered[1],])
                            '''

                            #'''
                            MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Channel0", "Channel1"],
                                                                                                                                    [CurrentTime_MainLoopThread]*2,
                                                                                                                                    [Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Position_Rev[0],
                                                                                                                                     Phidgets4EncoderAndDInput1047_MostRecentDict_EncodersList_Speed_RPS_Filtered[0]])
                            #'''

                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_IngeniaBLDC_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                traceback.print_exc()
        ####################################################
        ####################################################

        time.sleep(0.002)
    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

    ####################################################################################################################### THIS IS THE EXIT ROUTINE!
    #######################################################################################################################
    #######################################################################################################################
    print("Exiting main program 'test_program_for_Phidgets4EncoderAndDInput1047_ReubenPython2and3Class.")

    #################################################
    if Phidgets4EncoderAndDInput1047_OPEN_FLAG == 1:
        Phidgets4EncoderAndDInput1047_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    #################################################

    #######################################################################################################################
    #######################################################################################################################
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################