from os import path
from decimal import Decimal
from SeleniumHelper import DriverHelper
import time
import mysql.connector

class Proceso:
    def __init__(self, precio_mi, precio_ma, precio_ma2, que_buscar):
        self.precio_mi = Decimal(precio_mi)
        self.precio_ma = Decimal(precio_ma)
        self.precio_ma2 = Decimal(precio_ma2)
        self.que_buscar = que_buscar
        self.cumple_requisitos = []
        self.productos_mas_economicos = []
        self.precios_promedios_del_producto = []
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
            #--------------------------------------
            #productsDB viene en un array aunque encuentre 1 tipo de producto nomas
            cumple_requisitos_ordenado = []
            for productDB in productsDB:
                for product in productDB:
                    precioDB = product[2]
                    if precioDB >= self.precio_mi and (precioDB <= self.precio_ma or precioDB <= self.precio_ma2):
                        self.cumple_requisitos.append(product)
            #--------------------------------------
                if len(self.cumple_requisitos) >= 3:
                    ordenado = sorted(self.cumple_requisitos, key=lambda price: price[2])
                    self.productos_mas_economicos = ordenado[0:3]
                    lista_de_precios = [prod[2] for prod in self.cumple_requisitos]
                    self.precios_promedios_del_producto = sum(lista_de_precios)/len(lista_de_precios)
            #--------------------------------------
            mycursor.close()
            mydb.close()
            return ""
        except Exception as exce:
            return "Ocurrio un error al buscar el producto. Intentelo de nuevo y si el error persiste contacte con el ADMIN"


    def sorted(self, array):
        ret = []
        ret2 = []
        for arr in array:
            ret.append((arr[0], arr[2]))
        ret.sort()
        for re in ret:
            for arr in array:
                if re[0] == arr[0]:
                    ret2.append(arr)
        return ret2
            

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

Proceso(1000000, 2000000, 2, "heladera").SearchProducto()

