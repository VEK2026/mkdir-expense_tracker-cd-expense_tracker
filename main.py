import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# --- Функции ---
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_expense():
    amount = entry_amount.get()
    category = combo_category.get()
    date = entry_date.get()

    # Валидация
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            raise ValueError
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Сумма должна быть > 0, Дата в формате ГГГГ-ММ-ДД")
        return

    data = load_data()
    data.append({"amount": amount_float, "category": category, "date": date})
    save_data(data)
    
    clear_entries()
    update_table()
    calculate_total()

def update_table(filtered_data=None):
    # Очистка таблицы
    for i in tree.get_children():
        tree.delete(i)
    
    data = filtered_data if filtered_data is not None else load_data()
    
    for item in data:
        tree.insert("", "end", values=(item["date"], item["category"], item["amount"]))

def calculate_total():
    data = load_data()
    # Просто сумма за всё время
    total = sum(item["amount"] for item in data)
    label_total.config(text=f"Всего расходов: {total:.2f}")

def filter_data():
    date_from = entry_filter_from.get()
    date_to = entry_filter_to.get()
    category = combo_filter_cat.get()
    
    data = load_data()
    filtered = []
    
    for item in data:
        match = True
        if category and item["category"] != category:
            match = False
        if date_from and item["date"] < date_from:
            match = False
        if date_to and item["date"] > date_to:
            match = False
        
        if match:
            filtered.append(item)
            
    update_table(filtered)
    # Считаем сумму за отфильтрованный период
    total = sum(item["amount"] for item in filtered)
    label_total.config(text=f"Сумма (фильтр): {total:.2f}")

def clear_entries():
    entry_amount.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

# --- GUI ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x550")

# Форма добавления
frame_form = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=10)
frame_form.pack(padx=10, pady=10, fill="x")

tk.Label(frame_form, text="Сумма:").grid(row=0, column=0)
entry_amount = tk.Entry(frame_form)
entry_amount.grid(row=0, column=1)

tk.Label(frame_form, text="Категория:").grid(row=1, column=0)
combo_category = ttk.Combobox(frame_form, values=["Еда", "Транспорт", "Развлечения", "Другое"])
combo_category.grid(row=1, column=1)
combo_category.current(0)

tk.Label(frame_form, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0)
entry_date = tk.Entry(frame_form)
entry_date.grid(row=2, column=1)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))

btn_add = tk.Button(frame_form, text="Добавить", command=add_expense)
btn_add.grid(row=3, columnspan=2, pady=5)

# Фильтрация
frame_filter = tk.LabelFrame(root, text="Фильтр", padx=10, pady=10)
frame_filter.pack(padx=10, pady=5, fill="x")

tk.Label(frame_filter, text="С:").pack(side="left")
entry_filter_from = tk.Entry(frame_filter, width=10)
entry_filter_from.pack(side="left")

tk.Label(frame_filter, text="По:").pack(side="left")
entry_filter_to = tk.Entry(frame_filter, width=10)
entry_filter_to.pack(side="left")

tk.Label(frame_filter, text="Кат:").pack(side="left")
combo_filter_cat = ttk.Combobox(frame_filter, values=["", "Еда", "Транспорт", "Развлечения", "Другое"], width=10)
combo_filter_cat.pack(side="left")

btn_filter = tk.Button(frame_filter, text="Фильтр", command=filter_data)
btn_filter.pack(side="left", padx=5)

btn_reset = tk.Button(frame_filter, text="Сброс", command=update_table)
btn_reset.pack(side="left")

# Таблица
tree = ttk.Treeview(root, columns=("Date", "Category", "Amount"), show="headings")
tree.heading("Date", text="Дата")
tree.heading("Category", text="Категория")
tree.heading("Amount", text="Сумма")
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Итого
label_total = tk.Label(root, text="Всего расходов: 0.00", font=("Arial", 12, "bold"))
label_total.pack(pady=10)

# Инициализация
update_table()
calculate_total()

root.mainloop()
