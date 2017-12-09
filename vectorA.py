def Simplex(Tabla):
    print (Tabla)


variables = int(input("Variables >> "))
restricciones = int(input("Restricciones >> "))

tablaOptima = [[0 for columna in range(variables + restricciones + 1)] for renglon in range(restricciones + 1)]

for renglon in range(restricciones + 1):
    for columna in range(variables + restricciones + 1):
        tablaOptima[renglon][columna] = input("Da el valor para la posicion ({0},{1}) >>".format(renglon, columna))

while True:
    tipo = int(input("Seleccione una opcion\nMinimizar: 0\nMaximizar: 1\n>>"))
    if (tipo == 1 or tipo == 0):
        break
    else:
        print ("Opcion erronea")

funcion_objetivo = []
for variable in range(variables):
    aux = int(input("Introduce el valor {0} de la funcion objetivo>>".format(variable + 1)))
    funcion_objetivo.append(aux)

while True:
    cambio = int(input("En que variable se realizara el cambio?>>"))
    if cambio > variables or cambio <= 0:
        print ("Opcion erronea")
    else:
        break

vector_cambio = []
for restriccion in range(restricciones):
    aux = int(input("Introduce el valor {0} del vector a cambiar>>".format(restriccion + 1)))
    vector_cambio.append(aux)

vector_aux = []
for renglon in range(2, len(tablaOptima[0]) - 1):
    vector_aux.append(tablaOptima[0][renglon])

res = 0
for valor in range(len(vector_aux)):
    res = res + (vector_aux[valor] * vector_cambio[valor])

res = res - funcion_objetivo[cambio - 1]

if res > 0:
    tablaOptima[0][cambio - 1] = res
else:
    Simplex(tablaOptima)
