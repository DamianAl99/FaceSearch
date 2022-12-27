from os import path
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import html
from decimal import Decimal
import mysql.connector


import time
from SeleniumHelper import DriverHelper

class Proceso:
    def __init__(self, que_buscar):
        self.que_buscar = que_buscar
        self.dh = DriverHelper("https://www.facebook.com", True)

    def Logueo(self):
        xpath_no_existe_email = "//*[@id='facebook']/body/div[3]/div[2]/div/div/div/div/div[2]"
        xpath_no_existe_cuenta = "//*[@id='email_container']/div[2]"
        try:
            varEmail = self.dh.buscarPorXpath("//*[@id='email']")
            self.dh.escribirEnInput(varEmail, "damiianalmada06@gmail.com")
            #-----------
            varPass = self.dh.buscarPorXpath("//*[@id='pass']")
            self.dh.escribirEnInput(varPass,"Vicafeitador99")
            #-----------
            btnInicioSesion = self.dh.buscarPorXpath("//*[@name='login']")
            btnInicioSesion.click()
            time.sleep(10)
            #-----------
            if(self.dh.existe_elemento(xpath_no_existe_email, 5) == True):
                if(self.dh.buscarPorXpath(xpath_no_existe_email).text == "Is this your account?"
                or self.dh.buscarPorXpath(xpath_no_existe_email).text == "¿Es tu cuenta?"):
                    return "El correo ingresado es incorrecto"
            if(self.dh.existe_elemento(xpath_no_existe_cuenta, 5) == True):
                if(self.dh.buscarPorXpath(xpath_no_existe_cuenta).text == "El correo electrónico que ingresaste no está conectado a una cuenta. "):
                    return "El correo ingresado no esta conectado a una cuenta Facebook, verificalo bien"
            #-----------
            #en caso de que existe un popup
            self.dh.web_driver().ActionChains(self.dh.common()).send_keys(Keys.ESCAPE).perform()
            self.progress = 10
            return "" #OK
        except:
            return "Ocurrio un error no esperado en el login. Intentelo de nuevo y si el error persiste contacte con el ADMIN" #error

    def GoToMarketplace(self):
        try:
            self.dh.buscarPorXpath("//a[@aria-label='Marketplace']", 5).click()
            inputSearchProducts = self.dh.buscarXPorXpath("//input[@placeholder='Buscar en Marketplace']", 15)[0]
            self.dh.escribirEnInput(inputSearchProducts, self.que_buscar[1])
            inputSearchProducts.send_keys(Keys.ENTER)
            self.progress = 20
            time.sleep(5)
            return ""
        except:
            return "Ocurrio un error no esperado al hacer click en Market Place. Intentelo de nuevo y si el error persiste contacte con el ADMIN"

    def DoScrollForPage(self):
        try:
            for i in range(0, 20):
                self.dh.ejecutarJs("window.scrollBy(0,2500)")
                time.sleep(4)
            self.progress = 70
            return ""
        except:
            return "Ocurrio un error no esperado al ver los productos. Intentelo de nuevo y si el error persiste contacte con el ADMIN"

    def ExtractDataWeb(self):
        #variables scope
        cumpleRequisitos = []
        montosCardDecimal : Decimal
        #---------------
        #empieza el formateo con beatifull soup
        html_data = self.dh.htmlDeLaPagina()
        data2 = BeautifulSoup(html_data, "lxml")
        #---------------
        encontramosCards = data2.find_all("div", class_="x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6")#cambiar de vez en cuando
        for card in encontramosCards:
            try:
                montosCard = card.find_all("span")[2].get_text()
                montosCardDecimal = Decimal(str(montosCard).replace(".","").replace("?","").replace("$","").replace("₲",""))
            except:
                continue
        #---------------
            try:
                linkPublicacion = card.find_all("a")[0].get("href")
                descripcion = card.find(class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
                description_text = descripcion.text if descripcion is not None else ""
                dto_for_save_data = {
                    "producto":self.que_buscar[0],
                    "precio":montosCardDecimal,
                    "descripcion":description_text,
                    "link": "https://www.facebook.com" + linkPublicacion
                }
                cumpleRequisitos.append(dto_for_save_data)
            except:
                continue 
        #---------------
        self.progress = 80
        return cumpleRequisitos

    def SaveDataInDB(self, productos):
        try:
            mydb = mysql.connector.connect(user="u788216028_BotFace", passwd="", host="45.152.46.1", database="u788216028_MasterFace")        
            mycursor =mydb.cursor(buffered=True)
            for producto in productos:
                self.BulkInsert(producto['producto'], producto['precio'], producto['descripcion'], producto['link'], mydb, mycursor)
            mycursor.close()
            mydb.close()
            return ""
        except Exception as exce:
            return "Ocurrio un error al insertar los datos a la BD: "+exce
    
    def BulkInsert(self, product, price, description, link, mydb, mycursor):
        # mydb = mysql.connector.connect(user="u788216028_BotFace", passwd="Damian44*", host="45.152.46.1", database="u788216028_MasterFace")        
        # mycursor =mydb.cursor(buffered=True)
        sql = "INSERT INTO products (producto, precio, descripcion, link) VALUES (%s, %s, %s, %s)"
        val = (product, price, description, link)
        mycursor.execute(sql, val)
        mydb.commit()

    def CloseAll(self):
        self.dh.cerrar_ventantas()
        self.progress = 100


class main:
    def __init__(self) -> None:
        self.ExtractProductToSearch()
    def ExtractProductToSearch(self):
        mydb = mysql.connector.connect(user="u788216028_BotFace", passwd="Damian44*", host="45.152.46.1", database="u788216028_MasterFace")        
        mycursor =mydb.cursor(buffered=True)
        sql = "SELECT * FROM clients"
        mycursor.execute(sql)
        products = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        for product in products:
            pr = Proceso(product)
            result = pr.Logueo()
            if(result != ""): raise Exception("Logueo", result)
            #si no hay error en el gotomarketplace pasa
            result = pr.GoToMarketplace()
            if(result != ""): raise Exception("Ir al Market Place", result)
            #si no hay error durante el scroll pasa
            result = pr.DoScrollForPage()
            if(result != ""): raise Exception("Scrolleo Web", "Error al scrollear la web")
            #extraemos toda la lista
            cumple_requisito = pr.ExtractDataWeb()
            #cerramos la web
            pr.CloseAll()
            #guardamos todo en la bd
            result = pr.SaveDataInDB(cumple_requisito)
            if(result != ""): raise Exception("Database", result)
        print("Ya termino")

try:    
    main()
except Exception as exce:
    print(exce)