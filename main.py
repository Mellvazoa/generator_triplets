import tkinter as tk
from tkinter import filedialog, messagebox
import random
import re

def generate_fair_triplets(words, iterations):
    if len(words) < 3:
        return ["Ошибка: Нужно минимум 3 слова."]

    pool = []
    used_triplets = set()
    result = []

    n = len(words)
    max_unique = n * (n - 1) * (n - 2) // 6
    actual_iterations = min(iterations, max_unique)

    while len(result) < actual_iterations:
        current_selection = []

        for _ in range(500):
            temp_pool = list(pool)
            current_selection = []

            while len(current_selection) < 3:
                if not temp_pool:
                    new_batch = words[:]
                    random.shuffle(new_batch)
                    temp_pool = new_batch

                candidate = temp_pool.pop()
                if candidate not in current_selection:
                    current_selection.append(candidate)
                else:
                    temp_pool.insert(0, candidate)

            triplet = tuple(sorted(current_selection))
            if triplet not in used_triplets:
                used_triplets.add(triplet)
                pool = temp_pool
                result.append(triplet)
                break

    return result

class TripletsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор троек")
        self.root.geometry("550x650")
        self.root.configure(padx=20, pady=20)

        self.generated_triplets = []
        self.current_index = 0

        tk.Label(root, text="Ввод слов (разделитель: запятая):", font=("Arial", 12, "bold")).pack(
            anchor="w", pady=(0, 5))

        self.text_input = tk.Text(root, height=6, wrap="word", font=("Arial", 12))
        self.text_input.pack(fill="x", pady=5)

        tk.Button(root, text="📂 Загрузить из .txt файла", command=self.load_file).pack(anchor="w", pady=5)

        frame_settings = tk.Frame(root)
        frame_settings.pack(fill="x", pady=15)

        tk.Label(frame_settings, text="Сколько троек подготовить:", font=("Arial", 12)).pack(side="left")

        self.entry_count = tk.Entry(frame_settings, width=8, font=("Arial", 12))
        self.entry_count.insert(0, "15")
        self.entry_count.pack(side="left", padx=10)

        self.btn_prepare = tk.Button(root, text="⚙️ 1. Подготовить массив троек", command=self.prepare_triplets,
                                     bg="#2196F3", fg="black", font=("Arial", 12, "bold"), pady=5)
        self.btn_prepare.pack(fill="x", pady=(10, 5))

        self.btn_next = tk.Button(root, text="👁️ 2. Показать тройку/следующую", command=self.show_next_triplet,
                                  bg="#4CAF50", fg="black", font=("Arial", 14, "bold"), pady=10, state="disabled")
        self.btn_next.pack(fill="x", pady=5)

        tk.Label(root, text="Результат генерации:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        result_frame = tk.Frame(root)
        result_frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")

        self.text_output = tk.Text(result_frame, yscrollcommand=scrollbar.set, font=("Arial", 13), state="disabled",
                                   bg="#f4f4f4")
        self.text_output.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.text_output.yview)

    def load_file(self):
        filepath = filedialog.askopenfilename(title="Выберите текстовый файл",
                                              filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert(tk.END, file.read())
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")

    def prepare_triplets(self):
        raw_text = self.text_input.get("1.0", tk.END)

        words = [word.strip() for word in re.split(r'[,:\n]+', raw_text) if word.strip()]

        if len(words) < 3:
            messagebox.showwarning("Внимание", "Найдено меньше 3 слов. Проверьте ввод/входной файл!")
            return

        try:
            count = int(self.entry_count.get())
            if count <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число троек.")
            return

        self.generated_triplets = generate_fair_triplets(words, count)
        self.current_index = 0

        self.log_to_output(
            f"✅ Успешно подготовлено {count} уникальных троек из {len(words)} слов.\n👉 Нажимайте кнопку 'Показать тройку/следующую'!\n" + "-" * 40 + "\n",
            clear=True)
        self.btn_next.config(state="normal")

    def show_next_triplet(self):
        if self.current_index < len(self.generated_triplets):
            t = self.generated_triplets[self.current_index]
            self.current_index += 1

            if isinstance(t, str):
                self.log_to_output(t + "\n")
            else:
                self.log_to_output(f"Тройка {self.current_index}: {', '.join(t)}\n")

            self.text_output.see(tk.END)

            if self.current_index >= len(self.generated_triplets):
                self.btn_next.config(state="disabled")
                self.log_to_output("-" * 40 + "\n🏁 Все сгенерированные тройки показаны!\n")
                messagebox.showinfo("Готово",
                                    "Список подготовленных троек закончился. Вы можете сгенерировать новый массив.")

    def log_to_output(self, text, clear=False):
        self.text_output.config(state="normal")
        if clear:
            self.text_output.delete("1.0", tk.END)
        self.text_output.insert(tk.END, text)
        self.text_output.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = TripletsApp(root)
    root.mainloop()