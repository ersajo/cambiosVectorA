from threading import Thread
from tkinter import *
from tkinter import messagebox

class GUI:
    tabla_optima = []
    funcion_objetivo = []
    cambios = []
    vectorCambios = []
    etiqueta = []
    label = []
    content = []

    def __init__(self):
        try:
            self.master = Tk()
            self.master.geometry('400x100')
            self.master.title("Cambios en el vector A")

            Label(self.master, text="Variables").place(x=10, y=10)
            Label(self.master, text="Restricciones").place(x=10, y=35)

            self.variables = Entry(self.master, width=3)
            self.restricciones = Entry(self.master, width=3)

            self.variables.place(x=100, y=10)
            self.restricciones.place(x=100, y=35)

            self.variables.focus_set()

            self.botonGenerar = Button(self.master, text="Generar tabla optima vacia", width=25, command=self.generarOptimaNueva).place(x=200, y=10)
            self.var = IntVar()
            self.var.set(1)
            Radiobutton(self.master, text="Minimizar", variable=self.var, value=0, indicatoron=0, command=self.genEtiqueta).place(x=130, y=35)
            Radiobutton(self.master, text="Maximizar", variable=self.var, value=1, indicatoron=0, command=self.genEtiqueta).place(x=130,y=10)
            #self.botonImprimir = Button(self.master, text="Imprimir entradas", width=15, command=self.imprimirEntradas).place(x=200, y=35)
            self.botonCalcular = Button(self.master, text="Calcular cambios", width=15, command=self.calcularCambios).place(x=200, y=35)

        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def calcularCambios(self):
        try:
            i = -1
            flag = False
            res = []
            vectorAux = []
            for renglon in range(len(self.tabla_optima)):
                for columna in range(len(self.tabla_optima[renglon])):
                    i = i + 1
                    if (self.tabla_optima[renglon][columna].get()).find('/') == True:
                        aux = self.tabla_optima[renglon][columna].get().split('/')
                        self.content[i].set(str(int(aux[0]) / int(aux[1])))
            for valor in range(int(self.variables.get()),len(self.tabla_optima[0])-1):
                vectorAux.append(self.tabla_optima[0][valor].get())
            for vector in range(len(self.vectorCambios)):
                res.append(0)
                for cambio in range(len(self.vectorCambios[vector])):
                    res[vector] = res[vector] + (float(vectorAux[cambio]) * float(self.vectorCambios[vector][cambio].get()))
            for r in range(len(res)):
                res[r] = res[r] - (float(self.funcion_objetivo[r].get()))
            for i in range(len(self.cambio)):
                if self.cambio[i].get() == 1:
                    if res[i] > 0:
                        self.content[i].set(str(res[i]))
                        flag = True
                    else:
                        self.content[i].set(str(res[i]))
                        aux = []
                        for renglon in range(1,len(self.tabla_optima)):
                            aux.append([])
                            for valor in range(int(self.variables.get()),len(self.tabla_optima[renglon])-1):
                                aux[renglon-1].append(self.tabla_optima[renglon][valor].get())
                        for renglon in range(len(aux)):
                            sal = 0
                            for valor in range(len(aux[renglon])):
                                sal = sal + (float(aux[renglon][valor]) * float(self.vectorCambios[i][valor].get()))
                            self.content[((1+int(self.restricciones.get())+int(self.variables.get()))*(renglon+1))+i].set(str(sal))
                        self.simplex()
                        flag = True
            if flag == True:
                messagebox.showinfo("Listo", "Cambios en el vector A realizados")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def simplex(self):
        try:
            while True:
                aux = ""
                indices = []
                indices.clear()
                for valor in range(len(self.tabla_optima[0])):
                    if float(self.tabla_optima[0][valor].get()) < 0:
                        indices.append(valor)
                        aux = aux + "1"
                    else:
                        aux = aux + "0"
                if "1" not in aux:
                    break
                else:
                    cp = 0
                    for indice in indices:
                        if float(self.tabla_optima[0][indice].get()) < cp:
                            cp = indice
                    rp = 1
                    for renglon in range(1, len(self.tabla_optima) - 1):
                        a = float(self.tabla_optima[renglon][int(self.restricciones.get()) + int(self.variables.get())].get()) / float(self.tabla_optima[renglon][indice].get())
                        b = float(self.tabla_optima[renglon + 1][int(self.restricciones.get()) + int(self.variables.get())].get()) / float(self.tabla_optima[renglon + 1][indice].get())
                        if self.var.get() == 1:#Maximizar
                            if b < a and b < 0:
                                rp = renglon + 1
                        elif self.var.get() == 0:#Minimizar
                            if b > a and b > a:
                                rp = renglon + 1
                    factor =  float(self.tabla_optima[rp][cp].get())
                    r = int(self.restricciones.get())
                    v = int(self.variables.get())
                    for columna in range(len(self.tabla_optima[rp])):
                        res = float(self.tabla_optima[rp][columna].get())/factor
                        self.content[((1 + r + v)*rp)+columna].set(str(res))
                    for renglon in range(len(self.tabla_optima)):
                        if renglon != rp:
                            factor = float(self.tabla_optima[renglon][cp].get())
                            for columna in range(len(self.tabla_optima[renglon])):
                                res = float(self.tabla_optima[renglon][columna].get()) - (float(self.tabla_optima[rp][columna].get()) * factor)
                                self.content[((1 + r + v) * renglon) + columna].set(str(res))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

            #for renglon in self.tabla_optima:#Calculos
            #    print(renglon)

    def genEtiqueta(self):
        try:
            if self.var.get() == 1:
                Label(self.master, text="Max Z = ").place(x=40, y=65)
            elif self.var.get() == 0:
                Label(self.master, text="Min Z = ").place(x=40, y=65)
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def callback(self):
        try:
            print("Variables: {}\nRestricciones: {}".format(self.variables.get(), self.restricciones.get()))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def generarOptimaNueva(self):
        try:
            self.genEtiqueta()
            self.cambio = []
            #cambio en la etiqueta de las restriciones en la tabla optima
            if len(self.label) != 0:
                for label in self.label:
                    label.place_forget()
                self.label.clear()
            #Cambio de la etiqueta de la tabla optima
            if len(self.etiqueta) != 0:
                for etiqueta in self.etiqueta:
                    etiqueta.place_forget()
                self.etiqueta.clear()
            #Limpieza de los campos de la tabla optima
            if len(self.tabla_optima) != 0:
                for renglon in range(len(self.tabla_optima)):
                    for columna in range(len(self.tabla_optima[renglon])):
                        self.tabla_optima[renglon][columna].place_forget()
                self.tabla_optima.clear()

            #Limpieza de los campos de la funcion objetivo y el vector de los CheckButtoms
            if len(self.funcion_objetivo) != 0:
                for restriccion in range(len(self.funcion_objetivo)):
                    self.funcion_objetivo[restriccion].place_forget()
                    self.cambios[restriccion].place_forget()
                self.funcion_objetivo.clear()
                self.cambios.clear()

            #Creacion de los campos de la funcion objetivo, asi como sus respectivos CheckButtoms
            for variable in range(int(self.variables.get())):
                self.funcion_objetivo.append(Entry(self.master,width=5))
                self.funcion_objetivo[variable].place(x=100+(variable*70), y=65)
                self.cambio.append(IntVar())
                self.cambios.append(Checkbutton(self.master, text="x"+str(variable+1), variable=self.cambio[variable], indicatoron=0, command=self.genEntradas))
                self.cambios[variable].place(x=140+(variable*70), y=62)
                self.variable = variable

            # Creacion de etiquetas para la funcion objetivo
            for restriccion in range(int(self.restricciones.get())):
                self.label.append(Label(self.master, text="Restriccion " + str(restriccion + 1)))
                self.label[restriccion].place(x=10, y=90 + (restriccion * 25))

            # Creacion de la tabla optima en blanco
            i = -1
            self.etiqueta.append(Label(self.master, text="A continuacion introduzca los valores de la tabla optima:"))
            self.etiqueta[0].place(x=10, y=90+(int(self.restricciones.get())*25))
            for renglon in range(int(self.restricciones.get()) + 1):
                self.tabla_optima.append([])
                for columna in range(int(self.variables.get()) + int(self.restricciones.get()) + 1):
                    i = i + 1
                    self.content.append(StringVar())
                    self.tabla_optima[renglon].append(Entry(self.master, width=5, textvariable=self.content[i]))
                    self.tabla_optima[renglon][columna].place(x=10 + (columna * 40), y=115+(int(self.restricciones.get())*25)+(renglon * 25))
                    self.renglon = renglon
                    self.columna = columna

            #Adaptacion de la pantalla con respecto a los datos introducidos
            if (10 + (columna * 40)) > 140+(variable*70) and (10 + (columna * 40)) > 360:
                self.master.geometry(str(10 + (columna * 40)) + 'x' + str(145 + (int(self.restricciones.get()) * 25) + ((len(self.tabla_optima) - 1) * 25)))
            elif 140+(variable*70) > 400:
                self.master.geometry(str(170+(variable*70)) + 'x' + str(145 + (int(self.restricciones.get()) * 25) + ((len(self.tabla_optima) - 1) * 25)))
            else:
                self.master.geometry('400x' + str(145+(int(self.restricciones.get())*25)+((len(self.tabla_optima) - 1) * 25)))
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def genEntradas(self):
        try:
            if len(self.vectorCambios) != 0:
                for vector in range(len(self.vectorCambios)):
                    for cambio in range(len(self.vectorCambios[vector])):
                        self.vectorCambios[vector][cambio].place_forget()
                self.vectorCambios.clear()
            i = 0
            for cambio in range(len(self.cambio)):
                self.vectorCambios.append([])
                if self.cambio[cambio].get() == 1:
                    for restriccion in range(int(self.restricciones.get())):
                        self.vectorCambios[i].append(Entry(self.master, width=5))
                        self.vectorCambios[i][restriccion].place(x=100+(i*70),y=90 + (restriccion * 25))
                i = i + 1
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

    def imprimirEntradas(self):
        try:
            i = -1
            for renglon in range(len(self.tabla_optima)):
                for columna in range(len(self.tabla_optima[renglon])):
                    i = i + 1
                    if (self.tabla_optima[renglon][columna].get()).find('/') == True:
                        aux = self.tabla_optima[renglon][columna].get().split('/')
                        self.content[i].set(str(int(aux[0])/int(aux[1])))
                    print(self.tabla_optima[renglon][columna].get())
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "No se pudo realizar la operacion")

gui = GUI()

mainloop()