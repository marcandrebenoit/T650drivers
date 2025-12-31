# Automating the Unlock (udev Rules)

Since the T650 resets to "Mouse Mode" every time it is power-cycled or the system reboots, you can use a **udev rule** to automate the activation of Advanced Mode.

## 1. Create the Rule File
Create a new file in the udev directory:
`sudo nano /etc/udev/rules.d/99-t650.rules`

## 2. Add the Rule Logic
Paste the following line. Replace `/path/to/your/` with the actual absolute path to your script.

```bash
SUBSYSTEM=="hidraw", ATTRS{idVendor}=="046d", ATTRS{idProduct}=="c52b", RUN+="/usr/bin/python3 /path/to/your/tools/unlock_t650.py"
```
## 3. Reload udev
Tell the system to recognize the new rule:

```bash
sudo udevadm control --reload-rules

sudo udevadm trigger
```
### Why this works.
When the Unifying Receiver is plugged in (or detected at boot), the kernel identifies the Vendor and Product ID.

This rule triggers your Python script, which sends the "Key A" command to Interface 2 before you even touch the pad
