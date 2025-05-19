import tkinter as tk
from tkinter import messagebox
import csv
import datetime
from typing import Set, Tuple

def load_area_codes(filename: str) -> Set[str]:
    """
    加载区划代码文件，返回区划代码集合。如出错弹窗提示。
    """
    codes = set()
    try:
        with open(filename, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                codes.add(row['code'])
    except FileNotFoundError:
        messagebox.showerror("错误", f"未找到区划代码文件: {filename}")
    except Exception as e:
        messagebox.showerror("错误", f"读取区划代码文件失败: {e}")
    return codes

def is_valid_date(date_str: str) -> bool:
    """
    校验日期字符串是否合法（格式：YYYYMMDD）。
    """
    try:
        datetime.datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def calc_check_digit(id17: str) -> str:
    """
    计算身份证前17位的校验码。
    """
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    s = sum(int(n) * w for n, w in zip(id17, weights))
    r = s % 11
    return check_map[r]

def validate_id_card(id_number: str, area_codes: Set[str]) -> Tuple[bool, str]:
    """
    校验身份证号的合法性。
    返回 (是否通过, 消息)。
    """
    id_number = id_number.strip().upper()
    if len(id_number) != 18:
        return False, "身份证号长度应为18位"
    if not id_number[:17].isdigit():
        return False, "前17位应为数字"
    if not (id_number[-1].isdigit() or id_number[-1] == 'X'):
        return False, "最后一位应为数字或大写X"
    area_code = id_number[:6]
    if area_code not in area_codes:
        return False, f"区划代码{area_code}不合法"
    birth_date = id_number[6:14]
    if not is_valid_date(birth_date):
        return False, "出生日期无效"
    check_digit = calc_check_digit(id_number[:17])
    if id_number[-1] != check_digit:
        return False, f"校验码错误，应为 {check_digit}"
    return True, "校验通过"

class IDValidatorApp(tk.Tk):
    """
    身份证校验工具GUI应用
    """
    def __init__(self, area_codes: Set[str]):
        super().__init__()
        self.title("身份证号码校验工具")
        self.geometry("400x180")
        self.area_codes = area_codes

        self.label = tk.Label(self, text="请输入18位身份证号：")
        self.label.pack(pady=10)

        self.id_entry = tk.Entry(self, width=26, font=("Arial", 14))
        self.id_entry.pack(pady=5)
        self.id_entry.bind("<Return>", self.on_enter)  # 支持回车

        self.check_button = tk.Button(self, text="校验", command=self.check_id)
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=5)

        self.id_entry.focus_set()

    def check_id(self) -> None:
        """
        获取输入内容并进行校验，显示结果。
        """
        id_number = self.id_entry.get()
        try:
            is_valid, message = validate_id_card(id_number, self.area_codes)
            self.result_label.config(text=message, fg="green" if is_valid else "red")
            if not is_valid:
                self.id_entry.focus_set()
                self.id_entry.selection_range(0, tk.END)
        except Exception as e:
            messagebox.showerror("错误", f"校验过程中出现异常: {e}")

    def on_enter(self, event) -> None:
        """
        回车键事件，触发校验。
        """
        self.check_id()

if __name__ == "__main__":
    area_codes = load_area_codes("areas.csv")
    if area_codes:
        app = IDValidatorApp(area_codes)
        app.mainloop()
