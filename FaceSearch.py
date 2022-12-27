from tkinter import *
from tkinter import messagebox
from BotFacebook import Proceso

class InterfezUi:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("FaceSearch")

        aa = Label(self.ventana, text="Que deseas buscar?", background="#00352C", fg="white", font=("Arial", 15))
        aa.grid(row = 0, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.buscar= Entry(self.ventana, font = ("Calibri 12"))
        self.buscar.grid(row = 0, column = 1, columnspan = 1, padx = 15, pady = 15)
        self.buscar.focus()

        cc = Label(self.ventana, text="Precio minimo", background="#00352C", fg="white", font=("Arial", 15))
        cc.grid(row = 2, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_mi = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_mi.grid(row = 2, column = 1, columnspan = 1, padx = 15, pady = 15)

        dd = Label(self.ventana, text="Precio maximo", background="#00352C", fg="white", font=("Arial", 15))
        dd.grid(row = 3, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_ma = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_ma.grid(row = 3, column = 1, columnspan = 1, padx = 15, pady = 15)

        ee = Label(self.ventana, text="Precio maximo 2", background="#00352C", fg="white", font=("Arial", 15))
        ee.grid(row = 4, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_ma2 = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_ma2.grid(row = 4, column = 1, columnspan = 1, padx = 15, pady = 15)
        #Botones
        boton_igual = Button(self.ventana, text = "Iniciar", width= 50, height = 2, command = lambda: self.hacer_operacion())
        boton_igual.grid(row= 7, column = 1, padx = 15, pady = 15)

        self.ventana.configure(bg='#00352C')
        self.ventana.mainloop()

    def hacer_operacion(self):
        pr = Proceso(self.precio_mi.get(), self.precio_ma.get(), self.precio_ma2.get(), self.buscar.get())
        try:
            self.ValidarInput()
            #si no hay error en el logueo pasa
            result = pr.SearchProducto()
            if result != "":  messagebox.showerror("Error inesperado", result)
            result = pr.OpenTabs()
            if result != "":  messagebox.showerror("Error inesperado", result)
            #limpiar inputs
            self.buscar.delete(0, 'end')
            self.precio_ma.delete(0, 'end')
            self.precio_ma2.delete(0, 'end')
            self.precio_mi.delete(0, 'end')
            #mensaje al culimnar el proceso
            messagebox.showinfo("Excelente", "Disfrutá de lo encontrado!!")
        except Exception as ex:
            pr.CloseAll()
            messagebox.showerror("Error inesperado", ex)

    def ValidarInput(self):
        if(len(self.buscar.get()) < 2):
            raise Exception("Lo que deseas buscar debe tener mas letras")
        try:
            int(self.precio_ma.get())
            int(self.precio_ma2.get())
            int(self.precio_mi.get())
        except:
            raise Exception("Los campos 'Cuantas veces' y los 'precios' deben ser del tipo numerico")
        

InterfezUi()
