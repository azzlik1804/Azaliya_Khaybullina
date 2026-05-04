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

# --- ИСПРАВЛЕНИЕ 1: Надёжная загрузка истории ---
def load_history():
    """
    Загружает историю из JSON-файла.
    Если файл отсутствует, пуст или повреждён — возвращает пустой список.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:  # Пустой файл
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError, OSError):
        # Файл повреждён или ошибка чтения
        return []

# --- ИСПРАВЛЕНИЕ 2: Надёжное сохранение истории ---
def save_history(history):
    """Сохраняет историю в JSON с обработкой ошибок записи."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except (IOError, OSError) as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить историю: {e}")
        return False

# Инициализация файла истории при старте
def init_storage():
    """Создаёт файл истории с пустым массивом, если он отсутствует или пуст."""
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
    if save_history(history):
        update_history_list()

# Обновление списка истории в интерфейсе
def update_history_list():
    history_listbox.delete(0, tk.END)
    history = load_history()
    # Показываем новые задачи сверху
    for item in reversed(history):
        history_listbox.insert(tk.END, item)

# --- ИСПРАВЛЕНИЕ 3: Улучшенная валидация ввода ---
def add_new_task():
    # 1. Проверка названия задачи
    new_task = simpledialog.askstring("Новая задача", "Введите название задачи:")
    if not new_task or not new_task.strip():
        messagebox.showerror("Ошибка ввода", "Задача не может быть пустой!")
        return

    # 2. Выбор категории через выпадающий список (вместо ручного ввода!)
    category_window = tk.Toplevel(root)
    category_window.title("Выберите категорию")
    category_window.geometry("300x150")
    category_window.transient(root)
    category_window.grab_set()

    tk.Label(category_window, text="Категория задачи:").pack(pady=10)
    
    selected_category = tk.StringVar()
    category_combo = ttk.Combobox(category_window, textvariable=selected_category, 
                                   values=VALID_CATEGORIES, state="readonly", width=25)
    category_combo.pack(pady=5)
    category_combo.current(0)  # Выбрать первую по умолчанию

    def confirm_category():
        category = selected_category.get()
        if category not in VALID_CATEGORIES:
            messagebox.showerror("Ошибка", "Выберите допустимую категорию!")
            return
        # Добавляем задачу
        new_entry = {"task": new_task.strip(), "category": category}
        DEFAULT_TASKS.append(new_entry)
        messagebox.showinfo("Успех", f"Задача '{new_task.strip()}' добавлена в категорию '{category}'!")
        category_window.destroy()

    tk.Button(category_window, text="Добавить", command=confirm_category).pack(pady=10)

# Инициализация Git-репозитория
def init_git():
    try:
        # Проверяем, установлен ли git
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True, capture_output=True)
        
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True, capture_output=True)
        
        messagebox.showinfo("Git", "✓ Репозиторий инициализирован\n✓ Файлы добавлены\n✓ Создан коммит")
    except subprocess.CalledProcessError:
        messagebox.showerror("Git Error", "Ошибка при выполнении команд Git")
    except FileNotFoundError:
        messagebox.showerror("Git не найден", "Убедитесь, что Git установлен и добавлен в PATH")

# Очистка истории
def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю задач?"):
        if save_history([]):
            update_history_list()
            messagebox.showinfo("Готово", "История очищена")

# --- Настройка интерфейса ---
def setup_ui():
    root.title("Random Task Generator")
    root.geometry("650x550")
    root.resizable(True, True)
    root.configure(bg="#f5f5f5")

    # Заголовок
    title = tk.Label(root, text="🎲 Random Task Generator", 
                     font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#2c3e50")
    title.pack(pady=15)

    # Текущая задача
    tk.Label(root, text="Ваша задача:", font=("Arial", 12), bg="#f5f5f5").pack()
    global current_task_label
    current_task_label = tk.Label(root, text="Нажмите 'Сгенерировать задачу'", 
                                   font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#e74c3c",
                                   wraplength=550, justify="center")
    current_task_label.pack(pady=10)

    # Фильтр категорий
    filter_frame = tk.Frame(root, bg="#f5f5f5")
    filter_frame.pack(pady=5)
    tk.Label(filter_frame, text="Фильтр:", bg="#f5f5f5").pack(side=tk.LEFT, padx=5)
    
    global category_var
    category_var = tk.StringVar(value="Все")
    category_menu = ttk.Combobox(filter_frame, textvariable=category_var, 
                                  values=["Все"] + VALID_CATEGORIES, 
                                  state="readonly", width=15)
    category_menu.pack(side=tk.LEFT, padx=5)

    # Кнопки управления
    btn_frame = tk.Frame(root, bg="#f5f5f5")
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="🎲 Сгенерировать задачу", command=generate_task,
              font=("Arial", 11), bg="#3498db", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(btn_frame, text="➕ Добавить задачу", command=add_new_task,
              font=("Arial", 11), bg="#2ecc71", fg="white", padx=10).pack(side=tk.LEFT, padx=5)
    
    tk.Button(btn_frame, text="🗑️ Очистить историю", command=clear_history,
              font=("Arial", 11), bg="#e74c3c", fg="white", padx=10).pack(side=tk.LEFT, padx=5)

    # История задач
    tk.Label(root, text="📋 История задач:", font=("Arial", 12, "bold"), 
             bg="#f5f5f5").pack(pady=(15, 5))
    
    global history_listbox
    history_listbox = tk.Listbox(root, width=70, height=12, font=("Arial", 10),
                                  bg="white", selectbackground="#3498db")
    history_listbox.pack(pady=5)
    
    # Скроллбар для истории
    scrollbar = ttk.Scrollbar(history_listbox, orient=tk.VERTICAL, command=history_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    history_listbox.configure(yscrollcommand=scrollbar.set)

    # Git-кнопка
    tk.Button(root, text="🔧 Git: Init & Commit", command=init_git,
              font=("Arial", 10), bg="#95a5a6", fg="white").pack(pady=10)

    # Статус бар
    status = tk.Label(root, text="✓ Готов к работе | Файл истории: tasks.json", 
                      font=("Arial", 9), bg="#ecf0f1", fg="#7f8c8d", anchor="w")
    status.pack(side=tk.BOTTOM, fill=tk.X)

# --- Точка входа ---
if __name__ == "__main__":
    root = tk.Tk()
    
    # Инициализация хранилища ПЕРЕД запуском UI
    init_storage()
    
    setup_ui()
    update_history_list()  # Загрузить историю при старте
    
    root.mainloop()
        
