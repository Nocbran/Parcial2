import itertools
import tkinter as tk
from tkinter import messagebox, simpledialog

class Calificacion:
    def __init__(self,cultura,proyeccion,entrevista):
        self.cultura = cultura
        self.proyeccion = proyeccion
        self.entrevista = entrevista

    def promedio(self):
        return (self.cultura + self.proyeccion + self.entrevista) / 3


class Concurso:
    def __init__(self):
        self.candidatas = {}
        self.jurados = {}

    def RegistrarCandidata(self, codigo,nombre,edad,institucion,municiopio):
        self.candidatas[codigo] = {
            "nombre" : nombre,
            "edad" : edad,
            "institucion" : institucion,
            "municipio" : municiopio,
            "calificaciones" : []
        }

    def RegistrarJurado(self,nombre,especialidad):
        self.jurados[nombre] = {"especialidad":especialidad}

    def AgregarCalificacion(self,codigo,cultura,proyeccion,entrevista):
        if codigo in self.candidatas:
            cal = Calificacion(cultura,proyeccion,entrevista)
            self.candidatas[codigo]["calificaciones"].append(cal)

    def PuntajeFinal(self,codigo):
        calificaciones = self.candidatas[codigo]["calificaciones"]
        if not calificaciones:
            return 0
        return sum(i.promedio() for i in calificaciones) / len(calificaciones)

    def Ranking(self):
        return sorted(self.candidatas.items(),
                      key = lambda  i: self.PuntajeFinal(i[0]),
                      reverse=True)

    def GuardarCandidata(self,archivo="candidatas.txt"):
        with open(archivo, "w", encoding="utf-8") as arch:
            for codigo,datos in self.candidatas.items():
                arch.write(f"{codigo}:{datos['nombre']}:{datos['edad']}:{datos['institucion']}:{datos['municipio']}\n")
                for cal in datos["calificaciones"]:
                    arch.write(f"CAL:{codigo}:{cal.cultura}:{cal.proyeccion}:{cal.entrevista}\n")

            for nombre,datos in self.jurados.items():
                arch.write(f"JUR:{nombre}:{datos['especialidad']}\n")

    def CargarCandidata(self,archivo="candidatas.txt"):
        try:
            self.candidatas = {}
            self.jurados = {}

            with open(archivo, "r", encoding="utf-8") as arch:
                for linea in arch:
                    linea = linea.strip()
                    if not linea:
                        continue

                    partes = linea.split(":")
                    if linea.startswith("CAL:"):
                        _,codigo,cultura,proyeccion,entrevista = partes
                        self.AgregarCalificacion(codigo, int(cultura),int(proyeccion), int(entrevista))

                    elif linea.startswith("JUR:"):
                        _, nombre,especialidad = partes
                        self.RegistrarCandidata(nombre , especialidad)

                    else:
                        codigo,nombre,edad,institucion,municipio = partes
                        self.RegistrarCandidata(codigo,nombre,edad,institucion,municipio)
        except FileNotFoundError:
            messagebox.showerror("Error,"f"No existe el archivo {archivo}")


class Jurado:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad



class VentanaEntrada(tk.Toplevel):
    def __init__(self, parent, titulo, campos):
        super()._init_(parent)
        self.title(titulo)
        self.resultados = {}
        self.entradas = {}

        for campo in campos:
            tk.Label(self, text=campo + ":").pack(pady=2)
            entry = tk.Entry(self)
            entry.pack(pady=2)
            self.entradas[campo] = entry

        tk.Button(self, text="Aceptar", command=self.guardar).pack(pady=5)
        tk.Button(self, text="Cancelar", command=self.destroy).pack(pady=5)

        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def guardar(self):
        for campo, entry in self.entradas.items():
            self.resultados[campo] = entry.get()
        self.destroy()


class App:
    def __init__(self, ventana, concurso):
        self.ventana = ventana
        self.concurso = concurso
        ventana.title("Concurso de Candidatas")
        ventana.geometry("500x400")

        tk.Button(ventana, text="Registrar Candidata", command=self.registrar_candidata).pack(pady=5)
        tk.Button(ventana, text="Registrar Jurado", command=self.registrar_jurado).pack(pady=5)
        tk.Button(ventana, text="Agregar Calificación", command=self.agregar_calificacion).pack(pady=5)
        tk.Button(ventana, text="Mostrar Ranking", command=self.mostrar_ranking).pack(pady=5)

    def registrar_candidata(self):
        campos = ["Código", "Nombre", "Edad", "Institución", "Municipio"]
        ventana = VentanaEntrada(self.root, "Registrar Candidata", campos)
        datos = ventana.resultados
        if datos.get("Código") and datos.get("Nombre"):
            try:
                edad = int(datos.get("Edad"))
            except:
                edad = 0
            candidata = Candidata(datos["Código"], datos["Nombre"], edad,
                                  datos.get("Institución",""), datos.get("Municipio",""))
            self.concurso.registrar_candidata(candidata)
            messagebox.showinfo("Éxito", f"Candidata {datos['Nombre']} registrada.")

    def registrar_jurado(self):
        campos = ["Nombre", "Especialidad"]
        ventana = VentanaEntrada(self.root, "Registrar Jurado", campos)
        datos = ventana.resultados
        if datos.get("Nombre"):
            jurado = Jurado(datos["Nombre"], datos.get("Especialidad",""))
            self.concurso.registrar_jurado(jurado)
            messagebox.showinfo("Éxito", f"Jurado {datos['Nombre']} registrado.")

    def agregar_calificacion(self):
        if not self.concurso.candidatas:
            messagebox.showwarning("Atención","No hay candidatas registradas.")
            return

        cod_ventana = VentanaEntrada(self.root, "Calificación", ["Código de Candidata"])
        codigo = cod_ventana.resultados.get("Código de Candidata")
        candidata = next((c for c in self.concurso.candidatas if c.codigo == codigo), None)
        if not candidata:
            messagebox.showerror("Error", "Candidata no encontrada.")
            return

        campos = ["Cultura (0-100)", "Proyección (0-100)", "Entrevista (0-100)"]
        cal_ventana = VentanaEntrada(self.root, f"Calificar {candidata.nombre}", campos)
        datos = cal_ventana.resultados
        try:
            cultura = int(datos.get(campos[0],0))
            proyeccion = int(datos.get(campos[1],0))
            entrevista = int(datos.get(campos[2],0))
        except:
            cultura = proyeccion = entrevista = 0
        cal = Calificacion(cultura, proyeccion, entrevista)
        candidata.agregar_calificacion(cal)
        messagebox.showinfo("Éxito", f"Calificación registrada para {candidata.nombre}.")

    def mostrar_ranking(self):
        ranking = self.concurso.ranking()
        if not ranking:
            messagebox.showinfo("Ranking", "No hay candidatas registradas.")
            return
        texto = "\n".join([f"{i+1}. {c.nombre} - Puntaje: {c.puntaje_final():.2f}"
                           for i, c in enumerate(ranking)])
        messagebox.showinfo("Ranking", texto)


if __name__ == "_main_":
    concurso = Concurso()
    ventana = tk.Tk()
    app = App(ventana, concurso)
    ventana.mainloop()
