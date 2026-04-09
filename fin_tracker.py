import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from datetime import datetime

# Intentamos importar matplotlib. Si no está instalado, el programa no se colgará,
# pero avisará al usuario cuando intente usar la función de gráficos.
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import numpy as np # Necesario para agrupar barras
    MATPLOTLIB_DISPONIBLE = True
except ImportError:
    MATPLOTLIB_DISPONIBLE = False

class AppFinanzas:
    def __init__(self, root):
        self.root = root
        self.root.title("Mis Finanzas Personales - Gráfico de Ingresos y Gastos")
        self.root.geometry("600x800") # He ampliado un poco el alto

        self.archivo_datos = "finanzas.json"
        self.datos = [] # Aquí guardaremos todos los datos en memoria
        self.meses_disponibles = ["Todos"] # Para el filtro

        # ==========================================
        # 1. SECCIÓN DE ENTRADA (FORMULARIO)
        # ==========================================
        marco_entrada = tk.LabelFrame(self.root, text="Añadir Movimiento", padx=10, pady=10)
        marco_entrada.pack(padx=20, pady=10, fill="x")

        # Fila 0: Mes
        tk.Label(marco_entrada, text="Mes (AÑO-MES):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_mes = tk.Entry(marco_entrada)
        self.entry_mes.grid(row=0, column=1, padx=5, pady=5)
        self.entry_mes.insert(0, datetime.now().strftime("%Y-%m"))

        # Fila 1: Importe
        tk.Label(marco_entrada, text="Importe (€):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_importe = tk.Entry(marco_entrada)
        self.entry_importe.grid(row=1, column=1, padx=5, pady=5)

        # Fila 2: Categoría
        tk.Label(marco_entrada, text="Categoría:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        categorias = ["Comida", "Sueldo", "Alquiler/Hipoteca", "Ocio", "Facturas", "Otros"]
        self.combo_categoria = ttk.Combobox(marco_entrada, values=categorias, state="readonly")
        self.combo_categoria.grid(row=2, column=1, padx=5, pady=5)
        self.combo_categoria.current(0)

        # Fila 3: Tipo
        tk.Label(marco_entrada, text="Tipo:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.tipo_var = tk.StringVar(value="Gasto")
        marco_radios = tk.Frame(marco_entrada)
        marco_radios.grid(row=3, column=1, sticky="w")
        tk.Radiobutton(marco_radios, text="Gasto", variable=self.tipo_var, value="Gasto").pack(side="left")
        tk.Radiobutton(marco_radios, text="Ingreso", variable=self.tipo_var, value="Ingreso").pack(side="left")

        # Botón para guardar
        self.btn_guardar = tk.Button(marco_entrada, text="Añadir Transacción", command=self.agregar_transaccion, bg="#4CAF50", fg="white")
        self.btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

        # ==========================================
        # 2. SECCIÓN DE FILTRO Y RESUMEN
        # ==========================================
        marco_filtro = tk.Frame(self.root)
        marco_filtro.pack(pady=5)

        tk.Label(marco_filtro, text="Ver datos de:").pack(side="left", padx=5)
        self.combo_filtro_mes = ttk.Combobox(marco_filtro, values=self.meses_disponibles, state="readonly")
        self.combo_filtro_mes.pack(side="left", padx=5)
        self.combo_filtro_mes.current(0)
        self.combo_filtro_mes.bind("<<ComboboxSelected>>", lambda e: self.actualizar_vista())

        self.etiqueta_balance = tk.Label(self.root, text="Balance: 0.00 €", font=("Arial", 14, "bold"))
        self.etiqueta_balance.pack(pady=5)

        # Botón para ver gráficos (TEXTO ACTUALIZADO)
        self.btn_grafico = tk.Button(self.root, text="📊 Ver Balance Gráfico", command=self.mostrar_grafico, bg="#2196F3", fg="white")
        self.btn_grafico.pack(pady=5)

        # ==========================================
        # 3. SECCIÓN DE CONSULTA (TABLA)
        # ==========================================
        marco_tabla = tk.LabelFrame(self.root, text="Historial de Movimientos", padx=10, pady=10)
        marco_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        columnas = ("mes", "importe", "categoria", "tipo")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        self.tabla.heading("mes", text="Mes")
        self.tabla.heading("importe", text="Importe (€)")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("tipo", text="Tipo")

        self.tabla.column("mes", width=80, anchor="center")
        self.tabla.column("importe", width=100, anchor="center")
        self.tabla.column("categoria", width=150, anchor="center")
        self.tabla.column("tipo", width=100, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        self.btn_eliminar = tk.Button(self.root, text="Eliminar Seleccionado", command=self.eliminar_transaccion, bg="#f44336", fg="white")
        self.btn_eliminar.pack(pady=10)

        # ==========================================
        # 4. CARGAR DATOS AL INICIAR
        # ==========================================
        self.cargar_datos()

    # --- LÓGICA DE DATOS ---

    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, "r", encoding="utf-8") as f:
                    self.datos = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar los datos: {e}")
                self.datos = []
        self.actualizar_vista()

    def guardar_datos(self):
        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(self.datos, f, indent=4, ensure_ascii=False)

    # --- LÓGICA DE INTERFAZ ---

    def actualizar_vista(self):
        # 1. Limpiar la tabla actual
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # 2. Actualizar la lista de meses disponibles en el filtro
        meses_unicos = set()
        for mov in self.datos:
            mes = mov.get("mes", "Desconocido")
            meses_unicos.add(mes)

        self.meses_disponibles = ["Todos"] + sorted(list(meses_unicos))
        mes_seleccionado = self.combo_filtro_mes.get()
        self.combo_filtro_mes.config(values=self.meses_disponibles)
        if mes_seleccionado not in self.meses_disponibles:
            self.combo_filtro_mes.current(0)
            mes_seleccionado = "Todos"

        # 3. Filtrar datos, rellenar tabla y calcular balance
        balance_actual = 0.0

        for i, mov in enumerate(self.datos):
            mes = mov.get("mes", "Desconocido")
            if mes_seleccionado == "Todos" or mes == mes_seleccionado:
                self.tabla.insert("", "end", iid=str(i), values=(mes, f"{mov['importe']:.2f}", mov['categoria'], mov['tipo']))

                if mov['tipo'] == "Ingreso":
                    balance_actual += mov['importe']
                else:
                    balance_actual -= mov['importe']

        # 4. Actualizar etiqueta de balance
        color_balance = "red" if balance_actual < 0 else "black"
        self.etiqueta_balance.config(text=f"Balance ({mes_seleccionado}): {balance_actual:.2f} €", fg=color_balance)

    def agregar_transaccion(self):
        mes = self.entry_mes.get().strip()
        importe_str = self.entry_importe.get()
        categoria = self.combo_categoria.get()
        tipo = self.tipo_var.get()

        if not mes:
            messagebox.showwarning("Aviso", "Por favor, introduce un mes.")
            return

        try:
            importe = float(importe_str)
            if importe <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Introduce un importe numérico válido.")
            return

        nuevo_movimiento = {
            "mes": mes,
            "importe": importe,
            "categoria": categoria,
            "tipo": tipo
        }

        self.datos.append(nuevo_movimiento)
        self.guardar_datos()
        self.actualizar_vista()
        self.entry_importe.delete(0, tk.END)

    def eliminar_transaccion(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un movimiento para eliminar.")
            return

        respuesta = messagebox.askyesno("Confirmar", "¿Eliminar este movimiento?")
        if respuesta:
            indice_real = int(seleccion[0])
            self.datos.pop(indice_real)
            self.guardar_datos()
            self.actualizar_vista()

    # --- LÓGICA DE GRÁFICOS (ACTUALIZADA) ---

    def mostrar_grafico(self):
        if not MATPLOTLIB_DISPONIBLE:
            messagebox.showerror("Error", "La librería 'matplotlib' o 'numpy' no está instalada.\nAbre tu terminal y ejecuta: pip install matplotlib numpy")
            return

        mes_seleccionado = self.combo_filtro_mes.get()

        # Agrupar los gastos e ingresos por categoría para el mes seleccionado
        resumen_gastos = {}
        resumen_ingresos = {}
        # Mantenemos un set de todas las categorías que aparecen
        todas_categorias = set()

        for mov in self.datos:
            mes = mov.get("mes", "Desconocido")
            if (mes_seleccionado == "Todos" or mes == mes_seleccionado):
                cat = mov['categoria']
                todas_categorias.add(cat)
                if mov['tipo'] == "Gasto":
                    resumen_gastos[cat] = resumen_gastos.get(cat, 0) + mov['importe']
                elif mov['tipo'] == "Ingreso":
                    resumen_ingresos[cat] = resumen_ingresos.get(cat, 0) + mov['importe']

        if not todas_categorias:
            messagebox.showinfo("Sin datos", f"No hay datos registrados en {mes_seleccionado} para graficar.")
            return

        # Ordenar categorías para que siempre salgan en el mismo orden
        categorias_ordenadas = sorted(list(todas_categorias))

        # Preparar los datos para las barras (si una categoría no tiene ingreso/gasto, ponemos 0)
        valores_gastos = [resumen_gastos.get(cat, 0) for cat in categorias_ordenadas]
        valores_ingresos = [resumen_ingresos.get(cat, 0) for cat in categorias_ordenadas]

        # Crear una nueva ventana emergente para el gráfico
        ventana_grafico = tk.Toplevel(self.root)
        ventana_grafico.title(f"Balance Gráfico - {mes_seleccionado}")
        ventana_grafico.geometry("600x500")

        # Configuración del gráfico de barras agrupadas con Matplotlib
        figura, ax = plt.subplots(figsize=(6, 5))

        # Posiciones de las categorías en el eje X
        indices = np.arange(len(categorias_ordenadas))
        ancho_barra = 0.35 # Ancho de cada barra individual

        # Dibujar las barras de INGRESOS (Verde) y GASTOS (Rojo)
        barra_ingresos = ax.bar(indices, valores_ingresos, ancho_barra, label='Ingresos', color='#4CAF50') # Verde
        barra_gastos = ax.bar(indices + ancho_barra, valores_gastos, ancho_barra, label='Gastos', color='#f44336') # Rojo

        # Configurar etiquetas y ejes
        ax.set_ylabel('Importe (€)')
        ax.set_title(f"Ingresos vs Gastos por Categoría ({mes_seleccionado})")
        ax.set_xticks(indices + ancho_barra / 2) # Centrar etiquetas entre las dos barras
        ax.set_xticklabels(categorias_ordenadas, rotation=15, ha="right") # Rotar etiquetas para leer mejor
        ax.legend() # Mostrar la leyenda (cuál es cuál)
        ax.grid(axis='y', linestyle='--', alpha=0.7) # Añadir líneas de cuadrícula horizontales

        # Añadir etiquetas de valor encima de cada barra
        def añadir_etiquetas(barras):
            for barra in barras:
                alto = barra.get_height()
                if alto > 0:
                    ax.annotate(f'{alto:.0f}€',
                                xy=(barra.get_x() + barra.get_width() / 2, alto),
                                xytext=(0, 3), # Desplazamiento de 3 puntos hacia arriba
                                textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)

        añadir_etiquetas(barra_ingresos)
        añadir_etiquetas(barra_gastos)

        plt.tight_layout() # Ajustar diseño para que no se corten las etiquetas

        # Integrar la figura de Matplotlib en la ventana de Tkinter
        canvas = FigureCanvasTkAgg(figura, master=ventana_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AppFinanzas(ventana_principal)
    ventana_principal.mainloop()
