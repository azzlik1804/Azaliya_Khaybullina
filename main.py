import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import json
import os
import subprocess

# Путь к файлу истории
HISTORY_FILE = "tasks.json"
VALID_CATEGORIES = ["учёба", "спорт", "работа"]

# Предопределённые задачи с категориями
DEFAULT_TASKS = [
    {"task": "Прочитать статью", "category": "учёба"},
    {"task": "Сделать зарядку", "category": "спорт"},
    {"task": "Написать отчёт", "category": "работа"},
    {"task": "Выучить 10 слов на английском", "category": "учёба"},
    {"task": "Пробежать 3 км", "category": "спорт"},
    {"task": "Ответить на письма", "category": "работа"},
]

# --- ИСПРАВЛЕНИЕ 1: Надежная загрузка истории ---
def load_history():
    """Загружает историю из файла. Если файл пуст или поврежден, возвращает пустой список."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:  # Если файл пустой
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        # Если файл поврежден или ошибка чтения
        return []

# --- ИСПРАВЛЕНИЕ 2: Корректное сохранение ---
def save_history(history):
    """Сохраняет историю, гарантируя запись валидного JSON."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")

# Инициализация файла при старте, если он пуст
def init_storage():
    if not os.path.exists(HISTORY_FILE) or os.path.getsize(HISTORY_FILE) == 0:
        save_history([])

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
    current_task_label.config(text=task_text, fg="#2c3e50")

    # Добавляем в историю
    history = load_history()
    history.append(task_text)
    save_history(history)
    update_history_list()

# Обновление списка истории в интерфейсе
def update_history_list():
    history_listbox.delete(0, tk.END)
    history = load_history()
    for item in reversed(history):  # Показываем новые задачи сверху
        history_listbox.insert(tk.END, item)

# --- ИСПРАВЛЕНИЕ 3: Улучшенная валидация ввода ---
def add_new_task():
    # 1. Проверка названия
    new_task = simpledialog.askstring("Новая задача", "Введите название задачи:")
    if not new_task or not new_task.strip():
        messagebox.showerror("Ошибка ввода", "Задача не может быть пустой!")
