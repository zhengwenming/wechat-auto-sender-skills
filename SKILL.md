---
name: wechat-sender
description: This skill should be used whenever the user wants to send a WeChat message to a specific friend or group chat. It leverages an AppleScript automation to open WeChat, search for the target contact or group by name, and send a dynamic text message. Trigger phrases include "给XX发微信", "发消息给XX", "通知微信群XX", "send WeChat message to", or any similar instruction involving sending a WeChat message programmatically.
---

# WeChat Sender Skill

## Purpose

To automate sending WeChat messages to a specific friend or group chat using an AppleScript wrapper. The script controls the WeChat desktop app via macOS System Events, searches for the target by name, and sends the provided message text.

## Requirements

- macOS with WeChat desktop app installed and logged in
- macOS Accessibility permissions granted to the terminal/agent running the script
- The bundled script is located at: `scripts/wechat.applescript`

## Usage

To send a message, execute the following command:

```bash
osascript ~/.workbuddy/skills/wechat-sender/scripts/wechat.applescript "<联系人或群名>" "<消息内容>"
```

**Parameters:**
1. First argument — the exact name of the WeChat contact or group (e.g., `"技术交流群"` or `"张三"`)
2. Second argument — the message text to send (supports dynamic/variable content)

**Example:**

```bash
osascript ~/.workbuddy/skills/wechat-sender/scripts/wechat.applescript "产品讨论群" "今天下午3点开会，请准时参加"
```

## How It Works

1. Activate the WeChat application and wait for it to load
2. Use double Command key press to open the WeChat search bar
3. Type the target contact/group name and press Return to open the conversation
4. Paste the message text (via clipboard) and press Return to send

## Important Notes

- The script uses `delay` timers to account for UI loading. If the machine is slow, increase the delay values in the script.
- The script uses clipboard to paste messages (to support Chinese and special characters). The user's clipboard will be temporarily overwritten.
- If WeChat is already open and the chat window is in focus, the script still works correctly.
- Always use the **exact name** as it appears in WeChat for reliable search results.

## Workflow

When the user asks to send a WeChat message:

1. Extract the target name and message content from the user's request
2. Run the osascript command above with the extracted values
3. Confirm to the user that the message was sent (or report any errors)
