import json
import math

# Nodos para estaciones
class Estacion:
    def __init__(self, estacion, latitud, longitud, tipo, alimentadores, upz):
        self.nombreEstacion = estacion
        self.latitud = latitud
        self.longitud = longitud
        self.tipo = tipo
        self.alimentadores = alimentadores
        self.upz = upz
        self.sig = None
        self.ant = None

# Listas
class Troncal:
    def __init__(self, nombreTroncal, cantidad, identificador):
        self.nombreTroncal = nombreTroncal
        self.cantidadEstaciones = cantidad
        self.identificador = identificador
        self.cabeza = None
        self.cola = None
        self.tamano = 0

    def insertarNodo(self, estacion, latitud, longitud, tipo, alimentadores, upz):
        if self.cabeza is None:
            nuevoNodo = Estacion(estacion, latitud, longitud, tipo, alimentadores, upz)
            self.cabeza = nuevoNodo
            self.cola = nuevoNodo
        else:
            nuevoNodo = Estacion(estacion, latitud, longitud, tipo, alimentadores, upz)
            nuevoNodo.sig = self.cabeza
            self.cabeza.ant = nuevoNodo
            self.cabeza = nuevoNodo
            self.tamano += 1

    def imprimirLista(self):
        print("Troncal: ", self.nombreTroncal)
        item = self.cabeza
        for i in range(self.tamano):
            if(item != None):

                item = item.sig

    def imprimirListaInvertida(self):
        print("Troncal: ", self.nombreTroncal)
        item = self.cola
        print(item)
        while item != None:
            print(item.nombreEstacion)
            item = item.ant


    def buscarEstacion(self, nombreEstacion):
        item = self.cabeza
        for i in range(self.tamano):
            if(item.nombreEstacion == nombreEstacion):
                print("Estacion encontrada", nombreEstacion)
                return (self, item)
            item = item.sig


def abrirTroncales():
    with open('data.json') as file:
        data = json.load(file)
        todasTroncales = []
        for troncal in data['Troncales']:
            nuevaTroncal = Troncal(troncal['NombreTroncal'], troncal['CantidadEstaciones'], troncal['Identificador'])
            for estacion in troncal['Estaciones']:
                nuevaTroncal.insertarNodo(estacion['Nombre'], estacion['Latitud'], estacion['Longitud'], estacion['Tipo'], estacion['Alimentadores'], estacion['UPZ'])
            todasTroncales.append(nuevaTroncal)
        return todasTroncales

# Alistar Troncales con Estaciones
transmilenio = abrirTroncales()

# Buscar las troncales de las estaciones.

def encontrarTroncalPorEstacion(estacion):
    for troncal in transmilenio:
        troncalEncontrada = troncal.buscarEstacion(estacion)
        if (troncalEncontrada != None):
            return troncalEncontrada[0] # Posicion 0 es Troncal, 1 es Estacion encontrad.

def enontrarTroncalPorId(id):
    for troncal in transmilenio:
        if(troncal.identificador == id):
            return troncal

# Posible ruita de las troncales (lista)

def posiblesRutas(troncalOrigen, troncalDestino):
    orden = []
    posibleRuta = []
    if(troncalOrigen == 1 and troncalDestino == 2): # Caracas sur a Caracas o al contrario.
        orden = [enontrarTroncalPorId(1), enontrarTroncalPorId(2)]
    elif(troncalOrigen == 3 and troncalDestino == 6):
        orden = [enontrarTroncalPorId(6), enontrarTroncalPorId(3)]

    print(orden)

    nuevaTroncal = Troncal("Nueva Ruta", 0, -1)

    for index, troncal in enumerate(orden):
        item = troncal.cabeza
        nuevaTroncal.tamano += troncal.tamano
        for i in range(troncal.tamano):
            nuevaTroncal.insertarNodo(item.nombreEstacion, item.latitud, item.longitud, item.tipo, item.alimentadores, item.upz)
            if(item != None):
                item = item.sig

    nuevaTroncal.imprimirLista()
    return nuevaTroncal

# Sumar trayecto

def calcularDistanciaEstaciones(posibleRuta, estacionOrigen, estacionDestino):
    numEstaciones = 0
    cont = False
    item = posibleRuta.cabeza
    flag = True
    distance = 0
    while item != None:

        print(item.nombreEstacion)

        if (flag == False):
            if (item.nombreEstacion == estacionOrigen):
                    cont = False

        if (flag == True):
            if (item.nombreEstacion == estacionDestino):
                cont = True
                flag = False

        if (cont == True): # Empieza a contar distancia
            numEstaciones += 1
            distance += haversine((item.latitud, item.longitud), (item.sig.latitud, item.sig.longitud))

        if (item != None):
            item = item.sig
        else:
            break


    return distance


def calcularDistanciaEstacionesInvertido(posibleRuta, estacionOrigen, estacionDestino):
    numEstaciones = 0
    cont = False
    item = posibleRuta.cola
    flag = True
    distance = 0

    while item != None:

        print(item.nombreEstacion)

        if (flag == False):
            if (item.nombreEstacion == estacionOrigen):
                    cont = False

        if (flag == True):
            if (item.nombreEstacion == estacionDestino):
                cont = True
                flag = False

        if (cont == True): # Empieza a contar distancia
            numEstaciones += 1
            distance += haversine((item.latitud, item.longitud), (item.sig.latitud, item.sig.longitud))

        if (item != None):
            item = item.ant
        else:
            break


    return distance


def haversine(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d



hash_table = [[] for _ in range(10)]
print (hash_table)

def abrirUPZS():
    with open('upzs.json') as file:
        data = json.load(file)
        for upz in data:
            print(upz)




def insert(hash_table, key, value):
    hash_key = hash(key) % len(hash_table)
    key_exists = False
    bucket = hash_table[hash_key]
    for i, kv in enumerate(bucket):
        k, v = kv
        if key == k:
            key_exists = True
            break
    if key_exists:
        bucket[i] = ((key, value))
    else:
        bucket.append((key, value))

print("Bienvenido xd")
print("Ingrese la estacion de origen")
estacionOrigen = input()
print("Ingrese la estacion de destino")
estacionDestino = input()

troncalOrigen = encontrarTroncalPorEstacion(estacionOrigen)
troncalDestino = encontrarTroncalPorEstacion(estacionDestino)

rutaSeleccionada = posiblesRutas(troncalOrigen.identificador, troncalDestino.identificador)

rutaSeleccionada.imprimirListaInvertida()

calculoRuta = calcularDistanciaEstaciones(rutaSeleccionada, estacionOrigen, estacionDestino)

if(calculoRuta == 0):
    calculoRuta = calcularDistanciaEstacionesInvertido(rutaSeleccionada, estacionOrigen, estacionDestino)

print("La dsitancia entre estaciones es de ", calculoRuta, " Km")


abrirUPZS()


