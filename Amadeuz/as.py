#Muy importante Licencia UGPL Ivan Dragogear
#Freesound

import kivy
import os
import sqlite3
kivy.require("1.11.1")

#Seguro
#Sonido
from kivy.core.audio import SoundLoader

# Basico
from kivy.app import App

#divisiones
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

# propiedades de elementos
from kivy.properties import ListProperty, StringProperty
from kivy.properties import NumericProperty, BooleanProperty
from kivy.properties import ObjectProperty
# Tamaño de la apk
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import NoTransition 
from kivy.uix.screenmanager import SlideTransition 

#transiciones
from kivy.uix.screenmanager import SwapTransition 
from kivy.uix.screenmanager import FadeTransition 
from kivy.uix.screenmanager import WipeTransition 
from kivy.uix.screenmanager import FallOutTransition 
from kivy.uix.screenmanager import RiseInTransition
from kivy.properties import StringProperty

#Reloj
from kivy.clock import Clock

#Elementos
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# Mapa
from kivy_garden.mapview import MapView 

from kivy.base import runTouchApp
from kivy.lang import Builder

# Generador random
from random import randrange


#no c
from kivy_garden.mapview import MapMarkerPopup

# Tamaño de la pantalla
Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 1200)

# Cargar sonido
sound = SoundLoader.load('click.wav')
sound.seek(0)
##Variables para el algoritmo



tamx=30
tamy=30
points = []

# Algoritmo
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
    if(actual>r1[0]):
        p0=+10
    if(actual>r2[0]):
        p1=+10
    if(actual>r3[0]):
        p2=+10
    if(actual>r4[0]):    
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

def distSquared(pos1,pos2):
    x1=int(pos1/1000)
    y1=pos1%1000
    x2=int(pos2/1000)
    y2=pos2%1000
    return (x1 - x2)**2 + (y2 - y1)**2

dat=5
llego=True
pus=0
def siguiente(self,c1,c2,c3,c4,f,actual):
        global dat
        global pus
        global llego
        print(c3[0])
        dat=ruta(actual,c1,c2,c3,c4,dat)
        if dat==0:
            actual=f[0]
        if dat==1:
            actual=f[1]
        if dat==2:
            actual=f[2]
        if dat==3:
            actual=f[3]
        if(actual==4004 or pus>=12):
            llego=False
        print(dat)
        pus= pus+1;
        print(actual)
        print("\npaso: ",pus)

        if llego!=False:
            dcruces(self,actual)

#def actualizacion():


def dibujar(self,lat1,lon1):
    marker=MapMarkerPopup(lon=float(lon1), lat=float(lat1),source="output-onlinepngtools.png",popup_size=(10,10))
    self.ids.mapview.add_widget(marker)

def dcruces(self,sele):
    self.ids.container.clear_widgets()
    con = sqlite3.connect(self.DB_PATH)
    cursor = con.cursor()
    cursor.execute('select ID,Calle1,Calle2,Calle3,Calle4,lon,lat from Cruces')
    for i in cursor:
        if sele==i[0]:

            dcalles(self,i[1],i[2],i[3],i[4],4004,i[0])
            dibujar(self,i[5],i[6])

    con.close()
#Calles
def dcalles(self,c1,c2,c3,c4,ac,ac1):
    self.ids.container.clear_widgets()
    con = sqlite3.connect(self.DB_PATH)
    cursor = con.cursor()
    cursor.execute('select ID,Tamano,Velocidad,Congestion,PosA,PosB from Calles')
    ta=[0,0,0,0]
    for i in cursor:

#calle 1
        if c1==i[0]:
            if (ac!=i[5]):
                dis=distSquared(ac,i[5])
                ta[0]=i[5]
            else:
                dis=distSquared(ac,i[4])
                ta[0]=i[4]
            r1=(dis,i[1],i[2],i[3])


#calle 2
        if c2==i[0]:
            if (ac!=i[5]):
                dis=distSquared(ac,i[5])
                ta[1]=i[5]
            else:
                dis=distSquared(ac,i[4])
                ta[1]=i[4]
            r2=(dis,i[1],i[2],i[3])


#Calle 3
        if c3==i[0]:
            if (ac!=i[5]):
                dis=distSquared(ac,i[5])
                ta[2]=i[5]

            else:
                dis=distSquared(ac,i[4])
                ta[2]=i[4]
            r3=(dis,i[1],i[2],i[3])

#Calle 4
        if c4==i[0]:
            if (ac!=i[5]):
                dis=distSquared(ac,i[5])
                ta[3]=i[5]

            else:
                dis=distSquared(ac,i[4])
                ta[3]=i[4]

            r4=(dis,i[1],i[2],i[3])

    dis=distSquared(ac1,4004)
    siguiente(self,r1,r2,r3,r4,ta,dis)

    con.close()



#Base de datos 
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
 

# Controlador de las pantallas
class MainWid(ScreenManager):
    def __init__(self,**kwargs):
        super(MainWid,self).__init__()
        self.APP_PATH = os.getcwd()
        self.DB_PATH = self.APP_PATH+'/my_database.db'
        dcruces(self,1001)
        

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
        cursor.execute('select ID,Name,Latitud,Longitud from Rutas')
        for i in cursor:
            print(i)
            wid = DataWid(self)
            r1 = 'ID: '+str(100000000+i[0])[1:9]
            r2 = ', Nombre '+i[1]+'\n'
            wid.lat = str(i[2])
            wid.lon = str(i[3])
            wid.data = r1+r2
            self.ids.container.add_widget(wid)
        con.close()


    def actualizar_mapa(self,lon1,lat1):
        self.ids.mapview.center_on(float(lon1),float(lat1))
        marker=MapMarkerPopup(lon=float(lon1), lat=float(lat1),source="gps.png")
        self.ids.mapview.add_widget(marker)

    
    def click(self):
        lector = open("config.txt", 'r')
        lector.readline()
        lector.readline()
        if sound and lector.readline(1)=="1":
            sound.play()
#Rutas ------------------------------
#Cruces
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