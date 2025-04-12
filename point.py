import pyautogui
import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox

pyautogui.FAILSAFE = True 
pyautogui.PAUSE = 0.01 

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("滑鼠連點程式")
        self.root.geometry("300x300")

        self.running = False
        self.click_thread = None
        self.button_choice = tk.StringVar(value="right")  # 預設
        self.interval = tk.DoubleVar(value=10.0)  # 預設間隔秒
        self.remaining_time = 0  # 剩餘時間（秒）


        tk.Label(root, text="選擇滑鼠按鍵：").pack(pady=5)
        tk.Radiobutton(root, text="左鍵", variable=self.button_choice, value="left").pack()
        tk.Radiobutton(root, text="右鍵", variable=self.button_choice, value="right").pack()


        tk.Label(root, text="點擊間隔（秒）：").pack(pady=5)
        tk.Entry(root, textvariable=self.interval).pack()


        self.status_frame = tk.Frame(root)
        self.status_frame.pack(pady=10)
        self.status_label = tk.Label(self.status_frame, text="狀態：已停止", fg="red")
        self.status_label.pack(side=tk.LEFT)
        self.countdown_label = tk.Label(self.status_frame, text="", fg="blue")
        self.countdown_label.pack(side=tk.LEFT, padx=10)

        tk.Button(root, text="開始連點 (Shift + F5)", command=self.start_clicking).pack(pady=5)
        tk.Button(root, text="停止連點 (Shift + F6)", command=self.stop_clicking).pack(pady=5)


        tk.Label(root, text="按 Tab 鍵可緊急停止程式").pack(pady=5)


        tk.Label(root, text="Develop by DigKen", font=("Arial", 10, "italic"), fg="gray").pack(side=tk.BOTTOM, pady=5)

        keyboard.add_hotkey('shift+f5', self.start_clicking)  # Shift + F5 開啟連點
        keyboard.add_hotkey('shift+f6', self.stop_clicking)   # Shift + F6 關閉連點

        # 綁定 Esc 鍵來緊急停止程式
        keyboard.on_press_key("tab", lambda e: self.emergency_stop())

    def start_clicking(self):
        if self.running:
            messagebox.showinfo("提示", "連點已經在運行中！")
            return

        try:
            interval = self.interval.get()
            if interval <= 0:
                messagebox.showerror("錯誤", "點擊間隔必須大於 0！")
                return
        except tk.TclError:
            messagebox.showerror("錯誤", "請輸入有效的數字！")
            return

        self.running = True
        self.click_thread = threading.Thread(target=self.click_loop)
        self.click_thread.start()
        self.status_label.config(text="狀態：運行中", fg="green")
        print("連點已開始")

    def stop_clicking(self):
        if not self.running:
            messagebox.showinfo("提示", "連點尚未開始！")
            return
        self.running = False
        if self.click_thread:
            self.click_thread.join()
        self.status_label.config(text="狀態：已停止", fg="red")
        self.countdown_label.config(text="")  
        print("連點已停止")

    def emergency_stop(self):
        self.running = False
        if self.click_thread:
            self.click_thread.join()
        self.status_label.config(text="狀態：已停止", fg="red")
        self.countdown_label.config(text="")
        print("程式已緊急停止！")
        self.root.quit()

    def click_loop(self):
        button = self.button_choice.get()  
        interval = self.interval.get()  

        while self.running:
            start_time = time.time()  
            self.remaining_time = interval 

           
            while self.remaining_time > 0 and self.running:
                self.countdown_label.config(text=f"下次點擊：{self.remaining_time:.1f} 秒")
                self.root.update()  
                time.sleep(0.1)  
                elapsed = time.time() - start_time  
                self.remaining_time = interval - elapsed  

            if self.running:  
                pyautogui.click(button=button)  
                sleep_time = interval - (time.time() - start_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)  

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()