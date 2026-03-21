# WeChat Auto Sender Skills 🤖

一个用于自动发送微信消息的 OpenClaw Skill。通过 AppleScript 自动化控制微信桌面应用，支持向好友或群聊发送消息。

## 功能特点

- ✅ 自动搜索并打开指定联系人/群聊
- ✅ 支持发送文本消息（支持中文和特殊字符）
- ✅ 完全自动化，无需手动操作
- ✅ 适用于 OpenClaw 智能助理系统

## 系统要求

- **操作系统**: macOS
- **应用**: 微信桌面版 (WeChat for Mac)
- **权限**: 需要授予终端/代理 **辅助功能权限**
- **依赖**: OpenClaw

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/wenming/wechat-auto-sender-skills.git
cd wechat-auto-sender-skills
```

### 2. 授予辅助功能权限

1. 打开 **系统设置** → **隐私与安全性** → **辅助功能**
2. 找到你的终端应用（或 OpenClaw 使用的终端）
3. 勾选允许

如果列表中找不到，点击 `+` 号添加终端应用。

### 3. 在 OpenClaw 中使用

将此 skill 复制到 OpenClaw 的 skills 目录：

```bash
cp -r wechat-auto-sender-skills /usr/local/lib/node_modules/openclaw/skills/
```

## 使用方法

### 基本用法

```bash
osascript wechat.applescript "<联系人或群名>" "<消息内容>"
```

### 示例

```bash
# 发送给个人
osascript wechat.applescript "张三" "你好，明天开会吗？"

# 发送给群聊
osascript wechat.applescript "产品讨论群" "今天下午 3 点开会，请准时参加"

# 发送长消息
osascript wechat.applescript "技术交流群" "📢 通知：本周六下午 2 点在公司会议室举行技术分享会，主题是'AI  Agent 开发实践'，欢迎大家参加！"
```

### 在 OpenClaw 中使用

当用户说类似以下的话时，OpenClaw 会自动使用此技能：

- "给张三发微信：明天开会"
- "发消息给产品讨论群：下午 3 点开会"
- "通知微信群'技术交流群'：新功能上线了"
- "send WeChat message to John: meeting tomorrow"

## 工作原理

1. **激活微信** - 打开微信应用并等待加载
2. **打开搜索** - 使用 `Command + 空格` 打开微信搜索栏
3. **搜索联系人** - 输入联系人/群聊名称并打开对话
4. **发送消息** - 通过剪贴板粘贴消息内容并发送

## 注意事项

⚠️ **重要提示**：

- 脚本使用剪贴板来粘贴消息（支持中文和特殊字符），**剪贴板内容会被临时覆盖**
- 请使用**微信中显示的准确名称**，以确保搜索结果准确
- 如果电脑较慢，可能需要调整脚本中的 `delay` 值
- 微信必须保持登录状态

## 文件结构

```
wechat-auto-sender-skills/
├── README.md           # 本文件
├── SKILL.md            # OpenClaw Skill 定义
├── wechat.applescript  # AppleScript 自动化脚本
├── assets/             # 资源文件（可选）
└── references/         # 参考资料（可选）
```

## 故障排除

### 问题：提示"不允许发送按键"

**解决**：确保已授予终端/代理辅助功能权限。

### 问题：找不到联系人/群聊

**解决**：
- 检查名称是否与微信中显示的完全一致
- 确保微信已登录且该联系人/群聊存在
- 尝试使用微信搜索功能手动验证名称

### 问题：消息发送失败

**解决**：
- 确保微信窗口未被最小化
- 检查网络连接
- 增加脚本中的 `delay` 值（如果电脑较慢）

## 开发说明

此技能使用 AppleScript 通过 macOS System Events 控制微信 UI。脚本逻辑：

1. 激活微信应用
2. 使用 `Command + 空格` 打开搜索
3. 输入目标名称并回车
4. 使用 `Command + V` 粘贴消息
5. 回车发送

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
