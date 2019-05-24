#!/usr/bin/env python
import rospy
import serial
from geometry_msgs.msg import Pose2D
import math
#from graphical_client.msg import Pose2D_Array
robot = Pose2D()
meta = Pose2D()
obs0 = Pose2D()
obs1 = Pose2D()
obs2 = Pose2D()
obs3 = Pose2D()
obs4 = Pose2D()
margen = math.pi/2 #el margen de error de ir derecho
prefrenado = 10 #mm

objetos = 0
bmeta = False
bobs0 = False
bobs1 = False
bobs2 = False
bobs3 = False
bobs4 = False

xMax = 0
xMin = 0
yMin = 0
yMax = 0

dx = 200
dy = 200

r = 100

V  = [];
ruta = [];
NO = [];




def rotateLeft(magnitud):
	''' La magnitud es que tanto girar y se da en radianes '''
	actual = robot.theta
	esperada = actual+magnitud
	sec = 2 
	#Mientras la diferencia sea mayor a .05 radianes, sigue rotando
	while(abs(robot.theta-esperada) % math.pi*2 >margen):
		sec = sec/2 
		diferencia = abs(esperada - robot.theta) % math.pi*2
		#Si aun le falta por rotar, rota mucho a la izquierda 
		if(diferencia>margen):
			mandaInstruccion('2')
			
		#Si se paso por poquito, gira poco a la derecha
		else:
			mandaInstruccion('1')

		
		#rospy.sleep(sec)
		#mandaInstruccion('3')
		
			

def rotateRight(magnitud):
	''' La magnitud es que tanto girar y se da en radianes '''
	actual = robot.theta
	esperada = actual-magnitud
	sec = 2 
	#Mientras la diferencia sea mayor a .05 radianes, sigue rotando
	while(abs(robot.theta-esperada) % math.pi*2 >margen):
		sec = sec/2 
		diferencia = abs(robot.theta - esperada) % math.pi*2

		if(diferencia > margen):
			mandaInstruccion('1')
		
		else:
			mandaInstruccion('2')
		
		#rospy.sleep(sec)
		#mandaInstruccion('3')
		
			

def avanza(distancia):
	posInicial = [robot.x, robot.y]
	actual = [robot.x, robot.y]
	recorrido = 0
	while(abs(recorrido - distancia)>prefrenado):
		actual = [robot.x, robot.y]
		recorrido = math.sqrt(math.pow(actual[0]-posInicial[0],2)+math.pow(actual[1]-posInicial[1],2))
		mandaInstruccion('0')
	mandaInstruccion('3')


def makeGrid(inicio, final, obstaculos):
    global xMax, xMin, yMin, yMax, numObs, NO
    xMax = final.x  - dx/2
    xMin = inicio.x + dx/2
    print "Aqui va el inicio"
    print inicio
    print "Y la meta"
    print final

    yMax = final.y - dy/2
    yMin =  inicio.y + dy/2


    for o in obstaculos:
        NO.append([o.x - r, o.x + r, o.y - r, o.y + r])
    
    numObs = len(NO)

    aStar([xMin, yMin])
    ruta.append([xMin, yMin])




def  aStar(n):
    global ruta, V
    if n[0] == xMax and n[1] == yMax:
        return True
    frontera = getNext(n)
    k = frontera.keys()
    k.sort()
    end = False
    while k != [] and not end:
        next = frontera[k.pop(0)]
	#print("Siguiente: ", next)
        V.append(next)
        end = aStar(next)
    if end:
        ruta.append(next)
        return True
    else:
        return False


def getNext(n):
    fr = {}
    sumx = -1
    for i in range(0,3):
        sumy = -1;
        nX = n[0] + dx*sumx
	
        for j in range(0,3):
            nY = n[1] + dy*sumy
            if [nX, nY] not in V:
                notBlock = True
                k = 0
                if nX <= xMax and nY <= yMax and nX >= xMin and nY >= yMin:
		    #print(nX, nY)
                    while notBlock and k < numObs:
                        notblockX =  NO[k][0] < (nX - dx/2) and NO[k][1] < (nX - dx/2)
                        notblockX = notblockX or (NO[k][0] > (nX + dx/2) and NO[k][1] > (nX + dx/2))
                        notblockY = NO[k][2] < (nY - dy/2) and NO[k][3] < (nY - dy/2)
                        notblockY  = notblockY or (NO[k][2] > (nY + dy/2) and NO[k][3] > (nY + dy/2))
                        notBlock = notblockX  or notblockY
                        k = k + 1
                    if notBlock:
                        dist = math.sqrt(math.pow(nX - xMax, 2) + math.pow(nY - yMax,2))
                        fr[dist] = [nX,nY]
            sumy = sumy + 1
        sumx = sumx + 1
    return fr


def getRuta():
    global ruta
    ruta.reverse()
    return ruta




