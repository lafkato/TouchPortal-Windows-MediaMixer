# TouchPortal-Windows-MediaMixer
a TouchPortal plugin that allows you to control Window's default audio mixer.

- [TouchPortal-Windows-MediaMixer](#touchportal-windows-mediamixer)
- [Change Log](#change-log)
- [What is this?](#what-is-this)
- [Functionality](#functionality)
    - [Action](#action)
    - [State](#state)
- [Versioning](#versioning)
- [Lincense](#license)
- [Bugs/Echancements](#bugsenhancements)

# Change Log
```
v1.5.5 - CI compatibility fix (2026-06-01)
    CI / Packaging:
        - Pinned `pyee<12` in `requirements.txt` to ensure `TouchPortalAPI` imports `ExecutorEventEmitter` during GitHub Actions runs.

v1.5.4 - Release workflow: upload asset fix (2026-06-01)
    CI / Release:
        - Fixed GitHub Actions workflow to dynamically locate the generated `.tpp` and upload it as the release asset.
        - Added workflow permissions so the action can create releases.

v1.5.3 - Add GitHub Actions release automation (2026-06-01)
    CI:
        - Added `.github/workflows/release.yml` to build the plugin on tag push and create a GitHub Release with the built `.tpp`.

v1.5.2 - Build & runtime stability fixes (2026-06-01)
    Bug Fixes / Improvements:
        - Stabilized COM usage and threading in `TPAudioMixer.py` to prevent high CPU and plugin hangs.
        - Converted state updater thread to a daemon and reduced polling frequency to lower CPU usage.
        - Added robust COM init/uninit handling in `audioUtil/audioController.py` to prevent COM leaks and crashes.
        - Added error logging (`onError`) and clean shutdown handling (`onShutdown`).
        - Cached active window lookup to avoid redundant process queries.

v1.5.1 - Fixed listId not updating correctly
    Bug Fixes:
        - Fixed `listId` not updating for certain actions.

v1.5.0 - Fixed id and added ability to change audio volume
    Features:
        - Added action to change mic/speaker volume.

v1.0.0 - Initial Release (2022-05-26)
    Features:
        - Mute/Unmute/Toggle per application
        - Increase/Decrease/Set Master vol, current focused app or selected app

```

# What is this?
Have you ever wondering if theres a way to easily control Windows Volume Mixer without using third party software like voicemeter? You found the right place! Because this uses Windows buildin API which allows you to change individual Application volume in tip of finger!

# Functionality

## Action
![Action List](images/actions.png)

- Volume Mixer: Mute/Unmute process volume
    - This allows you to Toggle/Mute/Unmute any program you pick.
- Adjust App Volume
    - It allows you to Increase/Decrease/Set any application Volume
- Audio Output/Input Device Switcher
    - This allows you to change global default or communication audio device.
- Audio Output/Input Device Toggle
    - This allows you to toggle the default global audio or communication device between two choices.
- Set Device Volume
    - This allows you to set Micrphone or Speaker volume.
- Individual App Audio Device switcher
    - allows you to change app's volume source to a different audio device.

## State
![State list](images/states.png)
![Audio state](images/AudioDevice.png)

This plugin will create for each application
- appname.exe Mute state
   - This gives `Muted` or `Un-muted` depends on application
- is appname.exe Active
    - This gives `True` or `False` It will show `True` if application is playing sound
- appname.exe Volume
    - This shows this application's volume
- Audio Device: Get default Output devices
    - This shows your current Default output device
- Audio Device: Get default Output communication devices
    - This shows your Default output communication device
- Audio Device: Get default input device
    - This shows your default input device
- Audio Device: Get default input communication device
    - This shows your default input communication device
- Volume Mixer: current focused app
    - This gives you current focused app
- Volume Mixer: Get Current Master Volume
    - shows current master volume via states ranging 0-100
- Volume Mixer: focused app volume
    - shows current focused app volume as a state.

### Slider

This plugin also includes slider functionality. to use this feature simply change button type to `Slider` then you will have
- Volume Mixer: APP Volume slider
    - when button type is slider, you have ability to change selected app volume
     using slider also includes Current app (controls volume on whatever is on focus) and control master volume too! 

# Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the Releases section

# License

This project uses [GNU GPL v3.0](LICENSE)

# Bugs/Enhancements
Use the Github Issues tab to report any bugs/enhancements for this plug-in. Or mention them in the Official Touch Portal discord channel #win-mediamixer
