# 身份证校验
import tkinter as tk
from tkinter import messagebox
import csv
import datetime

def load_area_codes(filename):
    codes = set()
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codes.add(row['code'])
    return codes

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False

def calc_check_digit(id17):
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    s = sum(int(n) * w for n, w in zip(id17, weights))
    r = s % 11
    return check_map[r]

def validate_id_card(id_number, area_codes):
    if len(id_number) != 18:
        return False, "身份证号长度应为18位"
    if not id_number[:17].isdigit():
        return False, "前17位应为数字"
    if not (id_number[-1].isdigit() or id_number[-1] == 'X'):
        return False, "最后一位应为数字或大写X"
    if id_number[-1] == 'x':
        return False, "校验码X必须为大写"
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
    def __init__(self, area_codes):
        super().__init__()
        self.title("身份证号码校验工具")
        self.geometry("400x180")
        self.area_codes = area_codes

        self.label = tk.Label(self, text="请输入18位身份证号：")
        self.label.pack(pady=10)

        self.id_entry = tk.Entry(self, width=26, font=("Arial", 14))
        self.id_entry.pack(pady=5)

        self.check_button = tk.Button(self, text="校验", command=self.check_id)
        self.check_button.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=5)

    def check_id(self):
        id_number = self.id_entry.get().strip()
        is_valid, message = validate_id_card(id_number, self.area_codes)
        self.result_label.config(text=message, fg="green" if is_valid else "red")

if __name__ == "__main__":
    area_codes = load_area_codes("areas.csv")
    app = IDValidatorApp(area_codes)
    app.mainloop()