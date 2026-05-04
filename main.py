import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os
import subprocess

# Путь к файлу истории
HISTORY_FILE = "tasks.json"

# Предопределённые задачи с категориями
DEFAULT_TASKS = [
    {"task": "Прочитать статью", "category": "учёба"},
    {"task": "Сделать зарядку", "category": "спорт"},
    {"task": "Написать отчёт", "category": "работа"},
    {"task": "Выучить 10 слов на английском", "category": "учёба"},
    {"task": "Пробежать 3 км", "category": "спорт"},
    {"task": "Ответить на письма", "category": "работа"},
]

# Загрузка истории из файла
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение истории в файл
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Генерация случайной задачи с учётом фильтра
def generate_task():
    category_filter = category_var.get()
    available_tasks = DEFAULT_TASKS

    if category_filter != "Все":
        available_tasks = [t for t in DEFAULT_TASKS if t["category"] == category_filter]

    if not available_tasks:
        messagebox.showwarning("Предупреждение", "Нет задач для выбранной категории.")
        return

    task = random.choice(available_tasks)
    task_text = f"{task['task']} [{task['category']}]"
    current_task_label.config(text=task_text)

    # Добавляем в историю
    history = load_history()
    history.append(task_text)
    save_history(history)
    update_history_list()

# Обновление списка истории в интерфейсе
def update_history_list():
    history_listbox.delete(0, tk.END)
    history = load_history()
    for item in history:
        history_listbox.insert(tk.END, item)

# Добавление новой задачи пользователем
def add_new_task():
    new_task = simpledialog.askstring("Новая задача", "Введите название задачи:")
    if not new_task or not new_task.strip():
        messagebox.showerror("Ошибка", "Задача не может быть пустой!")
        return

    category = simpledialog.askstring("Категория", "Введите категорию (учёба, спорт, работа):")
    if category not in ["учёба", "спорт", "работа"]:
        messagebox.showerror("Ошибка", "Недопустимая категория! Используйте: учёба, спорт, работа.")
        return

    new_entry = {"task": new_task.strip(), "category": category}
    DEFAULT_TASKS.append(new_entry)
    messagebox.showinfo("Успех", "Задача добавлена!")

# Инициализация Git репозитория и коммит
def init_git():
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        messagebox.showinfo("Git", "Git репозиторий инициализирован и сделан первый коммит.")
    except Exception as e:
        messagebox.showerror("Git Error", f"Ошибка при работе с Git: {e}")

# Создание основного окна
root = tk.Tk()
root.title("Random Task Generator")
root.geometry("600x500")

# Метка для текущей задачи
current_task_label = tk.Label(root, text="Нажмите 'Сгенерировать задачу'", font=("Arial", 14))
current_task_label.pack(pady=10)

# Выпадающий список для фильтрации по категории
category_var = tk.StringVar(value="Все")
category_menu = tk.OptionMenu(root, category_var, "Все", "учёба", "спорт", "работа")
category_menu.pack(pady=5)

# Кнопка генерации задачи
generate_button = tk.Button(root, text="Сгенерировать задачу", command=generate_task, font=("Arial", 12))
generate_button.pack(pady=5)

# Кнопка добавления новой задачи
add_button = tk.Button(root, text="Добавить новую задачу", command=add_new_task, font=("Arial", 12))
add_button.pack(pady=5)

# Список истории
history_label = tk.Label(root, text="История задач:", font=("Arial", 12))
history_label.pack(pady=5)

history_listbox = tk.Listbox(root, width=50, height=10)
history_listbox.pack(pady=5)

# Кнопка инициализации Git
git_button = tk.Button(root, text="Инициализировать Git", command=init_git, font=("Arial", 12))
git_button.pack(pady=10)

# Загрузка истории при запуске
update_history_list()

# Запуск приложения
root.mainloop()
