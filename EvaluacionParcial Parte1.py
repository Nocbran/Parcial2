import tkinter as tk
from tkinter import messagebox

class Calificacion:
    def __init__(self, cultura, proyeccion, entrevista):
        self.cultura = cultura
        self.proyeccion = proyeccion
        self.entrevista = entrevista

    def promedio(self):
        return (self.cultura + self.proyeccion + self.entrevista) / 3


class Concurso:
    def __init__(self, nombre, fecha):
        self.nombre = nombre
        self.fecha = fecha
        self.candidatas = {}
        self.jurados = {}

    def RegistrarCandidata(self, codigo, nombre, edad, institucion, municipio):
        if codigo in self.candidatas:
            raise ValueError(f"El código {codigo} ya está registrado")
        self.candidatas[codigo] = {
            "nombre": nombre,
            "edad": edad,
            "institucion": institucion,
            "municipio": municipio,
            "calificaciones": []
        }

    def RegistrarJurado(self, nombre, especialidad):
        if nombre in self.jurados:
            raise ValueError(f"El jurado {nombre} ya está registrado")
        self.jurados[nombre] = {"especialidad": especialidad}

    def AgregarCalificacion(self, codigo, cultura, proyeccion, entrevista):
        if codigo not in self.candidatas:
            raise ValueError("Candidata no encontrada")
        cal = Calificacion(cultura, proyeccion, entrevista)
        self.candidatas[codigo]["calificaciones"].append(cal)

    def PuntajeFinal(self, codigo):
        calificaciones = self.candidatas[codigo]["calificaciones"]
        if not calificaciones:
            return 0
        return sum(i.promedio() for i in calificaciones) / len(calificaciones)

    def Ranking(self):
        return sorted(
            self.candidatas.items(),
            key=lambda i: self.PuntajeFinal(i[0]),
            reverse=True
        )


class ConcursoCandidatasApp:
    def __init__(self, concurso):
        self.concurso = concurso
        self.root = tk.Tk()
        self.root.title(concurso.nombre)
        self.root.geometry("600x400")

        self.menu()

        tk.Label(
            self.root,
            text=f"{concurso.nombre}\nFecha: {concurso.fecha}",
            font=("Arial", 12, "bold"),
            justify="center"
        ).pack(pady=50)

        self.root.mainloop()

    def menu(self):
        barra = tk.Menu(self.root)
        opciones = tk.Menu(barra, tearoff=0)
        opciones.add_command(label="Registrar Candidata", command=self.registrar_candidata)
        opciones.add_command(label="Registrar Jurado", command=self.registrar_jurado)
        opciones.add_command(label="Agregar Calificación", command=self.agregar_calificacion)
        opciones.add_command(label="Listar Candidatas", command=self.listar_candidatas)
        opciones.add_command(label="Ver Ranking", command=self.ver_ranking)
        opciones.add_separator()
        opciones.add_command(label="Salir", command=self.root.quit)
        barra.add_cascade(label="Opciones", menu=opciones)
        self.root.config(menu=barra)

    def registrar_candidata(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Candidata")

        campos = ["Código", "Nombre", "Edad", "Institución", "Municipio"]
        entradas = {}
        for campo in campos:
            tk.Label(ventana, text=f"{campo}:").pack()
            entry = tk.Entry(ventana)
            entry.pack()
            entradas[campo] = entry

        def guardar():
            try:
                codigo = entradas["Código"].get().strip()
                nombre = entradas["Nombre"].get().strip()
                edad = int(entradas["Edad"].get().strip() or 0)
                institucion = entradas["Institución"].get().strip()
                municipio = entradas["Municipio"].get().strip()
                self.concurso.RegistrarCandidata(codigo, nombre, edad, institucion, municipio)
                messagebox.showinfo("Éxito", f"Candidata {nombre} registrada")
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)

    def registrar_jurado(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Registrar Jurado")

        tk.Label(ventana, text="Nombre:").pack()
        entry_nombre = tk.Entry(ventana)
        entry_nombre.pack()

        tk.Label(ventana, text="Especialidad:").pack()
        entry_especialidad = tk.Entry(ventana)
        entry_especialidad.pack()

        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                especialidad = entry_especialidad.get().strip()
                self.concurso.RegistrarJurado(nombre, especialidad)
                messagebox.showinfo("Éxito", f"Jurado {nombre} registrado")
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)

    def agregar_calificacion(self):
        if not self.concurso.candidatas:
            messagebox.showwarning("Aviso", "No hay candidatas registradas")
            return

        ventana = tk.Toplevel(self.root)
        ventana.title("Agregar Calificación")

        tk.Label(ventana, text="Código de la Candidata:").pack()
        entry_codigo = tk.Entry(ventana)
        entry_codigo.pack()

        entradas = {}
        for crit in ["Cultura (0-100)", "Proyección (0-100)", "Entrevista (0-100)"]:
            tk.Label(ventana, text=crit).pack()
            entry = tk.Entry(ventana)
            entry.pack()
            entradas[crit] = entry

        def guardar():
            try:
                codigo = entry_codigo.get().strip()
                if codigo not in self.concurso.candidatas:
                    raise ValueError("Candidata no encontrada")
                cultura = int(entradas["Cultura (0-100)"].get().strip())
                proyeccion = int(entradas["Proyección (0-100)"].get().strip())
                entrevista = int(entradas["Entrevista (0-100)"].get().strip())
                self.concurso.AgregarCalificacion(codigo, cultura, proyeccion, entrevista)
                messagebox.showinfo("Éxito", f"Calificación registrada para {self.concurso.candidatas[codigo]['nombre']}")
                ventana.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(ventana, text="Guardar", command=guardar).pack(pady=5)

    def listar_candidatas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Listado de Candidatas")
        if not self.concurso.candidatas:
            tk.Label(ventana, text="No hay candidatas registradas.").pack()
            return
        for codigo, datos in self.concurso.candidatas.items():
            texto = f"{codigo} - {datos['nombre']} | Edad: {datos['edad']} | {datos['institucion']} | {datos['municipio']}"
            tk.Label(ventana, text=texto, anchor="w", justify="left").pack(fill="x", padx=5, pady=2)
            tk.Label(ventana, text="-----------------------------------------").pack()

    def ver_ranking(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Ranking Final")
        ranking = self.concurso.Ranking()
        if not ranking:
            tk.Label(ventana, text="No hay candidatas registradas.").pack()
            return
        tk.Label(ventana, text="Ranking Final (Mayor puntaje a menor):", font=("Arial", 12, "bold")).pack(pady=5)
        for i, (codigo, datos) in enumerate(ranking, start=1):
            tk.Label(
                ventana,
                text=f"{i}. {datos['nombre']} - Puntaje: {self.concurso.PuntajeFinal(codigo):.2f}",
                anchor="w", justify="left"
            ).pack(fill="x", padx=5, pady=2)
            tk.Label(ventana, text="-----------------------------------------").pack()



if __name__ == "__main__":
    concurso = Concurso("Concurso de Candidatas", "2025-09-14")
    ConcursoCandidatasApp(concurso)