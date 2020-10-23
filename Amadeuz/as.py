#Muy importante Licencia UGPL Ivan Dragogear
#Freesound

import kivy
import os
import sqlite3
kivy.require("1.11.1")

#Seguro
#Sonido
from kivy.core.audio import SoundLoader


from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, StringProperty
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 
from kivy.uix.screenmanager import SlideTransition 
#from kivy.uix.screenmanager import CardTransition 
from kivy.uix.screenmanager import SwapTransition 
from kivy.uix.screenmanager import FadeTransition 
from kivy.uix.screenmanager import WipeTransition 
from kivy.uix.screenmanager import FallOutTransition 
from kivy.uix.screenmanager import RiseInTransition
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy_garden.mapview import MapView 

from kivy.base import runTouchApp
from kivy.lang import Builder
import _random

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 1200)

sound = SoundLoader.load('click.wav')
sound.seek(0)

def ruta(actual,r1,r2,r3,r4,ul):
# 0 Posicion
# 1 Tamaño Via
# 2 Velocidad
# 3 Congestion
# 5 Vehiculos


    p0=0
    p1=0
    p2=0
    p3=0

# Distancia
    if(actual[0]>r1[0]):
        p0=+10
    if(actual[0]>r2[0]):
        p1=+10
    if(actual[0]>r3[0]):
        p2=+10
    if(actual[0]>r4[0]):    
        p3=+10

    p0=p0+(2/(r1[1]/r1[2]))
    p1=p1+(2/(r2[1]/r2[2]))
    p2=p2+(2/(r3[1]/r3[2]))
    p3=p3+(2/(r4[1]/r4[2]))

    p0=p0+(1-r1[3])
    p1=p1+(1-r2[3])
    p2=p2+(1-r3[3])
    p3=p3+(1-r4[3])

    zzz=0
    print(p0,p1,p2,p3)
    if (p0>p1 and p0>p2 and p0>p3 and ul!=1):
        zzz=0
    elif(p1>p2 and p1 > p3 and ul!=0):
        zzz=1
    elif (p2>p3 and ul!=3):
        zzz=2
    else: 
        zzz=3

    return zzz

def normalizacion():



def distSquared(y1,y2,x1,x2):
       return (x1 - x2)**2 + (y2 - y1)**2




#Base de datos -----
def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        Crear_tablas(cursor)
        con.commit()
        con.close()
    except Exception as e:
        print(e)


def Crear_tablas(cursor):
    cursor.execute(
        '''
        CREATE TABLE Rutas(
        ID           INT   PRIMARY KEY  NOT NULL,
        Name         TEXT               NOT NULL,
        Latitud      TEXT               NOT NULL,
        Longitud     TEXT               NOT NULL   
        );
        '''
    )
    cursor.execute(
        '''
           CREATE TABLE Calles(
        ID           INT   PRIMARY KEY  NOT NULL,
        Tamano       INT                NOT NULL,
        Velocidad    INT                NOT NULL,
        Congestion   INT                NOT NULL,
        PosA         INT                NOT NULL,
        PosB         INT                NOT NULL
        );
        '''
    )

    cursor.execute(
        '''
           CREATE TABLE Cruces(
        ID           INT   PRIMARY KEY  NOT NULL,
        Calle1       INT                Not Null,
        Calle2       INT                Not Null,
        Calle3       INT                Not Null,
        Calle4       INT                Not Null,
        lon          TEXT               Not Null,
        lat          TEXT               Not Null
        );
        '''
    )


class video (GridLayout,BoxLayout):
    pass


