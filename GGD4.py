import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- Функции для гидрогазодинамических расчётов ---
def calculate_hydro():
    try:
        V1 = float(entry_V1.get())
        F1 = float(entry_F1.get())
        p1 = float(entry_p1.get())
        F2 = float(entry_F2.get())
        p2 = float(entry_p2.get())
        G = float(entry_G.get())
        P1 = float(entry_P1.get())
        delta_Ptr = float(entry_delta_Ptr.get())

        V2 = (V1 * F1 * p1 + G) / (F2 * p2)
        P2 = P1 - delta_Ptr

        result_V2.config(text=f"Скорость во втором сечении (V2): {V2:.4f} м/с")
        result_P2.config(text=f"Давление во втором сечении (P2): {P2:.4f} Па")

    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный ввод! Проверьте данные.")

def create_hydro_window():
    hydro_window = tk.Toplevel()
    hydro_window.title("Расчёт гидрогазодинамических параметров")
    hydro_window.geometry("500x500")
    hydro_window.grab_set()

    label_title = ttk.Label(hydro_window, text="Введите параметры потока:", font=("Arial", 12, "bold"))
    label_title.pack(pady=10)

    frame_inputs = ttk.Frame(hydro_window)
    frame_inputs.pack(pady=10)

    # Поля ввода для гидрогазодинамики
    labels = [
        "Скорость в первом сечении (V1) [м/с]:",
        "Площадь первого сечения (F1) [м²]:",
        "Плотность в первом сечении (p1) [кг/м³]:",
        "Площадь второго сечения (F2) [м²]:",
        "Плотность во втором сечении (p2) [кг/м³]:",
        "Добавленный массовый расход (G) [кг/с]:",
        "Давление в первом сечении (P1) [Па]:",
        "Потери давления на трение (ΔPтр) [Па]:"
    ]

    entries = []
    for i, text in enumerate(labels):
        label = ttk.Label(frame_inputs, text=text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(frame_inputs)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    global entry_V1, entry_F1, entry_p1, entry_F2, entry_p2, entry_G, entry_P1, entry_delta_Ptr
    entry_V1, entry_F1, entry_p1, entry_F2, entry_p2, entry_G, entry_P1, entry_delta_Ptr = entries

    button_calculate = ttk.Button(hydro_window, text="Рассчитать", command=calculate_hydro)
    button_calculate.pack(pady=10)

    frame_results = ttk.Frame(hydro_window)
    frame_results.pack(pady=10)

    global result_V2, result_P2
    result_V2 = ttk.Label(frame_results, text="Скорость во втором сечении (V2): -", font=("Arial", 10))
    result_V2.pack(pady=5)
    result_P2 = ttk.Label(frame_results, text="Давление во втором сечении (P2): -", font=("Arial", 10))
    result_P2.pack(pady=5)

# --- Функции для расчёта теплопередачи ---
def calculate_heat():
    try:
        alpha1 = float(entry_alpha1.get())
        alpha2 = float(entry_alpha2.get())
        lambda_ = float(entry_lambda.get())
        d1 = float(entry_d1.get())
        d2 = float(entry_d2.get())
        G = float(entry_G_heat.get())
        Cp = float(entry_Cp.get())
        T_env = float(entry_T_env.get())
        T = float(entry_T.get())
        T1 = float(entry_T1.get())
        l = float(entry_l.get())

        if d1 <= 0 or d2 <= 0 or d1 >= d2:
            raise ValueError("Диаметры должны быть положительными, и d2 > d1")
        if alpha1 <= 0 or alpha2 <= 0 or lambda_ <= 0 or G <= 0 or Cp <= 0 or l <= 0:
            raise ValueError("Все коэффициенты должны быть положительными")

        k = 1 / (1/alpha1 + d1 * math.log(d2/d1) / (2 * lambda_) + d1/(alpha2 * d2))
        F = math.pi * d1 * l
        Q = k * F * (T_env - T)
        T2 = T1 + Q / (G * Cp)

        result_k.config(text=f"Коэффициент теплопередачи (k): {k:.4f} Вт/(м²·К)")
        result_Q.config(text=f"Тепловой поток (Q): {Q:.4f} Вт")
        result_T2.config(text=f"Температура во втором сечении (T2): {T2:.4f} °C")

    except ValueError as e:
        messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")
    except ZeroDivisionError:
        messagebox.showerror("Ошибка", "Деление на ноль! Проверьте входные данные")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

def create_heat_window():
    heat_window = tk.Toplevel()
    heat_window.title("Расчёт теплопередачи через цилиндрическую стенку")
    heat_window.geometry("500x650")
    heat_window.grab_set()

    label_title = ttk.Label(heat_window, text="Введите параметры теплопередачи:", font=("Arial", 12, "bold"))
    label_title.pack(pady=10)

    frame_inputs = ttk.Frame(heat_window)
    frame_inputs.pack(pady=10)

    # Поля ввода для теплопередачи
    heat_labels = [
        "Коэффициент теплоотдачи внутри (α1) [Вт/м²·К]:",
        "Коэффициент теплоотдачи снаружи (α2) [Вт/м²·К]:",
        "Теплопроводность материала (λ) [Вт/м·К]:",
        "Внутренний диаметр (d1) [м]:",
        "Внешний диаметр (d2) [м]:",
        "Длина трубы (l) [м]:",
        "Массовый расход (G) [кг/с]:",
        "Удельная теплоёмкость (Cp) [Дж/кг·К]:",
        "Температура окружающей среды (Tокр) [°C]:",
        "Температура внутри трубы (T) [°C]:",
        "Температура в первом сечении (T1) [°C]:"
    ]

    heat_entries = []
    for i, text in enumerate(heat_labels):
        label = ttk.Label(frame_inputs, text=text)
        label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = ttk.Entry(frame_inputs)
        entry.grid(row=i, column=1, padx=5, pady=5)
        heat_entries.append(entry)

    global entry_alpha1, entry_alpha2, entry_lambda, entry_d1, entry_d2, entry_l, entry_G_heat, entry_Cp, entry_T_env, entry_T, entry_T1
    (entry_alpha1, entry_alpha2, entry_lambda, entry_d1, entry_d2, 
     entry_l, entry_G_heat, entry_Cp, entry_T_env, entry_T, entry_T1) = heat_entries

    button_calculate = ttk.Button(heat_window, text="Рассчитать", command=calculate_heat)
    button_calculate.pack(pady=10)

    frame_results = ttk.Frame(heat_window)
    frame_results.pack(pady=10)

    global result_k, result_Q, result_T2
    result_k = ttk.Label(frame_results, text="Коэффициент теплопередачи (k): -", font=("Arial", 10))
    result_k.pack(pady=5)
    result_Q = ttk.Label(frame_results, text="Тепловой поток (Q): -", font=("Arial", 10))
    result_Q.pack(pady=5)
    result_T2 = ttk.Label(frame_results, text="Температура во втором сечении (T2): -", font=("Arial", 10))
    result_T2.pack(pady=5)

# --- Главное окно ---
root = tk.Tk()
root.title("Инженерные калькуляторы")
root.geometry("300x150")

label = ttk.Label(root, text="Выберите калькулятор:", font=("Arial", 16))
label.pack(pady=20)

btn_hydro = ttk.Button(root, text="Поток флюида в трубе", command=create_hydro_window)
btn_hydro.pack(pady=5)

btn_heat = ttk.Button(root, text="Теплопередача", command=create_heat_window)
btn_heat.pack(pady=5)

root.mainloop()