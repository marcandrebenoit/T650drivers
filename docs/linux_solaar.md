# Linux Gesture Implementation (Solaar Method)

On Linux, the most stable way to implement 3+ finger gestures without writing custom background drivers is by using the **Solaar Rule Editor**.
This method leverages the HID++ notifications the T650 sends once it is in "Raw Mode."

## Prerequisites
- **Solaar** installed (`sudo apt install solaar`).
- T650 must be in "Advanced" mode (Unlock Key A must have been sent).

## Step-by-Step Rule Setup (see all steps images in folder)
1. Open the **Solaar Rule Editor**.
2. Create a new **User-defined rule**.
3. **Condition:** Add a `Feature` condition  and select `TOUCHPAD RAW XY` or just copy and paste it if you don't see it in the list. (6100) might be added after the command,this is a non-issue.
4. **Bit Test (Test Bytes):** - This targets the "Contact Mask" byte to detect multiple fingers.
   - **Begin (inclusive):** `0`
   - **End (exclusive):** `1`
   - **Type:** `mask`
   - **Mask:** `4` (This bit represents the 3rd finger).
5. **Action:** Add a `Key press` action.
   - **Key:** `Super_L` (or your preferred shortcut).
   - **Type:** `click` (**CRITICAL:** Do not use 'press' or 'depress' as it will jam the key in the 'down' position).

## Why this works
Once the T650 is unlocked, it broadcasts its touch state via HID++ notifications.
Bit 2 (Value 4) of the first data byte is the indicator for the 3rd finger.
Solaar intercepts this bit and triggers a virtual keyboard event.
