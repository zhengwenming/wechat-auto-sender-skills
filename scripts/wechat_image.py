import os
import pyautogui
import time
import argparse
import pyperclip
import sys
import re
import uiautomation as auto
from io import BytesIO
from PIL import Image
import win32clipboard

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def _normalize_text(text):
    return "".join((text or "").split())

def _coarse_text(text):
    return "".join(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]+', text or ""))

def _is_blocked_result_name(name):
    blocked_keywords = ("搜一搜", "网络", "小程序", "公众号")
    return any(keyword in (name or "") for keyword in blocked_keywords)

def _rect_value(rect, field):
    value = getattr(rect, field, None)
    if callable(value):
        return value()
    return value

def _get_active_window_title():
    getter = getattr(pyautogui, "getActiveWindowTitle", None)
    return (getter() if callable(getter) else "") or ""

def _is_browser_window(title):
    browser_keywords = ("edge", "chrome", "firefox", "safari", "浏览器", "webview", "网页")
    low = (title or "").lower()
    return any(k in low for k in browser_keywords)

def _is_wrong_result_window():
    title = _get_active_window_title()
    if _is_browser_window(title):
        return True, title
    try:
        foreground = auto.GetForegroundControl()
        top = foreground.GetTopLevelControl() if foreground and hasattr(foreground, "GetTopLevelControl") else foreground
        if not top:
            return False, title
        top_name = (getattr(top, "Name", "") or "")
        class_name = (getattr(top, "ClassName", "") or "").lower()
        if any(k in class_name for k in ("webview", "chrome", "cef", "edge")):
            return True, top_name or title
        inspect_text = (top_name + " " + title).lower()
        if "网页由微信提供" in inspect_text or "在浏览器中打开" in inspect_text or "复制链接" in inspect_text:
            return True, top_name or title
    except Exception:
        pass
    return False, title

def _is_selected_control(control):
    try:
        return bool(getattr(control, "IsSelected", False))
    except Exception:
        return False

def _try_enter_selected_target(contact):
    target_norm = _normalize_text(contact)
    target_coarse = _coarse_text(contact)
    focused = auto.GetFocusedControl()
    focused_name = (focused.Name if focused else "") or ""
    focused_norm = _normalize_text(focused_name)
    focused_coarse = _coarse_text(focused_name)
    if (target_norm and target_norm in focused_norm) or (target_coarse and target_coarse in focused_coarse):
        pyautogui.press('enter')
        print(f"检测到焦点已是目标联系人，直接回车: {focused_name}")
        return True
    hwnd = auto.GetForegroundWindow()
    wechat_win = auto.ControlFromHandle(hwnd) if hwnd else None
    if not wechat_win:
        return False
    selected_candidates = []
    pid = wechat_win.ProcessId
    try:
        for win in auto.GetRootControl().GetChildren():
            class_name = (win.ClassName or "")
            is_wechat_related = (
                win.ProcessId == pid or
                "WeChat" in class_name or
                "Qt" in class_name or
                "DropShadow" in class_name or
                "TXGui" in class_name
            )
            if not is_wechat_related:
                continue
            for control, _ in auto.WalkTree(win, includeTop=True, maxDepth=30):
                name = (control.Name or "")
                if not name or _is_blocked_result_name(name):
                    continue
                if getattr(control, "ControlType", None) == auto.ControlType.EditControl:
                    continue
                if not _is_selected_control(control):
                    continue
                name_norm = _normalize_text(name)
                name_coarse = _coarse_text(name)
                if (target_norm and target_norm not in name_norm) and (target_coarse and target_coarse not in name_coarse) and (contact not in name):
                    continue
                score = 0
                if name_norm == target_norm:
                    score += 100
                elif target_norm and target_norm in name_norm:
                    score += 60
                if target_coarse and name_coarse == target_coarse:
                    score += 80
                elif target_coarse and target_coarse in name_coarse:
                    score += 30
                selected_candidates.append((score, control))
    except Exception:
        return False
    if not selected_candidates:
        return False
    selected_candidates.sort(key=lambda t: t[0])
    target_control = selected_candidates[-1][1]
    try:
        target_control.SetFocus()
    except Exception:
        pass
    pyautogui.press('enter')
    print(f"检测到已选中目标联系人，直接回车: {target_control.Name}")
    return True

