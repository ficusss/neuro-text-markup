import sys
import os
import platform
import time

from array import *
from ctypes import *
from sys import exit


class Brain:
    def __init__(self):
        self.currActive = [0 for _ in range(5)]

    def getActive(self):
        return self.currActive

    def go(self):
        try:
            if sys.platform.startswith('linux') and not platform.machine().startswith('arm'):
                srcDir = os.getcwd()
                libPath = srcDir + "/EmotivEpoc/linux64/libedk.so.3.3.3"
                libEDK = CDLL(libPath)
            else:
                raise Exception('System not supported.')
        except Exception as e:
            print('Error: cannot load EDK lib:', e)
            exit()

        IEE_EmoEngineEventCreate = libEDK.IEE_EmoEngineEventCreate
        IEE_EmoEngineEventCreate.restype = c_void_p
        eEvent = c_void_p(IEE_EmoEngineEventCreate())
        # print(eEvent, type(eEvent), c_uint(eEvent))
        IEE_EmoEngineEventGetEmoState = libEDK.IEE_EmoEngineEventGetEmoState
        IEE_EmoEngineEventGetEmoState.argtypes = [c_void_p, c_void_p]
        IEE_EmoEngineEventGetEmoState.restype = c_int

        IEE_EmoStateCreate = libEDK.IEE_EmoStateCreate
        IEE_EmoStateCreate.restype = c_void_p
        eState = c_void_p(IEE_EmoStateCreate())

        userID = c_uint(0)
        user = pointer(userID)
        ready = 0
        state = c_int(0)

        alphaValue = c_double(0)
        low_betaValue = c_double(0)
        high_betaValue = c_double(0)
        gammaValue = c_double(0)
        thetaValue = c_double(0)

        alpha = pointer(alphaValue)
        low_beta = pointer(low_betaValue)
        high_beta = pointer(high_betaValue)
        gamma = pointer(gammaValue)
        theta = pointer(thetaValue)

        channelList = array('I', [3, 7, 9, 12, 16])  # IED_AF3, IED_AF4, IED_T7, IED_T8, IED_Pz

        # -------------------------------------------------------------------------
        print("===================================================================")
        print("Example to get the average band power for a specific channel from" \
              " the latest epoch.")
        print("===================================================================")

        # -------------------------------------------------------------------------
        if libEDK.IEE_EngineConnect(bytes("Emotiv Systems-5".encode('utf-8'))) != 0:
            print("Emotiv Engine start up failed.")
            exit();

        print("Theta, Alpha, Low_beta, High_beta, Gamma \n")

        while True:
            state = libEDK.IEE_EngineGetNextEvent(eEvent)
            # print(eEvent)
            if state == 0:
                eventType = libEDK.IEE_EmoEngineEventGetType(eEvent)
                libEDK.IEE_EmoEngineEventGetUserId(eEvent, user)
                if eventType == 16:  # libEDK.IEE_Event_enum.IEE_UserAdded
                    ready = 1
                    libEDK.IEE_FFTSetWindowingType(userID, 1);  # 1: libEDK.IEE_WindowingTypes_enum.IEE_HAMMING
                    print("User added")

                if ready == 1:
                    for i in channelList:
                        result = c_int(0)
                        result = libEDK.IEE_GetAverageBandPowers(userID, i, theta, alpha, low_beta, high_beta, gamma)

                        if result == 0:  # EDK_OK
                             self.currActive = [thetaValue.value, alphaValue.value, low_betaValue.value,
                                               high_betaValue.value, gammaValue.value]

            elif state != 0x0600:
                print("Internal error in Emotiv Engine ! ", state)
            time.sleep(0.02)
        # -------------------------------------------------------------------------
        libEDK.IEE_EngineDisconnect()
        libEDK.IEE_EmoStateFree(eState)
        libEDK.IEE_EmoEngineEventFree(eEvent)