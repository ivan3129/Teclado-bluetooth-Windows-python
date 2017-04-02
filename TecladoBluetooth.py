#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Autor: Ivan Yuquilima
Fecha de creacion: 10-Marzo-2017
Fecha de ultima modificacion: 26-Marzo-2017
"""
__author__ = "Ivan Yuquilima"
__copyright__ = "Copyright 2017"
__credits__ = [""]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Ivan Yuquilima"
__email__ = "ivan31299@hotmail.com"
__status__ = "Production"


#source https://github.com/karulis/pybluez
from bluetooth import *
#source https://pypi.python.org/pypi/PyAutoGUI
from pyautogui import keyDown, keyUp
from thread import start_new_thread
from time import sleep

#Variable que permite que un solo cliente se conecte a la vez
flagEnUso=False

#Creacion de Socket bluetooth
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

#Puerto RFCOM en el que escucha el sockeb Bluetooth
puerto = server_sock.getsockname()[1]
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])

print("Esperando conexion RFCOMM en el puerto %d" % puerto)

#Hilo de ejecucion para los clientes
def hiloClientes(cliente_sock, cliente_info):
    global flagEnUso
    flagEnUso=True
    try:
        while True:
            data = cliente_sock.recv(1024)
            if len(data) == 0:
                break
            print("Recibido [%s]" % data.strip())
            if len(data)<=3:
                # ejemplo a, f12, etc.
                teclear(data.strip())
    except IOError:
        print("Error con el cliente: %s" % str(cliente_info))
        pass
    except SystemExit:
         print("Error grave con el cliente: %s" % str(cliente_info))
    finally:
        print("Cerrando conexion [%s]" % str(cliente_info))
        flagEnUso=False
        cliente_sock.close()

#Metodo que recible  como parametro t para teclear
def teclear(t):
    keyDown(t)
    keyUp(t)
    print ("Tecleado: %s\n" %t)

#Metodo que comienza a escuchar las conexiones de los clientes bluetooth
#Acepta un solo cliente a la vez 
def escuchar():
    global flagEnUso
    try:
        while True:
            if not flagEnUso:
                print("Escuchando..")
                client_sock, client_info = server_sock.accept()
                print("Conexion entrante [%s]"%  str(client_info))
                flagEnUso=True
                start_new_thread(hiloClientes,(client_sock,client_info,))
            sleep(1)
    except:
        print ('\nError Hilo de escucha')

#Ejecucion infinita del programa
try:
    start_new_thread(escuchar,())
    while True:
        sleep(1)
except KeyboardInterrupt:
    print ('Alerta: Interrupcion')
except (KeyboardInterrupt, SystemExit):
    print('Alerta: Interrupcion 1')
finally:
    print('Cerrando programa')
    server_sock.close()
    print ("\nSocket cerrado")
    exit


