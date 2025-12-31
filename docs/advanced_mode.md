# Understanding Advanced (Raw) Mode

The Logitech T650 operates in two distinct states. By default, it identifies as a legacy mouse to ensure compatibility with all systems. To access multi-finger data, it must be toggled into its native "Advanced" state.

| Feature | **Standard "Mouse" Mode** (Default) | **"Advanced" Raw Mode** (Unlocked) |
| :--- | :--- | :--- |
| **Identity** | Standard HID Mouse | Multi-touch Digitizer / Precision Pad |
| **Processing** | Handled by Unifying Receiver | Handled by Host OS (Linux/Windows) |
| **Data Type** | Relative Pointer Deltas | Raw 12-bit Absolute Coordinates |
| **Reporting** | 1-2 Finger standard events | Up to 5-Finger raw data streams |
| **Gestures** | Hardcoded in firmware | Fully customizable via software |

---

## Why is an "Unlock" required?
In Standard Mode, the T650 does not broadcast touch coordinates to save bandwidth on the 2.4GHz wireless spectrum. When the "Unlock Key A" is sent, the device enables the `TOUCHPAD RAW XY (6100)` feature. 

Without this transition, **Solaar Rules** and **Custom Python Listeners** will receive zero data because the hardware is literally not sending it.

## The Unlock Key A Handshake
To activate Advanced Mode, the following HID++ 2.0 command must be sent to **Interface 2** of the Unifying Receiver:

**Command (Hex):** `11 01 10 21 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00`

### Byte Breakdown:
* `11`: Long HID++ Report.
* `01`: Device Index (The T650's position on the receiver).
* `10`: Feature Index (Multi-touch engine).
* `21`: Function ID (Set Mode).
* `02`: Mode Value (**02** for Raw/Advanced, **00** for Mouse).

---

## Persistence and udev
This mode is **volatile** in most cases.

If the T650 is turned off or the computer reboots, the device may revert to **00** "Mouse Mode."

To automate this, see `drivers/linux/udev_rules.md` to trigger the unlock script automatically on device detection.



## Technical Note the Unifying Receiver **Interface 2**
* Interface 2 is the standard "Advanced Functionality" port for the Logitech Unifying Receiver (USB ID 046d:c52b).
* The Logitech Unifying Receiver (C-U0007/8) is a composite device.
* Interface 2 is the dedicated HID++ protocol channel.
* All raw touch coordinates and mode-switching commands must be sent through this interface.
* On some custom setups or different receivers (like the newer Logi Bolt), this index might differ, but for the standard Unifying Receiver, it is consistently 2.

### Is Interface 2 universal?
For the Logitech Unifying Receiver usb dongle speicifically, the answer is yes,but it might differ on the Logi Bolt for example  .

When you plug this specific receiver into any computer, it presents itself as a single physical USB device that contains three logical interfaces:
* Interface 0: Standard Keyboard emulation (so the BIOS/OS can see a basic keyboard).
* Interface 1: Standard Mouse emulation (for basic cursor movement).
* Interface 2: The HID++ (Vendor-Specific) interface. This is the "Data Pipe" used for pairing, battery status, and—most importantly for us—Advanced Raw Mode.

### Why this matters for all users
If a user tries to send the "Unlock Key" to Interface 0 or Interface 1, the receiver will simply ignore it because those interfaces only understand basic mouse/keyboard signals.

To "talk" to the T650's internal multi-touch engine, the software must specifically target **Interface 2**.

### How to verify this on any system
You can confirm this mapping by checking the device list in your terminal.

On Linux:
Run ``lsusb -v -d 046d:c52b | grep bInterfaceNumber`` and look for the bInterfaceNumber lines.

You will see 0, 1, and 2 (if interface 2 is present).
