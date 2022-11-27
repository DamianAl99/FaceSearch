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

        ff = Label(self.ventana, text="Correo")
        ff.grid(row = 5, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.correo = Entry(self.ventana, font = ("Calibri 12"))
        self.correo.grid(row = 5, column = 1, columnspan = 1, padx = 15, pady = 15)

        ii = Label(self.ventana, text="Contraseña")
        ii.grid(row = 6, column = 0, columnspan = 1, padx = 1, pady = 2)
        self.passw = Entry(self.ventana,show="*", font = ("Calibri 12"))
        self.passw.grid(row = 6, column = 1, columnspan = 1, padx = 15, pady = 15)
        #Botones
        boton_igual = Button(self.ventana, text = "Iniciar", width= 50, height = 2, command = lambda: self.hacer_operacion())
        boton_igual.grid(row= 7, column = 1, padx = 15, pady = 15)

        self.ventana.mainloop()

    def hacer_operacion(self):
        pr = Proceso(self.precio_mi.get(), self.precio_ma.get(), self.precio_ma2.get(), self.buscar.get(), self.cuantas_veces.get(), self.correo.get(), self.passw.get())
        try:
            self.ValidarInput()
            #si no hay error en el logueo pasa
            result = pr.Logueo()
            if(result != ""): raise Exception("Logueo", result)
            #si no hay error en el gotomarketplace pasa
            result = pr.GoToMarketplace()
            if(result != ""): raise Exception("Ir al Market Place", result)
            #si no hay error durante el scroll pasa
            result = pr.DoScrollForPage()
            if(result != ""): raise Exception("Scrolleo Web", "Error al scrollear la web")
            #extraemos toda la lista que cumple con los montos
            lista_url_productos = pr.ExtractDataWeb()
            #cerramos mi perfil
            pr.CerrarPrimerChromeDriver()
            #ponemos el link para que vea el cliente
            pr.OpenTabs(lista_url_productos)
            #limpiar inputs
            self.buscar.delete(0, 'end')
            self.cuantas_veces.delete(0, 'end')
            self.precio_ma.delete(0, 'end')
            self.precio_ma2.delete(0, 'end')
            self.precio_mi.delete(0, 'end')
            #mensaje al culimnar el proceso
            messagebox.showinfo("INFO", "Disfrutá de lo encontrado!!")
        except Exception as ex:
            pr.CloseAll()
            messagebox.showerror("Error inesperado", ex)

    def ValidarInput(self):
        if(len(self.buscar.get()) < 2):
            raise Exception("Lo que deseas buscar debe tener mas letras")
        try:
            if int(self.cuantas_veces.get()) > 100: raise Exception("'Cuantas veces': No se puede superar las 100 busquedas")
            int(self.precio_ma.get())
            int(self.precio_ma2.get())
            int(self.precio_mi.get())
        except:
            raise Exception("Los campos 'Cuantas veces' y los 'precios' deben ser del tipo numerico")
        

InterfezUi()
