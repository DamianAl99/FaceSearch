from os import path
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from lxml import html
from decimal import Decimal

import time
from SeleniumHelper import DriverHelper

class Proceso:
    def __init__(self, precio_mi, precio_ma, precio_ma2, que_buscar, cantidad_scroll):
        #variables globlales
        #print("Monto minimo: ")
        #self.precio_mi = input()
        self.precio_mi = precio_mi
        #print("Monto maximo: ")
        #self.precio_ma = input()
        self.precio_ma = precio_ma
        #print("Monto maximo 2: ")
        #self.precio_ma2 = input()
        self.precio_ma2 = precio_ma2
        #print("Que producto buscar: ")
        #self.que_buscar = input()
        self.que_buscar = que_buscar
        #print("Cantidad de scroll a realizar: ")
        #self.cantidadDeScrolls = input()
        self.cantidadDeScrolls = cantidad_scroll
        self.dh = DriverHelper("https://www.facebook.com")

    def Logueo(self):
        xpath_no_existe_email = "//*[@id='facebook']/body/div[3]/div[2]/div/div/div/div/div[2]"
        xpath_no_existe_cuenta = "//*[@id='email_container']/div[2]"
        try:
            varEmail = self.dh.buscarPorXpath("//*[@id='email']")
            self.dh.escribirEnInput(varEmail, "USER")
            varPass = self.dh.buscarPorXpath("//*[@id='pass']")
            self.dh.escribirEnInput(varPass, "PASS")
            btnInicioSesion = self.dh.buscarPorXpath("//*[@name='login']")
            btnInicioSesion.click()
            time.sleep(5)
            self.dh.web_driver().ActionChains(self.dh.common()).send_keys(Keys.ESCAPE).perform()
            if(self.dh.existe_elemento(xpath_no_existe_email, 5) == True):
                if(self.dh.buscarPorXpath(xpath_no_existe_email).text == "Is this your account?"
                or self.dh.buscarPorXpath(xpath_no_existe_email).text == "¿Es tu cuenta?"):
                    return "El correo ingresado es incorrecto"
            if(self.dh.existe_elemento(xpath_no_existe_cuenta, 5) == True):
                if(self.dh.buscarPorXpath(xpath_no_existe_cuenta).text == "El correo electrónico que ingresaste no está conectado a una cuenta. "):
                    return "El correo ingresado no esta conectado a una cuenta Facebook, verificalo bien"
            return "" #OK
        except:
            return "Ocurrio un error no esperado en el login. Intentelo de nuevo y si el error persiste contacte con el ADMIN" #error

    def GoToMarketplace(self):
        try:
            self.dh.buscarPorXpath("//a[@aria-label='Marketplace']", 5).click()
            inputSearchProducts = self.dh.buscarXPorXpath("//input[@placeholder='Buscar en Marketplace']", 10)[0]
            self.dh.escribirEnInput(inputSearchProducts, self.que_buscar)
            inputSearchProducts.send_keys(Keys.ENTER)
            time.sleep(10)
            return ""
        except:
            return "Ocurrio un error no esperado al hacer click en Market Place. Intentelo de nuevo y si el error persiste contacte con el ADMIN"

    def DoScrollForPage(self):
        #Primer Paso: Hacer 10 veces scroll
        try:
            for i in range(0, int(self.cantidadDeScrolls)):
                self.dh.ejecutarJs("window.scrollBy(0,2500)")
                time.sleep(4)
            return ""
        except:
            return "Ocurrio un error no esperado al ver los productos. Intentelo de nuevo y si el error persiste contacte con el ADMIN"

    def ExtractDataWeb(self):
        #segundo paso: extraer todo el html
        html_data = self.dh.htmlDeLaPagina()

        #tercer paso: parsear el html parser y pasar a string para buscar por
        #xpath
        data2 = BeautifulSoup(html_data, "lxml")

        #cuarto paso: encontrar el id actual a recorrer
        search_id : str
        separar_ids = str(data2).split("id=")
        for ids in separar_ids:
            if(ids.__contains__("mount_0_0_")):
                search_id = ids
                break

        search_id = str(search_id.split('"')[1])
        cumpleRequisitos = []
        montosCardDecimal : Decimal
        encontramosCards = data2.find_all("div", class_="x1e558r4 x150jy0e xs83m0k x1iyjqo2 xdt5ytf x1r8uery x78zum5 x9f619 x291uyu x1uepa24 xnpuxes xjkvuk6 x1iorvi4")
        for card in encontramosCards:
            try:
                montosCard = card.find_all("span")[2].get_text()
                montosCardDecimal = Decimal(str(montosCard).replace(".","").replace("?","").replace("$","").replace("₲",""))
            except:
                continue

            try:
                if(montosCardDecimal > Decimal(self.precio_mi) and montosCardDecimal < Decimal(self.precio_ma)):
                        linkPublicacion = card.find_all("a")[0].get("href")
                        descripcion = card.find(class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
                        descripcion.text if descripcion is not None else None
                        cumpleRequisitos.append("https://www.facebook.com" + linkPublicacion) #if descripcion.__contains__(que_buscar.split(" ")[0]) else print("")
                if(montosCardDecimal < Decimal(self.precio_ma2)):
                        linkPublicacion = card.find_all("a")[0].get("href")
                        descripcion = card.find(class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6")
                        descripcion.text if descripcion is not None else None
                        cumpleRequisitos.append("https://www.facebook.com" + linkPublicacion) #if descripcion.__contains__(que_buscar.split(" ")[0]) else print("")
            except:
                continue 

        return cumpleRequisitos
        
    def OpenTabs(self, cumpleRequisitos):
        for tabs in cumpleRequisitos:
            if(tabs is not None):
                self.dh.ejecutarJs("window.open('" + tabs + "')")
                time.sleep(2)

    def CloseAll(self):
        self.dh.cerrar_ventantas()
#test
# pr = Proceso()
# pr.Logueo()
# pr.GoToMarketplace()
# pr.DoScrollForPage()
# pr.OpenTabs(pr.ExtractDataWeb())
# input()