def ejecutaPlan(plan):
	paso = 0
	for mov in plan:
		print('Paso no: ')		
		print(paso)
		xmeta = mov[0]
		ymeta = mov[1]
		xactual = robot.x
		yactual = robot.y
		a = abs(xmeta - xactual)
		b = (ymeta - yactual)
		c = math.sqrt(a*a+b*b)
		theta0 = robot.theta
		theta1 = math.acos(a/c)
		thetar = (theta1 - theta0) % math.pi*2
		#if thetar < margen and thetar < 0:
		#	rotateLeft(thetar)
		#elif thetar > margen and thetar > 0 :
		#	rotateRight(thetar)
		avanza(c)
		paso = paso +1 
	mandaInstruccion('3')



def avanza(distancia):
	posInicial = [robot.x, robot.y]
	actual = [robot.x, robot.y]
	recorrido = 0
	while(abs(recorrido - distancia)>10):
		actual = [robot.x, robot.y]
		recorrido = math.sqrt(math.pow(actual[0]-posInicial[0],2)+math.pow(actual[1]-posInicial[1],2))
		mandaInstruccion('0')


def mandaInstruccion(instruccion):
	ser = serial.Serial('/dev/ttyUSB0')  # open serial port
	ser.write(instruccion)     # write a string
	ser.close()
	print instruccion


def callbackRobot(data):
	global robot
	global objetos
	robot.x = data.x
	robot.y = data.y	
	robot.theta = data.theta
	print "hola, ya estoy aqui"

	if(bmeta):
		print "ya entre al iffff"
		obs = []
		if(bobs0):
			obs.append(obs0)
		if(bobs1):
			obs.append(obs1)
		if(bobs2):
			obs.append(obs2)
		if(bobs3):
			obs.append(obs3)
		if(bobs4):
			obs.append(obs4)

		makeGrid(robot, meta, obs)
		
		ruta = getRuta()
		print ruta
		ejecutaPlan(ruta)
	#print "La ubicacion del robot es x: %(x)s y: %(y)s theta: %(t)s " % {'x': robot.x, 'y': robot.y, 't':robot.theta}


def callbackMeta(data):
	global meta
	global bmeta
	global objetos
	if(not bmeta):
		print "la meta si la recibi"
		meta.x = data.x
		meta.y = data.y
		meta.theta = data.theta
		bmeta = True
	

def callbackObs0(data):
	global obs0
	global bobs0
	global objetos
	if(not bobs0):
		print "recibi obs0"
		obs0.x = data.x
		obs0.y = data.y
		obs0.theta = data.theta
		bobs0 = True
		objetos = objetos + 1


def callbackObs1(data):
	global obs1
	global bobs1
	global objetos
	if(not bobs1):
		print "recibi obs1"
		obs1.x = data.x
		obs1.y = data.y
		obs1.theta = data.theta
		bobs1 = True
		objetos = objetos + 1
	#print "La ubicacion del obstaculo 1 es x: %(x)s y: %(y)s theta: %(t)s " % {'x': obs1.x, 'y': obs2.y, 't':obs3.theta}

def callbackObs2(data):
	global obs2
	global bobs2
	global objetos
	if(not bobs2):
		print "recibi obs2"
		obs2.x = data.x
		obs2.y = data.y
		obs2.theta = data.theta
		bobs2 = True
		objetos = objetos + 1
	#print "La ubicacion del obstaculo 2 es: " + obs2.x + ", " + obs2.y ". Con angulo " + obs2.theta

def callbackObs3(data):
	global obs3
	global bobs3
	global objetos
	if(not bobs3):
		print "recibi obs3"
		obs3.x = data.x
		obs3.y = data.y
		obs3.theta = data.theta
		bobs3 = True
		objetos = objetos + 1
	#print "La ubicacion del obstaculo 3 es: " + obs3.x + ", " + obs3.y ". Con angulo " + obs3.theta

def callbackObs4(data):
	global obs4
	global bobs4
	global objetos
	if(not bobs4):
		print "recibi obs4"
		obs4.x = data.x
		obs4.y = data.y
		obs4.theta = data.theta
		bobs4 = True
		objetos = objetos + 1
	#print "La ubicacion del obstaculo 4 es: " + obs4.x + ", " + obs4.y ". Con angulo " + obs4.theta

      
def listener():

  # In ROS, nodes are uniquely named. If two nodes with the same
  # name are launched, the previous one is kicked off. The
  # anonymous=True flag means that rospy will choose a unique
  # name for our 'listener' node so that multiple listeners can
  # run simultaneously.
  rospy.init_node('subscriptor', anonymous=True)
  print "Funciona"

  #Obstaculos
  rospy.Subscriber("/b_r1", Pose2D, callbackObs1)
  rospy.Subscriber("/b_r2", Pose2D, callbackObs2)
  rospy.Subscriber("/b_r3", Pose2D, callbackObs3)
  rospy.Subscriber("/b_r4", Pose2D, callbackObs4)
  rospy.Subscriber("/b_r0", Pose2D, callbackObs0)

  #meta
  rospy.Subscriber("/ball", Pose2D, callbackMeta)

  #robot
  rospy.Subscriber("/y_r0", Pose2D, callbackRobot)

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()

if __name__ == '__main__':
	try:
		listener()
	except rospy.ROSInterruptException:
	    pass


