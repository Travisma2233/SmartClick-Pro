import pyautogui
import time
import keyboard
import sys

class MouseAction:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def wait_for_key_release():
    """等待所有按键释放"""
    time.sleep(0.1)
    while keyboard.is_pressed('r') or keyboard.is_pressed('f') or keyboard.is_pressed('q') or keyboard.is_pressed('d') or keyboard.is_pressed('e'):
        time.sleep(0.1)

def show_actions(actions):
    """显示所有记录的点击位置"""
    print("\n当前记录的点击位置：")
    for i, action in enumerate(actions, 1):
        print(f"{i}. 位置: ({action.x}, {action.y})")

def record_clicks():
    """记录一系列鼠标点击位置"""
    print("\n=== 记录模式 ===")
    print("按 'r' 键：记录当前鼠标位置")
    print("按 'd' 键：删除最后一个记录的位置")
    print("按 'e' 键：编辑指定位置")
    print("按 'f' 键：完成记录")
    print("按 'q' 键：退出程序")
    
    actions = []
    while True:
        if keyboard.is_pressed('r'):
            x, y = pyautogui.position()
            actions.append(MouseAction(x, y))
            print(f"记录位置: ({x}, {y})")
            show_actions(actions)
            wait_for_key_release()
        
        elif keyboard.is_pressed('d'):
            if actions:
                removed = actions.pop()
                print(f"\n删除了最后一个位置: ({removed.x}, {removed.y})")
                show_actions(actions)
            else:
                print("\n没有可删除的位置")
            wait_for_key_release()
        
        elif keyboard.is_pressed('e'):
            wait_for_key_release()
            if not actions:
                print("\n没有可编辑的位置")
                continue
                
            show_actions(actions)
            try:
                index = get_valid_input("\n请输入要编辑的位置编号(1-{}): ".format(len(actions)), int, 1)
                if index > len(actions):
                    print("无效的编号")
                    continue
                    
                print("\n请将鼠标移动到新的位置，然后按 'r' 键确认")
                while True:
                    if keyboard.is_pressed('r'):
                        x, y = pyautogui.position()
                        actions[index-1] = MouseAction(x, y)
                        print(f"已更新位置 {index} 到: ({x}, {y})")
                        show_actions(actions)
                        wait_for_key_release()
                        break
                    elif keyboard.is_pressed('q'):
                        print("\n取消编辑")
                        wait_for_key_release()
                        break
            except ValueError:
                print("请输入有效的数字！")
        
        elif keyboard.is_pressed('f'):
            wait_for_key_release()
            break
            
        elif keyboard.is_pressed('q'):
            print("\n程序已终止")
            sys.exit()
    
    print(f"\n共记录了 {len(actions)} 个点击位置")
    return actions

def execute_actions(actions, repeat_times, delay_between_clicks=0.5):
    """执行记录的一系列点击操作"""
    for i in range(repeat_times):
        print(f"\n开始第 {i+1} 轮点击")
        for j, action in enumerate(actions, 1):
            if keyboard.is_pressed('q'):
                print("\n程序已终止")
                sys.exit()
            pyautogui.moveTo(action.x, action.y)
            pyautogui.click()
            print(f"完成第 {j} 个位置的点击: ({action.x}, {action.y})")
            time.sleep(delay_between_clicks)

def get_valid_input(prompt, input_type=int, min_value=None):
    """获取有效的用户输入"""
    while True:
        try:
            wait_for_key_release()
            value = input_type(input(prompt))
            if min_value is not None and value < min_value:
                print(f"输入值必须大于或等于 {min_value}")
                continue
            return value
        except ValueError:
            print("请输入有效的数字！")

def main():
    print("自动鼠标连续点击程序")
    print("==================")
    print("\n功能说明：")
    print("1. 记录模式下：")
    print("   - 按 'r' 键记录当前鼠标位置")
    print("   - 按 'd' 键删除最后一个记录的位置")
    print("   - 按 'e' 键编辑指定位置")
    print("   - 按 'f' 键完成记录")
    print("2. 随时按 'q' 键退出程序")
    
    input("\n准备好开始记录了吗？按回车键开始...")
    wait_for_key_release()
    
    # 记录点击位置
    actions = record_clicks()
    if not actions:
        print("没有记录任何点击位置！")
        return
    
    try:
        # 获取执行参数
        while True:
            try:
                repeat_times = int(input("\n请输入要重复执行的次数: "))
                if repeat_times >= 1:
                    break
                print("重复次数必须大于或等于1")
            except ValueError:
                print("请输入有效的数字！")
                
        delay_seconds = get_valid_input("请输入开始前的延迟秒数: ", int, 0)
        delay_between_clicks = get_valid_input("请输入每次点击之间的间隔秒数(建议不小于0.1): ", float, 0)
            
        print(f"\n程序将在 {delay_seconds} 秒后开始执行")
        print("按 'q' 键可以随时退出程序")
        
        # 倒计时
        for i in range(delay_seconds, 0, -1):
            if keyboard.is_pressed('q'):
                print("\n程序已终止")
                return
            print(f"还剩 {i} 秒...")
            time.sleep(1)
        
        # 执行点击序列
        execute_actions(actions, repeat_times, delay_between_clicks)
        print("\n所有操作已完成！")
        
    except KeyboardInterrupt:
        print("\n程序已终止")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True  # 将鼠标移动到屏幕左上角可以终止程序
    main() 