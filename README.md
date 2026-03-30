# WeChat Auto Sender Skills 🤖

一个用于自动发送微信消息的 OpenClaw Skill。支持 macOS（通过 AppleScript）和 Windows（通过 Python UI 自动化）系统，可以自动化控制微信桌面应用，向好友或群聊发送消息和图片。

## 功能特点

- ✅ 自动搜索并打开指定联系人/群聊
- ✅ 支持发送文本消息（支持中文和特殊字符）
- ✅ 支持发送图片（PNG、JPG 等格式）
- ✅ 跨平台支持：同时支持 macOS 和 Windows
- ✅ 完全自动化，无需手动操作
- ✅ 适用于 OpenClaw 智能助理系统

## 系统要求

### macOS
- **操作系统**: macOS
- **应用**: 微信桌面版 (WeChat for Mac)
- **权限**: 需要授予终端/代理 **辅助功能权限**

### Windows
- **操作系统**: Windows 10/11
- **应用**: 微信桌面版 (WeChat for Windows)
- **环境**: Python 3.x
- **依赖**: 需要安装 Python 依赖库 `pip install pyautogui pyperclip uiautomation pillow pywin32`

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/wenming/wechat-auto-sender-skills.git
cd wechat-auto-sender-skills
```

### 2. 配置权限与依赖

**macOS:**
1. 打开 **系统设置** → **隐私与安全性** → **辅助功能**
2. 找到你的终端应用（或 OpenClaw 使用的终端）
3. 勾选允许（如果列表中找不到，点击 `+` 号添加终端应用）

**Windows:**
```powershell
pip install pyautogui pyperclip uiautomation pillow pywin32
```

### 3. 在 OpenClaw 中使用

将此 skill 复制到 OpenClaw 的 skills 目录：

```bash
cp -r wechat-auto-sender-skills /usr/local/lib/node_modules/openclaw/skills/
```

## 使用方法

### 发送文本消息

**macOS:**
```bash
osascript scripts/wechat.applescript "<联系人或群名>" "<消息内容>"
```

**Windows:**
```powershell
python scripts/wechat.py -c "<联系人或群名>" -t "<消息内容>"
```

**示例：**

```bash
# macOS 发送给个人
osascript scripts/wechat.applescript "张三" "你好，明天开会吗？"

# Windows 发送给群聊
python scripts/wechat.py -c "产品讨论群" -t "今天下午 3 点开会，请准时参加"
```

### 发送图片

**macOS:**
```bash
osascript scripts/wechat_image.applescript "<联系人或群名>" "<图片绝对路径>"
```

**Windows:**
```powershell
python scripts/wechat_image.py -c "<联系人或群名>" -i "<图片绝对路径>"
```

**示例：**

```bash
# macOS 发送 PNG 图片
osascript scripts/wechat_image.applescript "技术交流群" "/Users/wenming/Desktop/chart.png"

# Windows 发送 JPG 图片
python scripts/wechat_image.py -c "张三" -i "D:\Photos\photo.jpg"
```

### 在 OpenClaw 中使用

当用户说类似以下的话时，OpenClaw 会自动使用此技能：

- "给张三发微信：明天开会"
- "发消息给产品讨论群：下午 3 点开会"
- "通知微信群'技术交流群'：新功能上线了"
- "send WeChat message to John: meeting tomorrow"

## 工作原理

### 文本消息发送流程

1. **激活微信** - 打开微信应用并等待加载（macOS 使用 AppleScript，Windows 使用 `uiautomation`）
2. **打开搜索** - 打开微信搜索栏（macOS: `Command + 空格`，Windows: `Ctrl + F`）
3. **搜索联系人** - 输入联系人/群聊名称并打开对话
4. **发送消息** - 通过剪贴板粘贴消息内容并发送（macOS: `Command + V`，Windows: `Ctrl + V`）

### 图片消息发送流程

1. **验证图片** - 检查图片文件是否存在
2. **激活微信** - 打开微信应用并等待加载
3. **搜索联系人** - 输入联系人/群聊名称并打开对话
4. **复制图片** - 将图片写入系统剪贴板
5. **发送图片** - 粘贴并发送图片

## 注意事项

⚠️ **重要提示**：

- 脚本使用剪贴板来粘贴消息（支持中文和特殊字符），**剪贴板内容会被临时覆盖**
- 请使用**微信中显示的准确名称**，以确保搜索结果准确
- 如果电脑较慢，可能需要调整脚本中的延迟等待时间
- 微信必须保持登录状态
- **Windows 用户**：如果微信最小化到系统托盘，请确保开启了 `Ctrl+Alt+W` 全局唤醒快捷键

## 文件结构

```
wechat-auto-sender-skills/
├── README.md                   # 本文件
├── LICENSE                     # MIT 许可证
├── SKILL.md                    # OpenClaw Skill 定义
├── scripts/
│   ├── wechat.applescript      # macOS 文本消息发送脚本
│   ├── wechat_image.applescript # macOS 图片消息发送脚本
│   ├── wechat.py               # Windows 文本消息发送脚本
│   └── wechat_image.py         # Windows 图片消息发送脚本
├── assets/                     # 资源文件（可选）
└── references/                 # 参考资料（可选）
```

## 故障排除

### 问题：提示"不允许发送按键" (macOS)

**解决**：确保已授予终端/代理辅助功能权限。

### 问题：找不到联系人/群聊

**解决**：
- 检查名称是否与微信中显示的完全一致
- 确保微信已登录且该联系人/群聊存在
- 尝试使用微信搜索功能手动验证名称

### 问题：消息发送失败

**解决**：
- 确保微信窗口未被最小化（Windows 需要注意托盘状态）
- 检查网络连接
- 增加脚本中的 `delay` 或 `time.sleep` 值（如果电脑较慢）

## 开发说明

此技能通过控制微信 UI 自动化实现。
- **macOS**: 使用 AppleScript 通过 macOS System Events 模拟操作。
- **Windows**: 使用 Python 的 `uiautomation` 获取控件句柄，结合 `pyautogui` 和剪贴板操作实现。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [AgentSkills 规范](https://docs.openclaw.ai/skills/overview)

---

**注意**: 本项目仅供学习和自动化研究使用。请遵守微信使用条款，不要用于发送垃圾消息或滥用自动化功能。
