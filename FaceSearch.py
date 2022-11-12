from tkinter import *
from tkinter import messagebox
from BotFacebook import Proceso

class InterfezUi:
    def __init__(self):
        self.ventana = Tk()
        self.ventana.title("FaceSearch")

        aa = Label(self.ventana, text="Que deseas buscar?")
        aa.grid(row = 0, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.buscar= Entry(self.ventana, font = ("Calibri 12"))
        self.buscar.grid(row = 0, column = 1, columnspan = 1, padx = 15, pady = 15)
        self.buscar.focus()

        bb = Label(self.ventana, text="Cuantas veces deseas buscar?")
        bb.grid(row = 1, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.cuantas_veces = Entry(self.ventana, font = ("Calibri 12"))
        self.cuantas_veces.grid(row = 1, column = 1, columnspan = 1, padx = 15, pady = 15)

        cc = Label(self.ventana, text="Precio minimo")
        cc.grid(row = 2, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_mi = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_mi.grid(row = 2, column = 1, columnspan = 1, padx = 15, pady = 15)

        dd = Label(self.ventana, text="Precio maximo")
        dd.grid(row = 3, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_ma = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_ma.grid(row = 3, column = 1, columnspan = 1, padx = 15, pady = 15)

        ee = Label(self.ventana, text="Precio maximo 2")
        ee.grid(row = 4, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.precio_ma2 = Entry(self.ventana, font = ("Calibri 12"))
        self.precio_ma2.grid(row = 4, column = 1, columnspan = 1, padx = 15, pady = 15)
        #Botones
        boton_igual = Button(self.ventana, text = "Iniciar", width= 50, height = 2, command = lambda: self.hacer_operacion())
        boton_igual.grid(row= 5, column = 1, padx = 15, pady = 15)


        self.ventana.mainloop()

    def hacer_operacion(self):
        pr = Proceso(self.precio_mi.get(), self.precio_ma.get(), self.precio_ma2.get(), self.buscar.get(), self.cuantas_veces.get())
        try:
            self.ValidarInput()   
            if(pr.Logueo()): raise Exception("Logueo", "Hubo un error en el logueo a Facebook")
            if(pr.GoToMarketplace()): raise Exception("Ir al Market Place", "Hubo un error al hacer click en el icono Market place")
            if(pr.DoScrollForPage()): raise Exception("Scrolleo Web", "Error al scrollear la web")
            pr.OpenTabs(pr.ExtractDataWeb())
        except Exception as ex:
            pr.CloseAll()
            messagebox.showerror("Error inesperado", ex)


    def ValidarInput(self):
        if(len(self.buscar.get()) < 2):
            raise Exception("Lo que deseas buscar debe tener mas letras")
        try:
            int(self.cuantas_veces.get())
            int(self.precio_ma.get())
            int(self.precio_ma2.get())
            int(self.precio_mi.get())
        except:
            raise Exception("Los campos Cuantas veces y los precios deben ser del tipo numerico")
        

InterfezUi()
