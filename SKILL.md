---
name: wechat-sender
description: This skill should be used whenever the user wants to send a WeChat message to a specific friend or group chat. It leverages an AppleScript automation (macOS) or Python automation (Windows) to open WeChat, search for the target contact or group by name, and send a dynamic text message or image. Trigger phrases include "给XX发微信", "发消息给XX", "通知微信群XX", "send WeChat message to", or any similar instruction involving sending a WeChat message programmatically.
---

# WeChat Sender Skill

## Purpose

To automate sending WeChat messages or images to a specific friend or group chat. The skill supports both macOS (using AppleScript) and Windows (using Python UI automation). It controls the WeChat desktop app, searches for the target by name, and sends the provided message text or image.

## Requirements

### macOS
- macOS with WeChat desktop app installed and logged in
- macOS Accessibility permissions granted to the terminal/agent running the script
- The bundled scripts are located at: `scripts/wechat.applescript` and `scripts/wechat_image.applescript`

### Windows
- Windows with WeChat desktop app installed and logged in
- Python 3.x installed
- Required Python packages: `pip install pyautogui pyperclip uiautomation pillow pywin32`
- The bundled scripts are located at: `scripts/wechat.py` and `scripts/wechat_image.py`

## Usage

### 1. Send Text Message

**macOS:**
```bash
osascript ~/.workbuddy/skills/wechat-sender/scripts/wechat.applescript "<联系人或群名>" "<消息内容>"
```

**Windows:**
```powershell
python ~/.workbuddy/skills/wechat-sender/scripts/wechat.py -c "<联系人或群名>" -t "<消息内容>"
```

**Parameters:**
1. Target Name — the exact name of the WeChat contact or group (e.g., `"技术交流群"` or `"张三"`)
2. Message Text — the message text to send (supports dynamic/variable content)

### 2. Send Image

**macOS:**
```bash
osascript ~/.workbuddy/skills/wechat-sender/scripts/wechat_image.applescript "<联系人或群名>" "<图片绝对路径>"
```

**Windows:**
```powershell
python ~/.workbuddy/skills/wechat-sender/scripts/wechat_image.py -c "<联系人或群名>" -i "<图片绝对路径>"
```

**Parameters:**
1. Target Name — the exact name of the WeChat contact or group
2. Image Path — the absolute path to the image file to be sent

## How It Works

1. **macOS**: Activates the WeChat application via AppleScript, uses double Command key press to open the WeChat search bar.
2. **Windows**: Activates WeChat via `uiautomation` and `pyautogui`, uses `Ctrl + F` to open the search bar.
3. Types/pastes the target contact/group name and presses Return to open the conversation.
4. Pastes the message text or image (via clipboard) and presses Return to send.

## Important Notes

- The scripts use `delay` (macOS) or `time.sleep` (Windows) timers to account for UI loading.
- The scripts use clipboard to paste messages (to support Chinese, special characters, and images). The user's clipboard will be temporarily overwritten.
- If WeChat is already open and the chat window is in focus, the scripts still work correctly.
- Always use the **exact name** as it appears in WeChat for reliable search results.
- **Windows Only**: Make sure WeChat is not minimized to tray without a window handle, or the hotkey `Ctrl+Alt+W` must be enabled to wake it up.

## Workflow

When the user asks to send a WeChat message or image:

1. Identify the user's operating system (macOS or Windows).
2. Extract the target name and message content/image path from the user's request.
3. Run the appropriate command for the detected OS with the extracted values.
4. Confirm to the user that the message or image was sent (or report any errors).
