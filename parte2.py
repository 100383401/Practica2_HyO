def costes(parada, coste):
	arrayNuevoCoste = []
  	for j in range (0, len(matrizCostes[parada - 1])):
    		arrayCostesParadasAdyacentes.append(matrizCostes[parada - 1][j])
  	for i in range (0,len(arrayCostesParadasAdyacentes)):
		if(arrayCostesParadasAdyacentes[i] != '--'):
			arrayNuevoCoste.append(("P" + repr(i + 1),int(arrayCostesParadasAdyacentes[i]) + coste))
  	return arrayNuevoCoste

def calcularAdyacente(parada):
	aux = []
	arrayParadasAdyacentes = []
	for j in range (0, len(matrizCostes[parada - 1])):
    		aux.append(matrizCostes[parada - 1][j])
  	for i in range (0,len(aux)):
		if(aux[i] != '--'):
			arrayParadasAdyacentes.append("P" + repr(i + 1))
  	return arrayParadasAdyacentes

"""Por ahora va a ser 0 pero hay que meter los parametros necesarios para calcular las heuristicas que hagamos"""
def heuristica (parada):
	for j in range (0, len(matrizCostes[numParadaBus - 1])):
		arrayHeuristicas.append(matrizCostes[numParadaBus - 1][j])
	for i in range (0,len(arrayHeuristicas)):
		if(arrayHeuristicas[i] != '--'):
			arrayHeuristicas[i] = 0
	return arrayHeuristicas


def acciones(estado):
	acciones = []
	arrayParadasAdyacentes = []
	final = False
	contar = 0
	arrayNumParadaBus = estado[0].split('P')
	arrayNumParadaBus.pop(0)
	numParadaBus = int(arrayNumParadaBus[0])
	"""Calculamos las paradas a las que se puede mover el bus"""
	arrayParadasAdyacentes = calcularAdyacente (numParadaBus)
	for i in range (0, len(arrayParadasAdyacentes)):
		acciones.append(('Mover', arrayParadasAdyacentes[i]))
	"""Calculamos si puede recoger a un alumno"""
	while (final == False and contar < len(estado[2])):
		if (estado[0] == estado[2][contar][0] and estado[4] > 0):
			final = True
			acciones.append ('Recoger')
		contar = contar + 1
	"""Comprobamos si puede dejar a un alumno en su cole"""
	final = False
	colegio = 0
	while (final == False and colegio < len(arrayColegios)):
		if (estado [0] == arrayColegios [colegio]):
			if (estado[1][colegio] > 0):
				"""contar + 1 para que luego al ejecutar la accion sepamos que cole hay que quitar del array de alumnos"""
				acciones.append(('Dejar', 'C' + str(colegio + 1)))
				final = True
		colegio = colegio + 1
	return acciones

def resultado (estado, accion):

	"""Si la accion es Mover"""
	if(accion[0] == 'Mover'):
		print("\nAccion a realizar: " + str(accion))
		estado[0] = accion[1]
		print(str(estado) + "\n")

	"""Si la accion es Recoger"""
	if(accion == 'Recoger'):
		final = 0
		destino = None
		numDestino = 0
		i = 0
		print("\nAccion a realizar: " + str(accion))
		while (final == False and i < len(estado[2])):
			if(estado[2][i][0] == estado[0]):
				print(accion)
				final = True
				destino = estado[2][i][1]
				print(destino)
				numDestino = int(destino.split('C')[1]) - 1
				estado[1][numDestino] += 1
				estado[4] -= 1
				estado[2][i][0] = 'B'
			i += 1

	"""Si la accion es Dejar"""
	if(accion[0] == 'Dejar'):
		final = 0
		destino = None
		numDestino = 0
		i = 0
		print("\nAccion a realizar: " + str(accion))
		while (final == False and i < len(estado[2])):
			if(estado[2][i][1] == accion[1] and estado[2][i][0] == 'B'):
				destino = estado[2][i][1]
				print(destino)
				numDestino = int(destino.split('C')[1]) - 1
				print(numDestino)
				estado[1][numDestino] -= 1
				estado[4] += 1
				estado[2][i][0] = 'E'
			i += 1

	return estado

f = open ("ejemplos/problema3.prob")
linea = f.readline()

x = linea.split()
numParadas = len(x)

matrizCostes = [[0 for columna in range (0,numParadas)] for fila in range (0,numParadas)]
for i in range (0, numParadas):
	matrizCostes[i][i] = '--'

