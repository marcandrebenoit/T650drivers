# 2026-10-25 Code Review Findings

Static review of all scripts in `tools/`, `drivers/linux/` and the protocol docs.
No hardware was available, so nothing here was verified on a device.
None of these findings have been fixed yet.

Suggested priority: #1, #2/#3, #6.

## Bugs

### 1. Y coordinate shift is wrong (`<< 8` should be `<< 4`)
- `tools/finger_diagnostic.py:32` and the snippet in `docs/PROTOCOL_ANALYSIS.md` (`parse_12bit`).
- Current: `y = (data[offset+1] >> 4) | (data[offset+2] << 8)`
- Per the packing table in `PROTOCOL_ANALYSIS.md`, Y = 4 bits from byte 1 (high nibble) + 8 bits from byte 2.
  The nibble fills Y bits 0-3, so byte 2 must start at bit 4: `(data[offset+2] << 4)`.
- X is correct (`<< 8`) because its first piece is a full byte; Y's first piece is a nibble.
  The `<< 8` looks copied from the X line.
- Example: b1=0xA5, b2=0x3C -> `<< 4` gives 0x3CA (970); `<< 8` gives 0x3C0A (15370, > 4095, bits 4-7 always 0).
- Git history: introduced in the initial commit (`2bda8a3`); no commit explains it.
- Discussed with the maintainer: the Solaar rule (mask 4 on byte 0) only tests the contact
  mask and never reads coordinate bytes, so it does not depend on this shift.
- Hardware check: slide one finger slowly top-to-bottom. With `<< 8`, Y jumps in steps of 256 and exceeds 4095.

### 2. `tools/discovery.py` uses Root.GetFeature incorrectly
- Lines 27-33 send `[0x11, idx, 0x00, 0x00, i, 0, ...]`, i.e. GetFeature for feature ID `i << 8`,
  then read reply bytes 4-5 as a feature ID. Reply byte 4 is actually the feature *index*, byte 5 the type.
- Fix: send GetFeature with params `0x61, 0x00` and read `res[4]` as the index of 0x6100.
  (To enumerate all features, use IFeatureSet 0x0001 function 1 instead.)
- Also: comment says 0x00-0x20, loop is 0x01-0x24; software ID 0 makes replies indistinguishable from notifications.

### 3. Hard-coded feature index `0x10` and device index `1`
- Feature index is per device/firmware; device index depends on receiver pairing slot.
- After fixing #2, `unlock_t650.py` should resolve the index for 0x6100 at runtime.

### 4. `tools/unlock_t650.py` reports errors as success
- An HID++ error reply (`11 01 FF 10 21 <err>`) has `res[3] == 0x10`, so it falls into the
  "no confirmation" branch which returns `True`.
- Check `res[2] == MT_IDX and res[3] == 0x21`; treat `res[2] == 0xFF` as failure.
- `finally: h.close()` raises NameError if `hid.device()` itself fails.

### 5. Windows scripts crash with UnboundLocalError when the device is missing
- `t650_cursor.py`, `t650_decoder.py`, `t650_gesture_driver.py`, `persistence.py`:
  `finally: device.close()` runs when `next(...)` raised StopIteration before `device` was assigned.
  This also masks the friendly message in `t650_decoder.py:35-40`. Init `device = None` and guard.

### 6. Heartbeat replies are parsed as touch data
- Windows loops accept any `report[0] == 0x11`. The reply to the `11 01 00 00 ...` ping has
  `report[4] == 0`, read as "0 fingers", which resets `is_gesturing`.
- `t650_gesture_driver.py:22` pings every loop (~200 Hz) and the drain-to-latest logic usually
  ends on a ping reply, so gestures will rarely fire.
- `t650_production.py` cancels an in-progress gesture every 3 s.
- Fix: filter on `report[2] == <touch feature index>`; use a non-zero software ID in the ping.

### 7. `tools/windows/persistence.py:16` writes a 7-byte long report
- Report 0x11 must be 20 bytes; Windows hidapi rejects wrong-length writes.

## Inconsistencies to verify

- Linux vs Windows decoders disagree:
  - Linux: byte 4 = per-finger bitmask, bytes 5-7 = packed 12-bit X/Y.
  - Windows: `byte4 & 0x0F` = finger count, `(b5<<8)|b6` = 16-bit X;
    `t650_gesture_driver.py:35` decodes the same bytes as Y.
  - If byte 4 is a bitmask, Windows `fingers == 3` matches F1+F2 (0b011) = two fingers.
    (The Windows branch may run without the unlock, so the format may differ; capture packets to confirm.)
- `t650_initialize.py:20` comments index 0x01 as "Root"; Root is 0x00. The packet is a
  feature-count query, not a raw-mode enable.
- `t650_force_wake.py` uses a different "raw mode" packet (`01 10 01`) than the Linux unlock (`10 21 02`).
- Heartbeat is commented "Get Protocol Version", but `00 00` is GetFeature(0x0000);
  GetProtocolVersion is function 1 (`00 1x`). Harmless, but misleading.

## Resolved during review (not issues)

- Solaar rule `drivers/linux/rules.yaml` `TestBytes: [0x0, 0x1, 0x4]` is the **mask** form
  (bit test of byte 0 = contact mask, since Solaar strips the 4-byte HID++ header), matching
  the rule-editor screenshots in `docs/linux_solaar.Step-by-Step.*.png`. Not an exact compare.

## Minor

- `finger_diagnostic.py`: no check for missing device (`open_path(None)`); handle never closed;
  accepts report 0x20 (DJ report, different layout); the unlock ack can be parsed once as touch data.
- `t650_production.py`: one read per 10 ms sleep can build a backlog if the pad reports >100 Hz
  (drain the buffer or use a blocking read with timeout); bare `except: pass` at line 32.
- udev rule (`drivers/linux/udev_rules.md:13`): matches every hidraw node of the receiver
  (including DJ children), so the script runs several times; may fire before the T650 is awake.
  Narrow to interface 2 (e.g. `ATTRS{bInterfaceNumber}=="02"`). `hidapi` must be installed for root's Python.
- README: says `/drivers` contains a `libevdev` driver (it only has a Solaar rule); `pynput` missing
  from prerequisites; no `requirements.txt`.
- VID/PID, device lookup and report construction are duplicated across all 12 scripts;
  a shared `tools/t650_common.py` would remove that.
