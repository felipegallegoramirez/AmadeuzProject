import pygame
from pygame.locals import *
import sys
import numpy as np
from random import randrange
import math
tamx=30
tamy=30
d0=[[0]*tamy]*tamx
d1=[[0]*tamy]*tamx
d2=[[0]*tamy]*tamx
d3=[[0]*tamy]*tamx
d4=[[0]*tamy]*tamx
d5=[[0]*tamy]*tamx 
caminox=[]
caminoy=[]
pygame.init()
screen = pygame.display.set_mode((30*tamx, 30*tamy))
done = False
def Cuadro(Px,Py,T1,T2,color):
	
	pygame.draw.rect(screen, color, pygame.Rect(Px, Py, T1, T2))


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

def distSquared(y1,y2,x1,x2):
       return (x1 - x2)**2 + (y2 - y1)**2

clock = pygame.time.Clock()
while not done:
		dat=4
		for event in pygame.event.get():
		    if event.type == pygame.QUIT:
		            done = True
		screen.fill((0, 0, 0))

		for i in range(tamx):
			for r in range(tamy):
				d0[i][r]=randrange(1,10)
				d1[i][r]=randrange(1,10)
				d2[i][r]=randrange(1,10)/10
				d3[i][r]=randrange(1,10)
				d4[i][r]=randrange(1,10)
		'''
		for i in range(tamx):
			for r in range(tamy):
				Cuadro(i*30,r*30,10,10,(255,255,255))
		'''
		pygame.display.flip()
		pr1=(10,9,60,0)
		pr2=(10,9,60,0)
		pr3=(9,9,60,1)
		pr4=(9,9,60,0)
		repe=1
		llego=True


		xf=randrange(0,tamx-1)
		yf=randrange(0,tamy-1)
		x=randrange(0,tamx-1)
		y=randrange(0,tamy-1)
		print("Posicion en x: ",x,"\nPosicion en y: ",y)
		print("Posicion F en x: ",xf,"\nPosicion F en y: ",yf)
		Cuadro(x*30,y*30,10,10,(0,0,255))

		
		while llego:

			if(x+1>tamx-1):
				c1=(9999,1,1,1)
			else:
				dis=distSquared(yf,y,xf,x+1)
				c1=(dis,d0[x+1][y],d1[x+1][y],d2[x+1][y])

			if(x-1<0):
				c2=(9999,1,1,1)
			else:
				dis=distSquared(yf,y,xf,x-1)
				c2=(dis,d0[x-1][y],d1[x-1][y],d2[x-1][y])

			if(y+1>tamy-1):
				c3=(9999,1,1,1)
			else:
				dis=distSquared(yf,y+1,xf,x)
				c3=(dis,d0[x][y+1],d1[x][y+1],d2[x][y+1])

			if(y-1<0):
				c4=(9999,1,1,1)
			else:
				dis=distSquared(yf,y-1,xf,x)
				c4=(dis,d0[x][y-1],d1[x][y-1],d2[x][y-1])

			dis=distSquared(yf,y,xf,x)
			actual=(dis,d0[x][y],d1[x][y],d2[x][y])
			print(actual,"//",c1,"//",c2,"//",c3,"//",c4)
			dat=ruta(actual,c1,c2,c3,c4,dat)
			if dat==0:
				x=x+1
			if dat==1:
				x=x-1
			if dat==2:
				y=y+1
			if dat==3:
				y=y-1
			if(y==yf and x==xf):
				llego=False
			Cuadro(x*30,y*30,10,10,(0,255,255))
			print(dat)
			repe=+1
			pygame.display.flip()
			Cuadro(xf*30,yf*30,10,10,(255,0,0))
		Cuadro(xf*30,yf*30,10,10,(255,0,0))
		pygame.display.flip()
		clock.tick(1)