class MainWid(ScreenManager):
    def __init__(self,**kwargs):
        super(MainWid,self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+'/my_database.db'
    #transition = NoTransition()
    #transition = SlideTransition()
    #transition = SwapTransition()
    #transition = FadeTransition()
    #transition = WipeTransition()
    #transition = FallOutTransition()
    #transition = RiseInTransition()


    def cargar(self):
        lector = open("config.txt", 'r')
        self.ids.name.text=lector.readline()
        if lector.readline(1)=="1":
            self.ids.Checkicon.active=True
            Ticon=True
        lector.readline()
        if lector.readline(1)=="1":
            self.ids.Checksound.active=True
            Tsonido=True
        lector.readline()
        if lector.readline(1)=="1":
            self.ids.Checkalert.active=True
            TAlert=True
        lector.close()


    def cambiarTexto(self):
        print ("Hello World")

    

    def Guardado_Config(self):
        a1 = self.ids.Checkicon.active
        a2 = self.ids.Checksound.active
        a3 = self.ids.Checkalert.active
        lector = open("config.txt", 'r')
        nombre=lector.readline()
        archivo = open("config.txt", 'w')
        archivo.write(nombre)
        if a1:
            archivo.write("1\n")
        else:
            archivo.write("0\n")
        if a2:
            archivo.write("1\n")
        else:
            archivo.write("0\n")
        if a3:
            archivo.write("1\n")
        else:
            archivo.write("0\n")
        lector.close()
        archivo.close() 

    def create_database(self):
        connect_to_database(self.DB_PATH)



    def Guardado_Nombre(self):
        lector = open("config.txt", 'r')
        lector.readline()
        a1=lector.readline()
        a2=lector.readline()
        a3=lector.readline()
        archivo = open("config.txt", 'w')
        nombre= self.ids.name.text
        archivo.write(nombre+"\n")
        archivo.write(a1)
        archivo.write(a2)
        archivo.write(a3)
        lector.close()
        archivo.close()


    def insert_data(self):
        con = sqlite3.connect(self.DB_PATH)
        cursor = con.cursor()
        d1 = self.ids.Rid.text
        d2 = self.ids.Rname.text
        d3 = self.ids.Rlon.text
        d4 = self.ids.Rlat.text
        a1 = (d1,d2,d3,d4)
        s1 = 'INSERT INTO Rutas(ID, Name, Latitud, Longitud)'
        s2 = 'VALUES(%s,"%s","%s",%s)' % a1
        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
        except Exception as e:
            print (e)

    def check_memory(self):
        self.ids.container.clear_widgets()
        con = sqlite3.connect(self.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID,Name, Latitud, Longitud from Rutas')
        for i in cursor:
            wid = DataWid(self)
            r1 = 'ID: '+str(100000000+i[0])[1:9]
            r2 = ', Nombre '+i[1]+'\n'
            wid.lat = str(i[2])
            wid.lon = str(i[3])
            wid.data = r1+r2
            self.ids.container.add_widget(wid)
        con.close()

    def actualizar_mapa(self,lon,lat):
        self.ids.mapview.lat =lat
        self.ids.mapview.lon =lon
        print("GG")
    
    def click(self):
        lector = open("config.txt", 'r')
        lector.readline()
        lector.readline()
        if sound and lector.readline(1)=="1":
            sound.play()

    def EstablecerRuta (self)
        self.ids.container.clear_widgets()
        con = sqlite3.connect(self.DB_PATH)
        cursor = con.cursor()
        cursor.execute('select ID,Name, Latitud, Longitud from Rutas')
        for i in cursor:
            wid = DataWid(self)
            r1 = 'ID: '+str(100000000+i[0])[1:9]
            r2 = ', Nombre '+i[1]+'\n'
            wid.lat = str(i[2])
            wid.lon = str(i[3])
            wid.data = r1+r2
            self.ids.container.add_widget(wid)
        con.close()

    pass
class DataWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataWid,self).__init__()
        self.mainwid = mainwid

    def update_data(self,lon,lat):
        self.mainwid.actualizar_mapa(lon,lat)
    pass

class UnaScreen(Screen):
    pass
    
class MainApp(App):
    title = "Screen Manager"
    def build(self):
        return MainWid()
        
if __name__ == "__main__":
    MainApp().run()