import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

class AppFinanzas:
    def __init__(self, root):
        self.root = root
        self.root.title("Mis Finanzas Personales")
        self.root.geometry("500x650") # He ampliado un poco el alto para el nuevo botón

        self.balance_total = 0.0
        self.archivo_datos = "finanzas.json"

        # ==========================================
        # 1. SECCIÓN DE ENTRADA (FORMULARIO)
        # ==========================================
        marco_entrada = tk.LabelFrame(self.root, text="Añadir Movimiento", padx=10, pady=10)
        marco_entrada.pack(padx=20, pady=10, fill="x")

        tk.Label(marco_entrada, text="Importe (€):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_importe = tk.Entry(marco_entrada)
        self.entry_importe.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(marco_entrada, text="Categoría:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        categorias = ["Comida", "Sueldo", "Alquiler/Hipoteca", "Ocio", "Facturas", "Otros"]
        self.combo_categoria = ttk.Combobox(marco_entrada, values=categorias, state="readonly")
        self.combo_categoria.grid(row=1, column=1, padx=5, pady=5)
        self.combo_categoria.current(0)

        tk.Label(marco_entrada, text="Tipo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.tipo_var = tk.StringVar(value="Gasto")
        marco_radios = tk.Frame(marco_entrada)
        marco_radios.grid(row=2, column=1, sticky="w")
        tk.Radiobutton(marco_radios, text="Gasto", variable=self.tipo_var, value="Gasto").pack(side="left")
        tk.Radiobutton(marco_radios, text="Ingreso", variable=self.tipo_var, value="Ingreso").pack(side="left")

        self.btn_guardar = tk.Button(marco_entrada, text="Añadir Transacción", command=self.agregar_transaccion, bg="#4CAF50", fg="white")
        self.btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

        # ==========================================
        # 2. SECCIÓN DE RESUMEN (BALANCE)
        # ==========================================
        self.etiqueta_balance = tk.Label(self.root, text="Balance Total: 0.00 €", font=("Arial", 14, "bold"))
        self.etiqueta_balance.pack(pady=10)

        # ==========================================
        # 3. SECCIÓN DE CONSULTA (TABLA)
        # ==========================================
        marco_tabla = tk.LabelFrame(self.root, text="Historial de Movimientos", padx=10, pady=10)
        marco_tabla.pack(padx=20, pady=10, fill="both", expand=True)

        columnas = ("importe", "categoria", "tipo")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings")
        self.tabla.heading("importe", text="Importe (€)")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("tipo", text="Tipo")

        self.tabla.column("importe", width=100, anchor="center")
        self.tabla.column("categoria", width=150, anchor="center")
        self.tabla.column("tipo", width=100, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        # NUEVO: Botón para eliminar la fila seleccionada
        self.btn_eliminar = tk.Button(self.root, text="Eliminar Seleccionado", command=self.eliminar_transaccion, bg="#f44336", fg="white")
        self.btn_eliminar.pack(pady=10)

        # ==========================================
        # 4. CARGAR DATOS AL INICIAR
        # ==========================================
        self.cargar_datos()

    def actualizar_balance_ui(self):
        color_balance = "red" if self.balance_total < 0 else "black"
        self.etiqueta_balance.config(text=f"Balance Total: {self.balance_total:.2f} €", fg=color_balance)

    def cargar_datos(self):
        if not os.path.exists(self.archivo_datos):
            return

        try:
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                datos = json.load(f)

                for movimiento in datos:
                    self.tabla.insert("", "end", values=(f"{movimiento['importe']:.2f}", movimiento['categoria'], movimiento['tipo']))

                    if movimiento['tipo'] == "Ingreso":
                        self.balance_total += movimiento['importe']
                    else:
                        self.balance_total -= movimiento['importe']

                self.actualizar_balance_ui()
        except Exception as e:
            messagebox.showerror("Error de carga", f"No se pudieron cargar los datos: {e}")

    def guardar_en_archivo(self, importe, categoria, tipo):
        datos = []
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                datos = json.load(f)

        nuevo_movimiento = {
            "importe": importe,
            "categoria": categoria,
            "tipo": tipo
        }
        datos.append(nuevo_movimiento)

        with open(self.archivo_datos, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def agregar_transaccion(self):
        importe_str = self.entry_importe.get()
        categoria = self.combo_categoria.get()
        tipo = self.tipo_var.get()

        try:
            importe = float(importe_str)
            if importe <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce un importe numérico válido y mayor que cero.")
            return

        self.tabla.insert("", "end", values=(f"{importe:.2f}", categoria, tipo))

        if tipo == "Ingreso":
            self.balance_total += importe
        else:
            self.balance_total -= importe
        self.actualizar_balance_ui()

        self.guardar_en_archivo(importe, categoria, tipo)
        self.entry_importe.delete(0, tk.END)

    # ==========================================
    # NUEVAS FUNCIONES DE ELIMINACIÓN
    # ==========================================
    def eliminar_del_archivo(self, indice):
        """Elimina un movimiento del archivo JSON usando su posición (índice)."""
        if os.path.exists(self.archivo_datos):
            with open(self.archivo_datos, "r", encoding="utf-8") as f:
                datos = json.load(f)

            # Borrar el elemento en el índice indicado
            if 0 <= indice < len(datos):
                datos.pop(indice)

            # Sobrescribir el archivo con el dato ya eliminado
            with open(self.archivo_datos, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def eliminar_transaccion(self):
        """Lógica que se ejecuta al pulsar el botón 'Eliminar Seleccionado'"""
        seleccion = self.tabla.selection() # Obtiene la fila seleccionada

        if not seleccion:
            messagebox.showwarning("Aviso", "Por favor, selecciona un movimiento de la tabla para eliminarlo.")
            return

        # Confirmación para evitar borrados por accidente
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este movimiento?")

        if respuesta:
            item_id = seleccion[0] # Cogemos el ID de la fila seleccionada
            indice = self.tabla.index(item_id) # Averiguamos qué posición (0, 1, 2...) ocupa en la tabla

            # 1. Recuperar los valores para deshacer el balance
            valores = self.tabla.item(item_id, "values")
            importe = float(valores[0])
            tipo = valores[2]

            if tipo == "Ingreso":
                self.balance_total -= importe # Si era ingreso, lo restamos
            else:
                self.balance_total += importe # Si era gasto, devolvemos el dinero

            self.actualizar_balance_ui()

            # 2. Borrar de la tabla visual
            self.tabla.delete(item_id)

            # 3. Borrar del archivo JSON permanentemente
            self.eliminar_del_archivo(indice)

if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = AppFinanzas(ventana_principal)
    ventana_principal.mainloop()
