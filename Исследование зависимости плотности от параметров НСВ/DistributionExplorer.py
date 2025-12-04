import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DistributionExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("Исследование распределений НСВ")
        self.root.geometry("1000x700")
        
        # Главный контейнер
        self.create_scrollable_container()
        
        # Выбор распределения
        self.distributions = {
            "Равномерное": stats.uniform,
            "Экспоненциальное": stats.expon,
            "Нормальное": stats.norm,
            "Бета": stats.beta
        }
        
        # Параметры по умолчанию
        self.default_params = {
            "Равномерное": {"loc": 0, "scale": 1},
            "Экспоненциальное": {"scale": 1},
            "Нормальное": {"loc": 0, "scale": 1},
            "Бета": {"a": 2, "b": 5}
        }
        
        # Интерфейс
        self.create_widgets()
        self.update_plots()
    
    def create_scrollable_container(self):
        """Создает контейнер с вертикальной и горизонтальной прокруткой"""
        # Главный фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # canvas для прокрутки
        self.canvas_main = tk.Canvas(main_frame)
        self.canvas_main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Вертикальная прокрутка
        v_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas_main.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Горизонтальная прокрутка
        h_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.canvas_main.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Настройка canvas
        self.canvas_main.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas_main.bind('<Configure>', lambda e: self.canvas_main.configure(scrollregion=self.canvas_main.bbox("all")))
        self.content_frame = ttk.Frame(self.canvas_main)
        self.canvas_main.create_window((0, 0), window=self.content_frame, anchor="nw")
        self.canvas_main.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas_main.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)
    
    def _on_mousewheel(self, event):
        """Обработка вертикальной прокрутки колесом мыши"""
        self.canvas_main.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def _on_shift_mousewheel(self, event):
        """Обработка горизонтальной прокрутки Shift+колесо мыши"""
        self.canvas_main.xview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_widgets(self):
        # Фреймы внутри content_frame
        control_frame = ttk.Frame(self.content_frame, padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        plot_frame = ttk.Frame(self.content_frame, padding="10")
        plot_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
        
        # Выбор распределения
        ttk.Label(control_frame, text="Распределение:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.dist_var = tk.StringVar(value="Равномерное")
        dist_combo = ttk.Combobox(control_frame, textvariable=self.dist_var, 
                                  values=list(self.distributions.keys()), 
                                  state="readonly", width=25, font=('Arial', 10))
        dist_combo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        dist_combo.bind("<<ComboboxSelected>>", self.on_distribution_change)
        
        param_group = ttk.LabelFrame(control_frame, text="Параметры распределения", padding="10")
        param_group.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.param_frame = ttk.Frame(param_group)
        self.param_frame.pack(fill=tk.BOTH, expand=True)
        
        # Слайдеры для параметров
        self.create_parameter_sliders()
        
        # Группа для информации с рамкой
        info_group = ttk.LabelFrame(control_frame, text="Теоретическая информация", padding="10")
        info_group.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        # Теоретическая информация с прокруткой
        info_frame = ttk.Frame(info_group)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Вертикальная прокрутка для текста
        info_scrollbar = ttk.Scrollbar(info_frame)
        info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(info_frame, height=12, width=60, font=('Courier', 9),
                                yscrollcommand=info_scrollbar.set, wrap=tk.WORD)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scrollbar.config(command=self.info_text.yview)
        
        # Кнопка обновления
        ttk.Button(control_frame, text="Обновить графики", 
                  command=self.update_plots).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Группа для графиков с рамкой
        plot_group = ttk.LabelFrame(plot_frame, text="Графики распределения", padding="10")
        plot_group.pack(fill=tk.BOTH, expand=True)
        
        # Создание графиков
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(14, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_group)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        control_frame.columnconfigure(1, weight=1)
        param_group.columnconfigure(0, weight=1)
        info_group.columnconfigure(0, weight=1)
        plot_group.columnconfigure(0, weight=1)
    
    def create_parameter_sliders(self):
        # Очистить предыдущие слайдеры
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        
        dist_name = self.dist_var.get()
        params = self.default_params[dist_name]
        
        self.sliders = {}
        
        for i, (param_name, default_value) in enumerate(params.items()):
            # Фрейм для одного параметра
            param_row = ttk.Frame(self.param_frame)
            param_row.pack(fill=tk.X, pady=5)
            
            # Метка параметра
            ttk.Label(param_row, text=f"{param_name}:", width=15, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 10))
            
            # Диапазон для слайдера
            if dist_name == "Равномерное":
                min_val, max_val = (-5, 10) if param_name == "loc" else (0.1, 5)
            elif dist_name == "Экспоненциальное":
                min_val, max_val = (0.1, 5)
            elif dist_name == "Нормальное":
                min_val, max_val = (-5, 5) if param_name == "loc" else (0.1, 3)
            elif dist_name == "Бета":
                min_val, max_val = (0.1, 10)
            
            # Создать слайдер
            var = tk.DoubleVar(value=default_value)
            slider = ttk.Scale(param_row, from_=min_val, to=max_val, 
                               variable=var, orient=tk.HORIZONTAL, length=200)
            slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            
            # Метка с текущим значением
            value_label = ttk.Label(param_row, text=f"{default_value:.2f}", width=8)
            value_label.pack(side=tk.LEFT, padx=5)
            
            def update_label(val, label=value_label, var=var):
                label.config(text=f"{var.get():.2f}")
            
            slider.configure(command=update_label)
            
            self.sliders[param_name] = {"var": var, "label": value_label}
    
    def on_distribution_change(self, event=None):
        self.create_parameter_sliders()
        self.update_info_text()
        self.update_plots()
    
    def get_current_parameters(self):
        dist_name = self.dist_var.get()
        params = {}
        
        for param_name in self.default_params[dist_name].keys():
            params[param_name] = self.sliders[param_name]["var"].get()
        
        return params
    
    def update_info_text(self):
        dist_name = self.dist_var.get()
        info = ""
        
        if dist_name == "Равномерное":
            a = self.sliders["loc"]["var"].get()
            b = a + self.sliders["scale"]["var"].get()
            info = f"""РАВНОМЕРНОЕ РАСПРЕДЕЛЕНИЕ U({a:.2f}, {b:.2f})

Плотность вероятности:
f(x) = 1/({b-a:.2f}),  x принадлежит [{a:.2f}, {b:.2f}]
f(x) = 0,           x не принадлежит [{a:.2f}, {b:.2f}]

Числовые характеристики:
M(X) = (a+b)/2 = {((a+b)/2):.4f}
D(X) = (b-a)²/12 = {((b-a)**2/12):.4f}
σ(X) = √D(X) = {np.sqrt((b-a)**2/12):.4f}"""
        
        elif dist_name == "Экспоненциальное":
            scale = self.sliders["scale"]["var"].get()
            lmbda = 1/scale
            info = f"""ЭКСПОНЕНЦИАЛЬНОЕ РАСПРЕДЕЛЕНИЕ Exp(λ)

Параметр интенсивности:
λ = 1/scale = {lmbda:.4f}

Плотность вероятности:
f(x) = {lmbda:.4f}·e^(-{lmbda:.4f}x),  x ≥ 0
f(x) = 0,                              x < 0

Числовые характеристики:
M(X) = 1/λ = {scale:.4f}
D(X) = 1/λ² = {scale**2:.4f}
σ(X) = √D(X) = {scale:.4f}"""
        
        elif dist_name == "Нормальное":
            loc = self.sliders["loc"]["var"].get()
            scale = self.sliders["scale"]["var"].get()
            info = f"""НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ N(μ, σ²)

Параметры:
μ = {loc:.2f}, σ = {scale:.2f}

Плотность вероятности:
f(x) = 1/({scale:.2f}·√(2π))·e^(-(x-{loc:.2f})²/(2·{scale:.2f}²))

Числовые характеристики:
M(X) = μ = {loc:.2f}
D(X) = σ² = {scale**2:.4f}
σ(X) = σ = {scale:.2f}"""
        
        elif dist_name == "Бета":
            a = self.sliders["a"]["var"].get()
            b = self.sliders["b"]["var"].get()
            mean = a/(a+b)
            var = (a*b)/((a+b)**2*(a+b+1))
            std = np.sqrt(var)
            info = f"""БЕТА-РАСПРЕДЕЛЕНИЕ Beta(α, β)

Параметры формы:
α = {a:.2f}, β = {b:.2f}

Плотность вероятности:
f(x) = x^{a-1:.2f}(1-x)^{b-1:.2f}/B({a:.2f},{b:.2f}),  x принадлежит [0,1]
f(x) = 0,                                              x не принадлежит [0,1]

где B(α,β) = Γ(α)Γ(β)/Γ(α+β) - бета-функция

Числовые характеристики:
M(X) = α/(α+β) = {mean:.4f}
D(X) = αβ/[(α+β)²(α+β+1)] = {var:.6f}
σ(X) = √D(X) = {std:.4f}"""
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
    
    def update_plots(self):
        dist_name = self.dist_var.get()
        dist_class = self.distributions[dist_name]
        params = self.get_current_parameters()
        
        # Очистить графики
        self.ax1.clear()
        self.ax2.clear()
        
        # Плотность и гистограмма выборки
        self.plot_pdf_histogram(dist_class, dist_name, params)
        
        # Функция распределения
        self.plot_cdf(dist_class, dist_name, params)
        
        self.canvas.draw()
        self.update_info_text()
        
        # Обновить область прокрутки
        self.canvas_main.update_idletasks()
        self.canvas_main.config(scrollregion=self.canvas_main.bbox("all"))
    
    def plot_pdf_histogram(self, dist_class, dist_name, params):
        # Выборка
        sample_size = 1_000_000
        dist = dist_class(**params)
        sample = dist.rvs(size=sample_size)
        
        # Диапазон для графика
        if dist_name == "Бета":
            x_min, x_max = 0, 1
        elif dist_name == "Экспоненциальное":
            x_min, x_max = 0, np.percentile(sample, 99.9)
        elif dist_name == "Равномерное":
            x_min, x_max = params["loc"] - 0.5, params["loc"] + params["scale"] + 0.5
        else:  # Нормальное
            x_min, x_max = params["loc"] - 4*params["scale"], params["loc"] + 4*params["scale"]
        
        x = np.linspace(x_min, x_max, 1000)
        
        # Гистограмма
        self.ax1.hist(sample, bins=50, density=True, alpha=0.6, 
                     color='skyblue', edgecolor='black', label='Выборка')
        
        # Теоретическая плотность
        self.ax1.plot(x, dist.pdf(x), 'r-', linewidth=2, label='Теоретическая плотность')
        
        # Теоретические характеристики
        mean = dist.mean()
        std = dist.std()
        self.ax1.axvline(x=mean, color='green', linestyle='--', 
                        linewidth=2, label=f'M(X) = {mean:.3f}')
        self.ax1.axvspan(mean-std, mean+std, alpha=0.2, color='yellow',
                        label=f'±σ = [{mean-std:.2f}, {mean+std:.2f}]')
        
        self.ax1.set_title(f"{dist_name} распределение\nПлотность и гистограмма (n={sample_size})", fontsize=12, fontweight='bold')
        self.ax1.set_xlabel("x", fontsize=10)
        self.ax1.set_ylabel("Плотность f(x)", fontsize=10)
        self.ax1.legend(loc='upper right', fontsize=9)
        self.ax1.grid(True, alpha=0.3)
        
        # Отступы
        self.ax1.set_xlim(x_min, x_max)
    
    def plot_cdf(self, dist_class, dist_name, params):
        dist = dist_class(**params)
        
        # Диапазон x
        if dist_name == "Бета":
            x = np.linspace(0, 1, 1000)
        elif dist_name == "Экспоненциальное":
            x = np.linspace(0, 10, 1000)
        elif dist_name == "Равномерное":
            x = np.linspace(params["loc"] - 1, params["loc"] + params["scale"] + 1, 1000)
        else:  # Нормальное
            x = np.linspace(params["loc"] - 4*params["scale"], 
                           params["loc"] + 4*params["scale"], 1000)
        
        # Теоретическая функция распределения
        self.ax2.plot(x, dist.cdf(x), 'b-', linewidth=2, label='Теоретическая F(x)')
        
        # Эмпирическая функция распределения
        sample = dist.rvs(size=1000)
        sorted_sample = np.sort(sample)
        ecdf = np.arange(1, len(sorted_sample) + 1) / len(sorted_sample)
        self.ax2.step(sorted_sample, ecdf, 'r-', alpha=0.7, linewidth=1.5, label='Эмпирическая F(x)')
        
        # Квантили
        for q in [0.25, 0.5, 0.75]:
            xq = dist.ppf(q)
            self.ax2.axvline(x=xq, color='gray', linestyle=':', alpha=0.5, linewidth=1)
            self.ax2.text(xq, q, f'  q={q}', va='center', fontsize=9, backgroundcolor='white')
        
        self.ax2.set_title("Функция распределения", fontsize=12, fontweight='bold')
        self.ax2.set_xlabel("x", fontsize=10)
        self.ax2.set_ylabel("F(x)", fontsize=10)
        self.ax2.legend(loc='upper left', fontsize=9)
        self.ax2.grid(True, alpha=0.3)
        
        # Отступы
        self.ax2.set_xlim(x[0], x[-1])
        self.ax2.set_ylim(-0.05, 1.05)

def main():
    root = tk.Tk()
    app = DistributionExplorer(root)
    root.mainloop()

if __name__ == "__main__":
    main()