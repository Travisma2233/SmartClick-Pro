import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
import keyboard
import sys
import threading
from datetime import datetime

class MouseAction:
    def __init__(self, x, y, click_type="single"):
        self.x = x
        self.y = y
        self.click_type = click_type

class Language:
    def __init__(self):
        self.current = 'zh'  # 默认中文
        self.texts = {
            'zh': {
                'title': "自动鼠标点击程序",
                'ready': "就绪",
                'recording': "正在记录 - 按F7记录位置",
                'control_panel': "控制面板",
                'start_record': "开始记录(F6)",
                'stop_record': "停止记录(F6)",
                'clear_all': "清除所有",
                'click_type': "点击类型",
                'single_click': "单击",
                'double_click': "双击",
                'settings': "参数设置",
                'repeat_times': "重复次数:",
                'delay_seconds': "延迟秒数:",
                'click_interval': "点击间隔(秒):",
                'recorded_positions': "记录的点击位置",
                'number': "序号",
                'x_coord': "X坐标",
                'y_coord': "Y坐标",
                'click_type_col': "点击类型",
                'time': "记录时间",
                'delete_selected': "删除选中",
                'edit_selected': "编辑选中",
                'start_execute': "开始执行(F8)",
                'stop_execute': "停止执行(F9)",
                'hotkey_title': "快捷键说明",
                'hotkey_text': """
F6: 开始/停止记录
F7: 记录当前位置
F8: 开始执行
F9: 停止执行
ESC: 退出程序
                """,
                'confirm_clear': "确定要清除所有记录的位置吗？",
                'warning': "警告",
                'select_to_delete': "请先选择要删除的项目",
                'confirm_delete': "确定要删除选中的位置吗？",
                'select_to_edit': "请先选择要编辑的项目",
                'one_at_time': "一次只能编辑一个位置",
                'move_mouse': "将鼠标移动到新位置，然后点击确定",
                'confirm': "确定",
                'cancel': "取消",
                'no_positions': "没有记录任何点击位置",
                'invalid_params': "请输入有效的参数值",
                'preparing': "准备开始 - {}秒后执行",
                'executing': "执行中 - 第{}/{}轮",
                'stopped': "已停止执行",
                'single_text': "单击",
                'double_text': "双击",
                'switch_lang': "Switch to English"
            },
            'en': {
                'title': "Auto Mouse Clicker",
                'ready': "Ready",
                'recording': "Recording - Press F7 to record position",
                'control_panel': "Control Panel",
                'start_record': "Start Record(F6)",
                'stop_record': "Stop Record(F6)",
                'clear_all': "Clear All",
                'click_type': "Click Type",
                'single_click': "Single Click",
                'double_click': "Double Click",
                'settings': "Settings",
                'repeat_times': "Repeat Times:",
                'delay_seconds': "Delay Seconds:",
                'click_interval': "Click Interval(s):",
                'recorded_positions': "Recorded Positions",
                'number': "No.",
                'x_coord': "X Coord",
                'y_coord': "Y Coord",
                'click_type_col': "Click Type",
                'time': "Time",
                'delete_selected': "Delete Selected",
                'edit_selected': "Edit Selected",
                'start_execute': "Start Execute(F8)",
                'stop_execute': "Stop Execute(F9)",
                'hotkey_title': "Hotkeys",
                'hotkey_text': """
F6: Start/Stop Recording
F7: Record Current Position
F8: Start Execution
F9: Stop Execution
ESC: Exit Program
                """,
                'confirm_clear': "Are you sure to clear all recorded positions?",
                'warning': "Warning",
                'select_to_delete': "Please select items to delete",
                'confirm_delete': "Are you sure to delete selected positions?",
                'select_to_edit': "Please select an item to edit",
                'one_at_time': "Can only edit one position at a time",
                'move_mouse': "Move mouse to new position, then click Confirm",
                'confirm': "Confirm",
                'cancel': "Cancel",
                'no_positions': "No positions recorded",
                'invalid_params': "Please enter valid parameters",
                'preparing': "Preparing - {} seconds to start",
                'executing': "Executing - Round {}/{}",
                'stopped': "Execution stopped",
                'single_text': "Single",
                'double_text': "Double",
                'switch_lang': "切换到中文"
            }
        }

    def get(self, key):
        return self.texts[self.current][key]

    def switch(self):
        self.current = 'en' if self.current == 'zh' else 'zh'

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.lang = Language()
        self.setup_gui()
        self.add_watermark()  # 添加水印
        
    def setup_gui(self):
        self.root.title(self.lang.get('title'))
        self.root.geometry("600x900")
        
        # 设置样式
        style = ttk.Style()
        style.configure("Action.TButton", padding=5, font=('微软雅黑', 10))
        style.configure("Record.TButton", padding=5, font=('微软雅黑', 10))
        
        self.actions = []
        self.is_recording = False
        self.is_running = False
        self.current_click_type = tk.StringVar(value="single")
        
        self.create_widgets()
        self.setup_keyboard_listener()

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 语言切换按钮
        self.lang_button = ttk.Button(main_frame, text=self.lang.get('switch_lang'), 
                                    command=self.switch_language, style="Action.TButton")
        self.lang_button.grid(row=0, column=0, columnspan=2, pady=5)
        
        # 状态显示
        self.status_var = tk.StringVar(value=self.lang.get('ready'))
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=('微软雅黑', 12, 'bold'))
        status_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # 记录控制按钮
        control_frame = ttk.LabelFrame(main_frame, text=self.lang.get('control_panel'), padding="5")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.record_button = ttk.Button(control_frame, text=self.lang.get('start_record'), 
                                      command=self.toggle_recording, style="Record.TButton")
        self.record_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.clear_button = ttk.Button(control_frame, text=self.lang.get('clear_all'), 
                                     command=self.clear_actions, style="Action.TButton")
        self.clear_button.grid(row=0, column=1, padx=5, pady=5)
        
        # 点击类型选择
        click_type_frame = ttk.LabelFrame(control_frame, text=self.lang.get('click_type'))
        click_type_frame.grid(row=0, column=2, padx=5, pady=5)
        
        self.single_radio = ttk.Radiobutton(click_type_frame, text=self.lang.get('single_click'), 
                                          variable=self.current_click_type, value="single")
        self.single_radio.grid(row=0, column=0, padx=5)
        
        self.double_radio = ttk.Radiobutton(click_type_frame, text=self.lang.get('double_click'), 
                                          variable=self.current_click_type, value="double")
        self.double_radio.grid(row=0, column=1, padx=5)
        
        # 参数设置
        settings_frame = ttk.LabelFrame(main_frame, text=self.lang.get('settings'), padding="5")
        settings_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.repeat_label = ttk.Label(settings_frame, text=self.lang.get('repeat_times'))
        self.repeat_label.grid(row=0, column=0, padx=5, pady=5)
        self.repeat_times = ttk.Entry(settings_frame, width=10)
        self.repeat_times.insert(0, "1")
        self.repeat_times.grid(row=0, column=1, padx=5, pady=5)
        
        self.delay_label = ttk.Label(settings_frame, text=self.lang.get('delay_seconds'))
        self.delay_label.grid(row=1, column=0, padx=5, pady=5)
        self.delay_seconds = ttk.Entry(settings_frame, width=10)
        self.delay_seconds.insert(0, "3")
        self.delay_seconds.grid(row=1, column=1, padx=5, pady=5)
        
        self.interval_label = ttk.Label(settings_frame, text=self.lang.get('click_interval'))
        self.interval_label.grid(row=2, column=0, padx=5, pady=5)
        self.click_interval = ttk.Entry(settings_frame, width=10)
        self.click_interval.insert(0, "0.5")
        self.click_interval.grid(row=2, column=1, padx=5, pady=5)
        
        # 记录列表
        list_frame = ttk.LabelFrame(main_frame, text=self.lang.get('recorded_positions'), padding="5")
        list_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建Treeview
        self.tree = ttk.Treeview(list_frame, columns=('序号', 'X坐标', 'Y坐标', '点击类型', '时间'), 
                                show='headings', height=10)
        self.update_tree_headers()
        
        self.tree.column('序号', width=50)
        self.tree.column('X坐标', width=80)
        self.tree.column('Y坐标', width=80)
        self.tree.column('点击类型', width=80)
        self.tree.column('时间', width=100)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 列表操作按钮
        list_button_frame = ttk.Frame(list_frame)
        list_button_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        self.delete_button = ttk.Button(list_button_frame, text=self.lang.get('delete_selected'), 
                                      command=self.delete_selected, style="Action.TButton")
        self.delete_button.grid(row=0, column=0, padx=5)
        
        self.edit_button = ttk.Button(list_button_frame, text=self.lang.get('edit_selected'), 
                                    command=self.edit_selected, style="Action.TButton")
        self.edit_button.grid(row=0, column=1, padx=5)
        
        # 执行控制
        execute_frame = ttk.Frame(main_frame)
        execute_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(execute_frame, text=self.lang.get('start_execute'), 
                                     command=self.start_execution, style="Action.TButton")
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(execute_frame, text=self.lang.get('stop_execute'), 
                                    command=self.stop_execution, style="Action.TButton")
        self.stop_button.grid(row=0, column=1, padx=5)
        self.stop_button['state'] = 'disabled'
        
        # 快捷键说明
        help_frame = ttk.LabelFrame(main_frame, text=self.lang.get('hotkey_title'), padding="5")
        help_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.help_label = ttk.Label(help_frame, text=self.lang.get('hotkey_text'), justify=tk.LEFT)
        self.help_label.grid(row=0, column=0, padx=5, pady=5)

    def switch_language(self):
        self.lang.switch()
        self.update_gui_text()

    def update_gui_text(self):
        # 更新窗口标题
        self.root.title(self.lang.get('title'))
        
        # 更新语言切换按钮
        self.lang_button.configure(text=self.lang.get('switch_lang'))
        
        # 更新状态文本
        if self.is_recording:
            self.status_var.set(self.lang.get('recording'))
        else:
            self.status_var.set(self.lang.get('ready'))
        
        # 更新所有框架标题（包括嵌套框架）
        def update_frame_titles(widget):
            if isinstance(widget, ttk.LabelFrame):
                # 控制面板
                if "控制面板" in widget.cget('text') or "Control Panel" in widget.cget('text'):
                    widget.configure(text=self.lang.get('control_panel'))
                # 参数设置
                elif "参数设置" in widget.cget('text') or "Settings" in widget.cget('text'):
                    widget.configure(text=self.lang.get('settings'))
                # 记录的点击位置
                elif "记录的点击位置" in widget.cget('text') or "Recorded Positions" in widget.cget('text'):
                    widget.configure(text=self.lang.get('recorded_positions'))
                # 快捷键说明
                elif "快捷键说明" in widget.cget('text') or "Hotkeys" in widget.cget('text'):
                    widget.configure(text=self.lang.get('hotkey_title'))
                # 点击类型
                elif "点击类型" in widget.cget('text') or "Click Type" in widget.cget('text'):
                    widget.configure(text=self.lang.get('click_type'))
            
            # 递归处理所有子部件
            for child in widget.winfo_children():
                update_frame_titles(child)
        
        # 从主框架开始更新所有标题
        for child in self.root.winfo_children():
            update_frame_titles(child)
        
        # 更新按钮文本
        self.record_button.configure(text=self.lang.get('start_record') if not self.is_recording else self.lang.get('stop_record'))
        self.clear_button.configure(text=self.lang.get('clear_all'))
        self.single_radio.configure(text=self.lang.get('single_click'))
        self.double_radio.configure(text=self.lang.get('double_click'))
        
        # 更新设置标签
        self.repeat_label.configure(text=self.lang.get('repeat_times'))
        self.delay_label.configure(text=self.lang.get('delay_seconds'))
        self.interval_label.configure(text=self.lang.get('click_interval'))
        
        # 更新树形视图标题
        self.update_tree_headers()
        
        # 更新按钮文本
        self.delete_button.configure(text=self.lang.get('delete_selected'))
        self.edit_button.configure(text=self.lang.get('edit_selected'))
        self.start_button.configure(text=self.lang.get('start_execute'))
        self.stop_button.configure(text=self.lang.get('stop_execute'))
        
        # 更新快捷键说明
        self.help_label.configure(text=self.lang.get('hotkey_text'))

    def update_tree_headers(self):
        self.tree.heading('序号', text=self.lang.get('number'))
        self.tree.heading('X坐标', text=self.lang.get('x_coord'))
        self.tree.heading('Y坐标', text=self.lang.get('y_coord'))
        self.tree.heading('点击类型', text=self.lang.get('click_type_col'))
        self.tree.heading('时间', text=self.lang.get('time'))

    def setup_keyboard_listener(self):
        def check_hotkeys():
            while True:
                if keyboard.is_pressed('f6'):
                    self.root.after(0, self.toggle_recording)
                    time.sleep(0.3)
                elif keyboard.is_pressed('f7') and self.is_recording:
                    self.root.after(0, self.record_position)
                    time.sleep(0.3)
                elif keyboard.is_pressed('f8') and not self.is_running:
                    self.root.after(0, self.start_execution)
                    time.sleep(0.3)
                elif keyboard.is_pressed('f9') and self.is_running:
                    self.root.after(0, self.stop_execution)
                    time.sleep(0.3)
                elif keyboard.is_pressed('esc'):
                    self.root.after(0, self.root.quit)
                    break
                time.sleep(0.1)
        
        threading.Thread(target=check_hotkeys, daemon=True).start()
    
    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.record_button.configure(text=self.lang.get('stop_record'))
            self.status_var.set(self.lang.get('recording'))
        else:
            self.record_button.configure(text=self.lang.get('start_record'))
            self.status_var.set(self.lang.get('ready'))
    
    def record_position(self):
        if not self.is_recording:
            return
        x, y = pyautogui.position()
        click_type = self.current_click_type.get()
        self.actions.append(MouseAction(x, y, click_type))
        current_time = datetime.now().strftime("%H:%M:%S")
        click_type_text = self.lang.get('double_text') if click_type == "double" else self.lang.get('single_text')
        self.tree.insert('', 'end', values=(len(self.actions), x, y, click_type_text, current_time))
    
    def clear_actions(self):
        if messagebox.askyesno(self.lang.get('warning'), self.lang.get('confirm_clear')):
            self.actions.clear()
            for item in self.tree.get_children():
                self.tree.delete(item)
    
    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('select_to_delete'))
            return
            
        if messagebox.askyesno(self.lang.get('warning'), self.lang.get('confirm_delete')):
            for item in selected:
                index = self.tree.index(item)
                self.actions.pop(index)
                self.tree.delete(item)
            self.update_indexes()
    
    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('select_to_edit'))
            return
        
        if len(selected) > 1:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('one_at_time'))
            return
            
        item = selected[0]
        index = self.tree.index(item)
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title(self.lang.get('edit_selected'))
        edit_window.geometry("300x200")
        
        ttk.Label(edit_window, text=self.lang.get('move_mouse')).pack(pady=10)
        
        click_type_var = tk.StringVar(value=self.actions[index].click_type)
        click_frame = ttk.LabelFrame(edit_window, text=self.lang.get('click_type'))
        click_frame.pack(pady=10)
        ttk.Radiobutton(click_frame, text=self.lang.get('single_click'), 
                       variable=click_type_var, value="single").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(click_frame, text=self.lang.get('double_click'), 
                       variable=click_type_var, value="double").pack(side=tk.LEFT, padx=5)
        
        def confirm():
            x, y = pyautogui.position()
            click_type = click_type_var.get()
            self.actions[index] = MouseAction(x, y, click_type)
            current_time = datetime.now().strftime("%H:%M:%S")
            click_type_text = self.lang.get('double_text') if click_type == "double" else self.lang.get('single_text')
            self.tree.set(item, column=1, value=x)
            self.tree.set(item, column=2, value=y)
            self.tree.set(item, column=3, value=click_type_text)
            self.tree.set(item, column=4, value=current_time)
            edit_window.destroy()
        
        ttk.Button(edit_window, text=self.lang.get('confirm'), command=confirm).pack(pady=10)
        ttk.Button(edit_window, text=self.lang.get('cancel'), 
                  command=edit_window.destroy).pack(pady=5)
    
    def update_indexes(self):
        for i, item in enumerate(self.tree.get_children(), 1):
            self.tree.set(item, column=0, value=i)
    
    def start_execution(self):
        if not self.actions:
            messagebox.showwarning(self.lang.get('warning'), self.lang.get('no_positions'))
            return
            
        try:
            repeat_times = int(self.repeat_times.get())
            delay_seconds = int(self.delay_seconds.get())
            click_interval = float(self.click_interval.get())
            
            if repeat_times < 1 or delay_seconds < 0 or click_interval < 0:
                raise ValueError("参数必须大于0")
                
        except ValueError as e:
            messagebox.showerror(self.lang.get('warning'), self.lang.get('invalid_params'))
            return
        
        self.is_running = True
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.record_button['state'] = 'disabled'
        
        def execute():
            self.status_var.set(self.lang.get('preparing').format(delay_seconds))
            for i in range(delay_seconds, 0, -1):
                if not self.is_running:
                    break
                self.status_var.set(self.lang.get('preparing').format(i))
                time.sleep(1)
            
            for i in range(repeat_times):
                if not self.is_running:
                    break
                self.status_var.set(self.lang.get('executing').format(i+1, repeat_times))
                for j, action in enumerate(self.actions, 1):
                    if not self.is_running:
                        break
                    pyautogui.moveTo(action.x, action.y)
                    if action.click_type == "double":
                        pyautogui.doubleClick()
                    else:
                        pyautogui.click()
                    time.sleep(click_interval)
            
            self.is_running = False
            self.root.after(0, self.reset_execution_state)
        
        threading.Thread(target=execute, daemon=True).start()
    
    def stop_execution(self):
        self.is_running = False
        self.status_var.set(self.lang.get('stopped'))
        self.reset_execution_state()
    
    def reset_execution_state(self):
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.record_button['state'] = 'normal'
        if not self.is_running:
            self.status_var.set(self.lang.get('ready'))

    def add_watermark(self):
        # 创建水印标签
        watermark = tk.Label(self.root, 
                           text="@Travisma2233", 
                           fg='gray',
                           font=('Arial', 10, 'italic'))
        # 将水印放置在窗口右下角
        watermark.place(relx=1.0, 
                       rely=1.0, 
                       anchor='se', 
                       x=-10, 
                       y=-5)

def main():
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    main() 