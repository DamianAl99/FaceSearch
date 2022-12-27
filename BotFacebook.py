from os import path
from decimal import Decimal
from SeleniumHelper import DriverHelper
import time
import mysql.connector

class Proceso:
    def __init__(self, precio_mi, precio_ma, precio_ma2, que_buscar):
        self.precio_mi = precio_mi
        self.precio_ma = precio_ma
        self.precio_ma2 = precio_ma2
        self.que_buscar = que_buscar
        self.cumple_requisitos = []
        self.progress = 0

    def SearchProducto(self):
        try:
            mydb = mysql.connector.connect(user="u788216028_BotFace", passwd="Damian44*", host="45.152.46.1", database="u788216028_MasterFace")        
            mycursor =mydb.cursor(buffered=True)
            #--------------------------------------
            clientsID = self.SearchClientsId(mycursor)
            if clientsID == None: return f"No se encontro nada referente al producto '{self.que_buscar}'. Intenta ser mas puntual con lo que buscas!"
            productsDB = self.SearchProductById(clientsID, mycursor)
            if productsDB == None: return f"No se encontro info acerca del producto consultado. Comuniquese con el ADMIN"
            for productDB in productsDB:
                precioDB = productDB[2]
                if precioDB >= self.precio_mi and (precioDB <= self.precio_ma or precioDB <= self.precio_ma2):
                    self.cumple_requisitos.append(productDB)
            #--------------------------------------
            cumple_requisitos_ordenado = self.cumple_requisitos.sort()
            self.productos_mas_economicos = cumple_requisitos_ordenado[0:3]
            lista_de_precios = [(sum(producto[0])/len(productDB)) for producto in productDB]
            self.precios_promedios_del_producto = lista_de_precios
            #--------------------------------------
            mycursor.close()
            mydb.close()
            return ""
        except:
            return "Ocurrio un error al buscar el producto. Intentelo de nuevo y si el error persiste contacte con el ADMIN"

    def OpenTabs(self):
        try:
            max_ventanas = 0
            dh = DriverHelper("https://www.facebook.com", False)
            #---------------
            for tabs in self.cumple_requisitos:
                print(tabs[4])
                dh.ejecutarJs("window.open('" + tabs[4] + "')")
                max_ventanas += 1
                time.sleep(2)
            return ""
        except Exception as exce:
            return exce

    def SearchClientsId(self, mycursor):
        sql = f"SELECT * FROM clients WHERE name like '%{self.que_buscar}%'"
        mycursor.execute(sql)
        return mycursor.fetchall()

    def SearchProductById(self, clients, mycursor):
        result_with_products = []
        for client in clients:
            sql = f"SELECT * FROM products WHERE producto like '{client[0]}'"
            mycursor.execute(sql)
            result_with_products.append(mycursor.fetchall())
        return result_with_products

