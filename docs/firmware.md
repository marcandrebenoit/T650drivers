# Why Firmware 041.001.00038 is Required

The ability to use the T650 as a native multi-touch device on modern operating systems depends entirely on **Firmware version 041.001.00038** (commonly referred to as **Firmware 038**). 

Earlier versions of the firmware were designed for a different era of computing and do not expose the necessary HID++ features to the OS.

## The Firmware Evolution

| Firmware Version | Major Changes & Capabilities |
| :--- | :--- |
| **Pre-038** | Designed for Windows 7/8. All gestures are "baked" into the hardware. The device sends standard mouse/keyboard shortcuts (like `Alt+Tab`) rather than raw finger coordinates. |
| **Firmware 038** | **The "Unlock" Update.** Logitech shifted gesture processing from the hardware to the software. This update exposed the `TOUCHPAD RAW XY` feature, allowing host OSs to see 3, 4, and 5 fingers. |

## Why it fails on older firmware
If your T650 is running an older firmware (e.g., v033 or lower), the "Unlock Key A" command (`11 01 10 21 02`) will likely fail or return a **Feature Not Found** error. 

1. **Missing Feature Index:** Older firmwares do not have the Multi-touch Feature (ID `0x6100`) mapped to the command bus.
2. **Hardcoded Gestures:** On older firmware, the touchpad is hard-locked to emulate a mouse. It simply does not have the "vocabulary" to stream raw coordinates over the Unifying Receiver.
3. **Tap-to-Click:** Firmware 038 moved the "Tap-to-Click" logic onto the device itself, which is what allows it to work "out of the box" on Linux without extra drivers.

## How to check your version
You can check your current firmware version using **Solaar**:
1. Open Solaar.
2. Click on the **Wireless Rechargeable Touchpad T650**.
3. Look at the **Firmware** field. It should read `041.001.00038`.

## How to Update
Logitech does not provide a Linux-native firmware updater. To update to 038:
1. Connect your Unifying Receiver to a **Windows** machine.
2. Download the very specific (I've tried more recent versions and those didn't work) [Logitech SetPoint6.69.126_64.exe](https://fichiers.toutlesdrivers.com/61086/SetPoint6.69.126_64.exe) software from the reputable (IMHO) French site ToutLesDrivers.com (All The Drivers!). 
3. Earlier versions will not have the 038 firmware update, older versions will not let the firmware update to take place (in my personal experience)
4. See `SetpointDownloadDetails.png` to visually see the file that I got from them and its digital signature from Logitech (always validate this).
5. Install this version while making sure to uninstall any other versions newer or older prior to that. When installed do resist the temptation to install updates to this software.
6. Make sure that the T650 is recharged to full and **not plugged in** to the usb cable used to recharge the device otherwise a **Waiting for the device to finish charging** message will appear as you press the **update firmware** button
7. Ensure the T650 is paired and turned on and proceed to run the **Mouse and Keyboard Settings** software once installed.
8. When started SetPoint defaults to Tools Settings Information Resources the round I icon on top left. We need to click on the third icon (with the unify sun logo) Unify settings and Click on the Open Unifying Software button.
9. Look at the `SetPointUnifyingDetail01.png` `SetPointUnifyingDetail02.png` and `SetPointUnifyingDetail03.png` to see the steps visually before we continue.
10. Next we need to click on advanced, select TouchPad T650 from the list and apply the 038 patch by pressing the Update Firmware button.
11. It will ask to turn off and on the T650 and will display a **Do not Turn off** message while a tiny progress bar appears for a few seconds.
12. Then when process is complete! You should see the firmware updated to 041.001.00038 if not (only after the firmware complete message appears) turn off and on once more. Congrats!

> **Note:** Once updated to 038, the hardware changes are permanent and will carry over when you plug the receiver back into your Linux or Windows 10/11 machine.


## References used while researching how to update:
 A github gist by [David Ruhmann](https://github.com/davidruhmann) aptly named [Logitech T650 on Windows 10](https://gist.github.com/davidruhmann/9674f90794790ce419430ab3b45054b3) which helped me to narrow down the specific SetPoint version that would work to update the firmware,although the Logitech links have died since then,it gave me a good start researching how to successfully upgrade the firmware from 033 to 038!
 

