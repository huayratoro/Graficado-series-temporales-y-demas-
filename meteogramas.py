############################################
#### SCRIPT PARA HACER UN METEOGRAMA EN BASE 
#### A DATOS DE UNA ESTACION PARTICULAR
#### VERSION MAS SENCILLA
#### POWERED BY HUAYRATORO
############################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

#
dir_datos = '...'
salida = '...'
# Se importan los datos desde un csv particular
datos = pd.read_csv(dir_datos, sep=',')	# indicar la separacion correspondiente

# Convierto la fecha en un objeto datetime y como indice del DF
# esto es para que en el eje x se grafiquen las fechas y horas... 
for i in range(0, len(datos.HORA)) :
	if len(str(datos.HORA[i])) <= 1 :
		datos.FECHA[i] = datos.FECHA[i] + ' 0' + str(datos.HORA[i]) + (':00:00')
	if len(str(datos.HORA[i])) > 1 :
		datos.FECHA[i] = datos.FECHA[i] + ' ' + str(datos.HORA[i]) + (':00:00')

datos = datos.set_index(pd.to_datetime(datos.FECHA))
del datos['HORA']
del datos['FECHA']

# Se hace la figura 
fig = plt.figure(figsize = (10,5))
#### Temperatura y Td ####
ax1 = fig.add_subplot(211)	# en este caso dos graficos 21
## Con esta funcion Pandas grafica las series : 
## las etiquetas despues del . en el dataframe son los nombres de las columnas del mismo 
## que representan a las variables
datos.TEMPERATURA.plot(ax = ax1, color = 'red', legend = True, fontsize = 14)
datos.TD.plot(ax = ax1, color = 'blue', legend = True, fontsize = 14)
plt.ylabel('Temperatura °C', fontsize = 12)
datos.PRESION.plot(ax = ax1, color = 'black', legend = True, secondary_y=True, fontsize = 14)
plt.ylabel('PRESION hPa', fontsize = 12)
plt.grid()
#### Viento (int y dir) ####
ax2 = fig.add_subplot(212)
datos.VINT.plot(ax = ax2, color = 'orange', legend = True, fontsize = 14)
plt.ylabel('km/h', fontsize = 12)
plt.ylim(0,100)
datos.VDIR.plot(ax = ax2, style = 'o', secondary_y=True, legend = True, fontsize = 14)
plt.ylabel('grados', fontsize = 12)
plt.ylim(0,360)
plt.grid()

plt.show()
#plt.savefig(salida + 'Meteograma.png', dpi = 250)