def _try_click_contact_by_ui(contact, enable_sampling_strategy=False):
    clicked_by_ui = False
    hwnd = auto.GetForegroundWindow()
    wechat_win = auto.ControlFromHandle(hwnd) if hwnd else None
    target_norm = _normalize_text(contact)
    target_coarse = _coarse_text(contact)
    matched_items = []
    if wechat_win:
        pid = wechat_win.ProcessId
        try:
            for win in auto.GetRootControl().GetChildren():
                class_name = (win.ClassName or "")
                is_wechat_related = (
                    win.ProcessId == pid or
                    "WeChat" in class_name or
                    "Qt" in class_name or
                    "DropShadow" in class_name or
                    "TXGui" in class_name
                )
                if not is_wechat_related:
                    continue
                for control, _ in auto.WalkTree(win, includeTop=True, maxDepth=30):
                    name = control.Name or ""
                    if not name:
                        continue
                    if _is_blocked_result_name(name):
                        continue
                    if getattr(control, "ControlType", None) == auto.ControlType.EditControl:
                        continue
                    name_norm = _normalize_text(name)
                    name_coarse = _coarse_text(name)
                    if (target_norm and target_norm in name_norm) or (target_coarse and target_coarse in name_coarse) or (contact in name):
                        matched_items.append(control)
        except Exception as e:
            print(f"UI遍历匹配失败: {e}")
    if matched_items:
        candidates = []
        for item in matched_items:
            item_name = item.Name or ""
            item_norm = _normalize_text(item_name)
            item_coarse = _coarse_text(item_name)
            score = 0
            if item_norm == target_norm:
                score += 100
            elif target_norm and target_norm in item_norm:
                score += 60
            if item_coarse == target_coarse and target_coarse:
                score += 80
            elif target_coarse and target_coarse in item_coarse:
                score += 40
            try:
                rect = item.BoundingRectangle
                width = _rect_value(rect, 'width') or 0
                height = _rect_value(rect, 'height') or 0
                y_center = _rect_value(rect, 'ycenter') if (width > 0 and height > 0) else -1
            except Exception:
                y_center = -1
            candidates.append((score, y_center, item))
        candidates.sort(key=lambda t: (t[0], t[1]))
        target_item = candidates[-1][2]
        try:
            rect = target_item.BoundingRectangle
            width = _rect_value(rect, 'width') or 0
            height = _rect_value(rect, 'height') or 0
            if width > 0 and height > 0:
                x_center = _rect_value(rect, 'xcenter')
                y_center = _rect_value(rect, 'ycenter')
                pyautogui.click(int(x_center), int(y_center))
                clicked_by_ui = True
                print(f"已通过坐标点击命中联系人: {target_item.Name}")
            else:
                target_item.Click(simulateMove=False)
                clicked_by_ui = True
                print(f"已通过UI点击命中联系人: {target_item.Name}")
        except Exception as e:
            print(f"点击匹配联系人失败: {e}")
    if clicked_by_ui or (not enable_sampling_strategy):
        return clicked_by_ui
    try:
        focused = auto.GetFocusedControl()
        rect = focused.BoundingRectangle if focused else None
        width = (_rect_value(rect, 'width') or 0) if rect else 0
        height = (_rect_value(rect, 'height') or 0) if rect else 0
        if not rect or width <= 0 or height <= 0:
            return False
        left = int(_rect_value(rect, 'left') or 0)
        right = int(_rect_value(rect, 'right') or 0)
        bottom = int(_rect_value(rect, 'bottom') or 0)
        x_positions = []
        x = left + 40
        end_x = right - 20
        while x <= end_x:
            x_positions.append(x)
            x += 80
        if not x_positions:
            x_positions = [int(_rect_value(rect, 'xcenter') or ((left + right) // 2))]
        candidates = []
        for y in range(bottom + 24, bottom + 360, 22):
            for px in x_positions:
                try:
                    c = auto.ControlFromPoint(px, y)
                except Exception:
                    continue
                probe = c
                chosen = None
                for _ in range(7):
                    if not probe:
                        break
                    nm = probe.Name or ""
                    nm_norm = _normalize_text(nm)
                    nm_coarse = _coarse_text(nm)
                    if _is_blocked_result_name(nm):
                        probe = probe.GetParentControl()
                        continue
                    if (target_norm and target_norm in nm_norm) or (target_coarse and target_coarse in nm_coarse) or (contact in nm):
                        chosen = probe
                        break
                    probe = probe.GetParentControl()
                if chosen:
                    candidates.append((y, px, chosen))
        if not candidates:
            return False
        candidates.sort(key=lambda t: t[0])
        y, x, chosen = candidates[-1]
        pyautogui.click(x, y)
        print(f"已通过坐标采样点击命中联系人: {chosen.Name}")
        return True
    except Exception as e:
        print(f"坐标采样匹配失败: {e}")
        return False

def _send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
    finally:
        win32clipboard.CloseClipboard()

def _copy_image_to_clipboard(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片不存在: {image_path}")
    image = Image.open(image_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    _send_to_clipboard(win32clipboard.CF_DIB, data)

def send_wechat_image(contact, image_path):
    active_title = _get_active_window_title()
    if "微信" not in active_title:
        pyautogui.hotkey('ctrl', 'alt', 'w')
        time.sleep(2)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyperclip.copy(contact)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)
    pyautogui.press('space')
    pyautogui.press('backspace')
    time.sleep(1.5)
    print(f"正在动态查找联系人/群聊: {contact} ...")
    focused_before = auto.GetFocusedControl()
    print(f"搜索后当前焦点: {(focused_before.Name if focused_before else '')}")
    clicked_by_ui = _try_click_contact_by_ui(contact, enable_sampling_strategy=False)
    if not clicked_by_ui:
        print("进入按键重试方案：检测浏览器误跳转后自动回退并增加下移次数。")
        retry_success = False
        max_retry = 6
        for down_count in range(0, max_retry + 1):
            active_title = _get_active_window_title()
            if "微信" not in active_title:
                pyautogui.hotkey('ctrl', 'alt', 'w')
                time.sleep(1.2)
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyperclip.copy(contact)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            pyautogui.press('space')
            pyautogui.press('backspace')
            time.sleep(1.0)
            entered_by_selected = _try_enter_selected_target(contact)
            if not entered_by_selected:
                if down_count == 0:
                    print("按键重试第0次：优先直接回车尝试默认选中项。")
                else:
                    print(f"按键重试第{down_count}次：下移{down_count}次后回车。")
                    for _ in range(down_count):
                        pyautogui.press('down')
                        time.sleep(0.15)
                pyautogui.press('enter')
            time.sleep(1.2)
            wrong_window, wrong_title = _is_wrong_result_window()
            if wrong_window:
                print(f"检测到误跳转窗口: {wrong_title}，回退并继续重试。")
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(0.6)
                wrong_window, _ = _is_wrong_result_window()
                if wrong_window:
                    pyautogui.hotkey('ctrl', 'w')
                    time.sleep(0.6)
                for _ in range(2):
                    if "微信" in _get_active_window_title():
                        break
                    pyautogui.hotkey('ctrl', 'alt', 'w')
                    time.sleep(0.8)
                continue
            active_title_after_enter = _get_active_window_title()
            if "微信" in active_title_after_enter:
                retry_success = True
                print(f"按键重试成功，当前窗口: {active_title_after_enter}")
                break
            print(f"未检测到误跳转，但当前不在微信窗口: {active_title_after_enter}，继续重试。")
            pyautogui.hotkey('ctrl', 'alt', 'w')
            time.sleep(0.8)
        if not retry_success:
            print("未能可靠命中目标联系人，已取消本次发送以避免误发。")
            return
    time.sleep(2)
    _copy_image_to_clipboard(image_path)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)
    pyautogui.press('enter')
    time.sleep(1)
    time.sleep(1)
    pyautogui.press('esc')

def main():
    parser = argparse.ArgumentParser(description="微信自动发送图片脚本")
    parser.add_argument('-c', '--contact', required=True, help="联系人名称（微信备注或昵称）")
    parser.add_argument('-i', '--image', required=True, help="要发送的图片路径（绝对路径）")
    args = parser.parse_args()
    print(f"即将发送图片给【{args.contact}】...")
    send_wechat_image(args.contact, args.image)
    print("发送完成！")

if __name__ == "__main__":
    main()
