variables = input("Variables >> ")
restricciones = input("restricciones >> ")

tablaOptima = [[ 0 for columna in range(variables + restricciones + 1)] for renglon in range(restricciones + 1)]

for renglon in range(restricciones + 1):
    for columna in range(variables + restricciones + 1):
        tablaOptima[renglon][columna] = input("Da el valor para la posicion ({0},{1}) >>".format(renglon,columna))
        # print "{0},{1}={2}".format(renglon,columna,tablaOptima[renglon][columna])

print tablaOptima

while True:
    tipo = input("Seleccione una opcion\nMinimizar: 0\nMaximizar: 1\n>>")
    if (tipo == (1 or 0)):
        break
    else:
        print "Opcion erronea"