arrayColegios = []
arrayEstudiantes = []
contador = 0
colegio = False
alumno = False
while len(linea) != 0:
  linea = f.readline()
  if (linea != ""):
    aux = linea.split()
    if (aux[0] == 'C1:'):
      colegio = True
      numColegios = len(aux)/2
      contadorColegios = 0
      for j in range (0, len(aux)):
        if (j%2 != 0):
		      separador = aux
		      y = separador[j].split(";")
		      arrayColegios.append (y[0])
      linea = f.readline()
      estudiante = linea.split()
      finalizado = False
      iterador = 0
      a = ""
      """Bucle para guardar cada alumno con su parada y a que colegio va"""
      while (finalizado == False):
        a = ""
        x = estudiante[iterador].split(",")
        if (len(x) == 2):
          parada = estudiante[iterador-2].split(":")
          tupla = (parada[0],estudiante[iterador-1], x[0])
          arrayEstudiantes.append(tupla)
          while (a != ";" and finalizado == False):
            iterador = iterador + 1
            x2 = estudiante[iterador].split(",")
            if (len(x2) == 2):
              tupla = (parada[0],estudiante[iterador-1], x2[0])
              arrayEstudiantes.append(tupla)
              iterador = iterador + 1
            x3 = estudiante[iterador].split(";")
            if (len(x3) == 2):
              a = ";"
              tupla = (parada[0],estudiante[iterador-1], x3[0])
              arrayEstudiantes.append(tupla)
              iterador = iterador + 1
            if (iterador == len(estudiante)-1):
              tupla = (parada[0],estudiante[iterador-1], estudiante[iterador])
              arrayEstudiantes.append(tupla)
              iterador = iterador + 1
              finalizado = True
        if (iterador < len(estudiante)):
          x4 = estudiante[iterador].split(";")
          if(len(x4) == 2):
            parada = estudiante[iterador-2].split(":")
            tupla = (parada[0],estudiante[iterador-1], x4[0])
            arrayEstudiantes.append(tupla)
            iterador = iterador + 1
          if (iterador == len(estudiante)-1):
            parada = estudiante[iterador-2].split(":")
            tupla = (parada[0],estudiante[iterador-1], estudiante[iterador])
            arrayEstudiantes.append(tupla)
            iterador = iterador + 1
            finalizado = True
        iterador = iterador + 1
    if (aux[0] == 'B:'):
		  posBusInicial = aux[1]
		  capacidadBus = int(aux[2])
    if (colegio == False):
		  aux.pop(0)
		  for i in range(0,numParadas):
		    matrizCostes[contador][i] = aux[i]
		  contador = contador + 1
arrayNumParadaBus = posBusInicial.split('P')
arrayNumParadaBus.pop(0)
numParadaBus = int(arrayNumParadaBus[0])
numeroAlumnos = 0
"""Calculo numero de alumnos, calculo de donde esta cada alumno y a que cole va"""
estadoAlumno = []
for z in range (0, len(arrayEstudiantes)):
	arrayAux = []
	"""CUIDADO CUANDO HAY VARIOS ESTUDIANTES QUE VAN AL MISMO COLE EN LA MISMA PARADA (CASO DE P7)"""
	for i in range (0, int(arrayEstudiantes[z][1])):
		arrayAux.append(arrayEstudiantes[z][0])
		arrayAux.append(arrayEstudiantes[z][2])
		estadoAlumno.append(arrayAux)
		numeroAlumnos += int(arrayEstudiantes[z][1])
	"""estadoAlumno.append((,))"""
print(estadoAlumno)
print("\nCUIDADOOOOOO SON 7 ALUMNOS, NO " + str(numeroAlumnos) + ", EN P7 SE LIA \n")
"""calculo numero de coles y array de alumnos que lleva al inicio"""
numeroColegios = len(arrayColegios)
alumnosInicio = []
for i in range (0 , numeroColegios):
	alumnosInicio.append(1)

"""Definicion estado inicial"""
estadoInicial = [posBusInicial, alumnosInicio, estadoAlumno, numeroAlumnos, capacidadBus]

estadoFinal = [posBusInicial, alumnosInicio, estadoAlumno, 0, 5]

"""Definimos una variable con la que iremos moviendonos en los estados, comienza siendo como el inicial"""
estado = [posBusInicial, alumnosInicio, estadoAlumno, numeroAlumnos, capacidadBus]
print (estado)

a = acciones(estado)
print (a)

b = resultado(estado, 'Recoger')
print(str(b) + "\n")
b = resultado(estado, ('Dejar', 'C1'))
print(str(b) + "\n")

arrayCostesParadasAdyacentes = []
arrayCostesParadasAdyacentes = costes(numParadaBus, 5)
"""for i in range (0, len(matrizCostes)):
	print (matrizCostes[i])"""
print (arrayCostesParadasAdyacentes)
print (matrizCostes[numParadaBus - 1])
print (arrayColegios)
"""arrayCostesParadasAdyacentes.sort()"""
arrayHeuristicas = []
arrayHeuristicas = heuristica(numParadaBus)
"""print (matrizCostes[numParadaBus - 1])
arrayCostesParadasAdyacentes = matrizCostes[numParadaBus - 1]
print(arrayCostesParadasAdyacentes)
arrayParadasAdyacentes = []
for i in range (0,len(arrayCostesParadasAdyacentes)):
	if(arrayCostesParadasAdyacentes[i] != '--'):
		arrayParadasAdyacentes.append("P" + repr(i + 1))
		print(arrayParadasAdyacentes)
		arrayParadasAdyacentes.append(int(arrayCostesParadasAdyacentes[i]))
		print(arrayParadasAdyacentes)"""
f.close()
"""
Hay que definir bien el estado inicial.
estadoInicial = (posBusInicial, 0, ('C1', 'E'))
print(estadoInicial)

Falta crear una variable global de coste acumulado para meterlo como primer parametro para la funcion,
	tal y como se indica 5 lineas mas abajo.
costeAcumulado = 0
def g (costeAcumulado, coste):
	costeAcumulado += coste
	return costeAcumulado
ejemploCoste = g(costeAcumulado,19)
ejemploCoste = g(costeAcumulado,19)
print(ejemploCoste)"""
