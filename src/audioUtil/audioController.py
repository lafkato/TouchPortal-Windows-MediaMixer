from ctypes import POINTER, cast

import comtypes
import pythoncom
from comtypes import CLSCTX_ALL
from pycaw.constants import CLSID_MMDeviceEnumerator
from pycaw.pycaw import (AudioUtilities, EDataFlow, IAudioEndpointVolume,
                         IMMDeviceEnumerator)


class AudioController(object):
    def __init__(self, process_name):
        self.process_name = process_name
        self.volume = self.process_volume()

    def process_volume(self):
        pythoncom.CoInitialize()
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume
                if session.Process and session.Process.name() == self.process_name:
                    return interface.GetMasterVolume()
        finally:
            pythoncom.CoUninitialize()

    def set_volume(self, decibels):
        pythoncom.CoInitialize()
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume
                if session.Process and session.Process.name() == self.process_name:
                    self.volume = min(1.0, max(0.0, decibels))
                    interface.SetMasterVolume(self.volume, None)
        finally:
            pythoncom.CoUninitialize()

    def decrease_volume(self, decibels):
        pythoncom.CoInitialize()
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume
                if session.Process and session.Process.name() == self.process_name:
                    self.volume = max(0.0, self.volume - decibels)
                    interface.SetMasterVolume(self.volume, None)
        finally:
            pythoncom.CoUninitialize()

    def increase_volume(self, decibels):
        pythoncom.CoInitialize()
        try:
            sessions = AudioUtilities.GetAllSessions()
            for session in sessions:
                interface = session.SimpleAudioVolume
                if session.Process and session.Process.name() == self.process_name:
                    self.volume = min(1.0, self.volume + decibels)
                    interface.SetMasterVolume(self.volume, None)
        finally:
            pythoncom.CoUninitialize()


def muteAndUnMute(process, value):
    pythoncom.CoInitialize()
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == process:
                if value == "Toggle":
                    value = 0 if volume.GetMute() == 1 else 1
                elif value == "Mute":
                    value = 1
                elif value == "Unmute":
                    value = 0
                volume.SetMute(value, None)
    finally:
        pythoncom.CoUninitialize()


def volumeChanger(process, action, value):
    if process == "Master Volume":
        if action == "Set":
            setMasterVolume(value)
        else:
            if action == "Increase":
                value = int(value)
            else:
                value = -int(value)
            master_vol = getMasterVolume() + value
            setMasterVolume(min(100, max(0, master_vol)))
    elif action == "Set":
        AudioController(str(process)).set_volume((int(value) * 0.01))
    elif action == "Increase":
        AudioController(str(process)).increase_volume((int(value) * 0.01))
    elif action == "Decrease":
        AudioController(str(process)).decrease_volume((int(value) * 0.01))


def setMasterVolume(Vol):
    pythoncom.CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        scalarVolume = int(Vol) / 100
        volume.SetMasterVolumeLevelScalar(scalarVolume, None)
    finally:
        pythoncom.CoUninitialize()


def getMasterVolume() -> int:
    pythoncom.CoInitialize()
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

        volume = interface.QueryInterface(IAudioEndpointVolume)
        return int(round(volume.GetMasterVolumeLevelScalar() * 100))
    finally:
        pythoncom.CoUninitialize()


def getDeviceObject(device_id, direction="Output"):
    deviceEnumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator,
            IMMDeviceEnumerator,
            comtypes.CLSCTX_INPROC_SERVER)
    
    if deviceEnumerator is None:
        return None

    flow = EDataFlow.eCapture.value
    if direction.lower() == "output":
        flow = EDataFlow.eRender.value

    devices = deviceEnumerator.EnumAudioEndpoints(flow, 1)

    for dev in devices:
        if dev.GetId() == device_id:
            return dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return None


def setDeviceVolume(device_id, direction, volume_level):
    pythoncom.CoInitialize()
    try:
        if device_id == "default":
            if direction.lower() == "output":
                device = AudioUtilities.GetSpeakers()
            else:
                device = AudioUtilities.GetMicrophone()
            device_object = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        else:
            device_object = getDeviceObject(device_id, direction)

        if device_object:
            volume = cast(device_object, POINTER(IAudioEndpointVolume))
            scalar_volume = float(volume_level) / 100
            volume.SetMasterVolumeLevelScalar(scalar_volume, None)
    finally:
        pythoncom.CoUninitialize()


def get_process_id(name):
    pythoncom.CoInitialize()
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name() == name:
                return session.Process.pid
        return None
    finally:
        pythoncom.CoUninitialize()
