from .RoxiStateHandler import RoxiStateHandler, StateMachineStates
import time
import threading
import logging


class VersionNumber():
    major = 0
    minor = 0
    revision = 0
    build = 0

    def __init__(self, version):
        self.major    = (version & 0xFF000000) >> 24
        self.minor    = (version & 0x00FF0000) >> 16
        self.revision = (version & 0x0000FF00) >> 8
        self.build =    (version & 0x000000FF)

    def getVersionAsString(self):
        return "{0}.{1}.{2}-{3}".format(self.major, self.minor, self.revision, self.build)

########################################################################################################
#               CLASS   RoxiCommunication                                                              #
########################################################################################################
class RoxiCommunication():
    mStateHandler = RoxiStateHandler()
    mRunning = True

    def __init__(self):
        self.mRunning = True
        pass

    def GetDllVersion(self):
        version = self.mStateHandler.GetRoxiLibVersion()
        dllVersion = VersionNumber(version)
        return dllVersion.getVersionAsString()

    def __startHandler(self):
        while self.mRunning == True:
            self.mRunning = self.mStateHandler.ExecuteState()
            time.sleep(0.2) #Provide some time for other tasks as well.

    def Connect(self):
        self.thread = threading.Thread(target=self.__startHandler)
        self.thread.daemon = True
        self.thread.start()
        self.mStateHandler.SetIdleMode(False)
        pass

    def Shutdown(self):
        self.mStateHandler.Shutdown()
        logging.info("Shutdown issued .. ")
        self.thread.join()
        logging.info(" Join completed")

    def IsConnected(self):
        return self.mStateHandler.isConnected()

    def GetConnectedDevices(self):
        self.mStateHandler.SetIdleMode(False)
        return self.mStateHandler.GetDeviceList()

    def ClearConnectedDevices(self):
        self.mStateHandler.ClearDeviceList()
        self.mStateHandler.appendTask(StateMachineStates.GET_DEVICE_LIST)
        pass

    def UpdateDevice(self, deviceIndex):
        self.mStateHandler.SetIdleMode(False)
        return self.mStateHandler.UpdateDevice(deviceIndex)

    def UpdateDeviceStatusBusy(self):
        return self.mStateHandler.UpdateDeviceStatusBusy()

    def IsRunning(self):
        return self.mStateHandler.Running()

    def SetIdleMode(self):
        return self.mStateHandler.SetIdleMode(True)
