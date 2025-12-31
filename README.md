# Logitech T650 Multi-Touch Driver Project

This repository provides the research, diagnostic tools, and driver implementation required to unlock the full 5-finger multi-touch capabilities of the Logitech T650 Rechargeable Touchpad on modern operating systems (Linux and Windows 10/11).
> [!IMPORTANT]
> Your T650 needs to be at [firmware 041.001.00038 to use this](/docs/firmware.md#why-firmware-04100100038-is-required) anything earlier will not work. 


## 1. The Problem
By default, the T650 identifies as a "Generic HID Mouse" when connected via a Unifying Receiver. This legacy compatibility mode hides the high-resolution digitizer data, resulting in:
* **No Touchpad Settings:** The OS does not recognize the device as a touchpad.
* **Limited Gestures:** Only 1-finger movement and 2-finger basic scrolling are available.
* **Low Precision:** Movement is restricted to standard mouse resolution rather than the native 12-bit digitizer precision.

## 2. The Solution: HID++ 2.0 Unlock
Our research into the HID++ 2.0 protocol (specifically **Firmware 038**) revealed that the device requires a specific "Unlock Key" to enable Raw Reporting Mode.

### Hardware Constants
- **VID:** `0x046D` (Logitech)
- **PID:** `0xC52B` (Unifying Receiver)
- **Interface:** 2 (HID++ Protocol Interface)
- **Feature Index:** `0x10` (Multi-touch Feature)
- **Unlock Sequence (Key A):** `11 01 10 21 02`



## 3. Repository Structure

| Folder | Description |
| :--- | :--- |
| `/tools` | Diagnostic scripts to verify 5-finger coordinate data. |
| `/drivers` | User-space driver implementations (Linux `libevdev`). |
| `/docs` | Technical documentation of the 12-bit bit-packing and protocol. |

## 4. Getting Started

### Prerequisites
You must have Python 3.10+ installed along with the `hidapi` library:
```bash
pip install hidapi
```
### Verification
To confirm your hardware is communicating correctly, run the diagnostic tool:

```bash
sudo python3 tools/finger_diagnostic.py
```
If successful, you will see a live update of 5-finger coordinates (X, Y) and the active contact bitmask.

## 5. OS Implementation Status
### [Linux (Ubuntu 24.04+)](docs/linux_solaar.md) (work in progress,3 fingers click gesture working)
The T650 can be "tricked" into native mode. By sending the unlock command and power-cycling the device, the kernel re-enumerates it as a Precision Touchpad, enabling the native GNOME Touchpad settings panel.

### [Windows 10/11](docs/windows_setup.md) (work in progress,see windows-experimental branch) 
Work is ongoing to implement a user-space driver that translates raw HID++ packets into Windows Precision Touchpad (PTP) events or virtual keyboard/mouse shortcuts for gestures.

## 6. Known Issues & Troubleshooting
Kernel Locking: Sometimes the hid-logitech-dj driver prevents user-space scripts from writing to the device.

Reboot Persistence: The "Unlock" command is volatile and must be re-sent after a device power cycle or system reboot.
Use the provided [udev rules](drivers/linux/udev_rules.md) to automate this.

> [!IMPORTANT]
> This project is an independent research effort and is not affiliated with Logitech.
