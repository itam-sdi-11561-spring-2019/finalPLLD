#!/usr/bin/env python
import rospy
import serial
from geometry_msgs.msg import Pose2D
#from graphical_client.msg import Pose2D_Array
robot = Pose2D()
meta = Pose2D()
obs1 = Pose2D()
obs2 = Pose2D()
obs3 = Pose2D()
obs4 = Pose2D()


ser = serial.Serial('/dev/ttyUSB0')  # open serial port
print(ser.name)         # check which port was really used


def rotateLeft(magnitud):
	''' La magnitud es que tanto girar y se da en radianes '''
	actual = robot.theta
	esperada = actual+magnitud
	#Mientras la diferencia sea mayor a .05 radianes, sigue rotando
	while(math.abs(robot.theta-esperada)>0.05):
		diferencia = esperada - robot.theta
		#Si aún le falta más de .25 radianes por rotar, rota mucho a la izquierda 
		if(diferencia>.25):
			mandaInstruccion(1)
		#Si le falta poquito por rotar, rota poco a la izquierda
		else if(diferencia>0):
			mandaInstruccion(2)
		#Si se pasó por poquito, gira poco a la derecha
		else if(diferencia>-.25):
			mandaInstruccion(4)
		#Si se pasó por mucho, gira mucho a la derecha
		else:
			mandaInstrucción(3)

def rotateRight(magnitud):
	''' La magnitud es que tanto girar y se da en radianes '''
	actual = robot.theta
	esperada = actual-magnitud
	#Mientras la diferencia sea mayor a .05 radianes, sigue rotando
	while(math.abs(robot.theta-esperada)>0.05):
		diferencia = robo.theta - esperada
		#Si aún le falta más de .25 radianes por rotar, rota mucho a la derecha 
		if(diferencia>.25):
			mandaInstruccion(3)
		else if(diferencia>0):
			mandaInstruccion(4)
		else if(diferencia>-.25):
			mandaInstruccion(2)
		else:
			mandaInstrucción(1)

def avanza(distancia):
	posInicial = [robot.x, robot.y]
	recorrida = [robot.x, robot.y]
	while(math.abs(recorrida-distancia)>10):
		recorrida = math.sqrt(math.pow(recorrida[0]-posInicial[0],2)+math.pow(recorrida[1]-posInicial[1],2))
		mandaInstruccion(0)


def mandaInstruccion(instruccion):
	ser.write(instruccion)     # write a string
	ser.close() 


def callbackRobot(data):
	global robot
	robot.x = data.x
	robot.y = data.y
	robot.theta = data.theta
	#print "La ubicacion del robot es x: %(x)s y: %(y)s theta: %(t)s " % {'x': robot.x, 'y': robot.y, 't':robot.theta}


def callbackMeta(data):
	global meta
	meta.x = data.x
	meta.y = data.y
	meta.theta = data.theta
	

def callbackObs1(data):
	global obs1
	obs1.x = data.x
	obs1.y = data.y
	obs1.theta = data.theta
	#print "La ubicacion del obstaculo 1 es x: %(x)s y: %(y)s theta: %(t)s " % {'x': obs1.x, 'y': obs2.y, 't':obs3.theta}

def callbackObs2(data):
	global obs2
	obs2.x = data.x
	obs2.y = data.y
	obs2.theta = data.theta
	#print "La ubicacion del obstaculo 2 es: " + obs2.x + ", " + obs2.y ". Con angulo " + obs2.theta

def callbackObs3(data):
	global obs3
	obs3.x = data.x
	obs3.y = data.y
	obs3.theta = data.theta
	#print "La ubicacion del obstaculo 3 es: " + obs3.x + ", " + obs3.y ". Con angulo " + obs3.theta

def callbackObs4(data):
	global obs4
	obs4.x = data.x
	obs4.y = data.y
	obs4.theta = data.theta
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
