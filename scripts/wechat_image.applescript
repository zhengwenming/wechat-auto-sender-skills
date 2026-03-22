-- 接收外部参数：第1个=联系人，第2个=发送内容（文字或图片路径），第3个=类型（text/image，可选，默认text）
on run argv
	set targetName to item 1 of argv
	set sendMsg to item 2 of argv
	
	tell application "WeChat"
		activate
		delay 5
	end tell
	
	-- 打开 Spotlight（全局快捷键，不在微信进程内）
	tell application "System Events"
		keystroke space using {command down}
	end tell
	
	delay 0.3
	
	-- 清空并搜索微信
	tell application "System Events"
		-- 全选删除
		keystroke "a" using {command down}
		delay 0.1
		keystroke (key code 51)
		delay 0.2
		
		-- 输入搜索
		keystroke "weixin"
		delay 0.3
		keystroke return
		delay 0.4
		keystroke return
		
		-- 搜索联系人
		delay 0.4
		keystroke "f" using {command down}
		delay 1
		set the clipboard to targetName
		keystroke "v" using {command down}
		delay 1
		keystroke return
		delay 2
		keystroke return
		
		-- 导航
		delay 0.3
		key code 125 using {option down}
		key code 126 using {option down}
		delay 0.3
		
		-- 发送消息
		set the clipboard to sendMsg
		keystroke "v" using {command down}
		delay 1
		keystroke return
		keystroke return
	end tell
end run
