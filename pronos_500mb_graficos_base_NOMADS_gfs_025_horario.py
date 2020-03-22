#### SCRIPT PARA HACER CAMPOS DE PRONOSTICO 
#### LA INFO PERTENECE A LA PAGINA DEL NOMADS-NCEP
#### https://nomads.ncep.noaa.gov/dods/gfs_0p25_1hr
#### SE GRAFICAN LOS PRONOSTICOS DEL GFS 025 HORARIOS

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from os import listdir
from datetime import datetime, timedelta
import metpy.calc as mpcalc
from metpy.units import units
import scipy.ndimage as ndimage
import metpy.calc as mpcalc

states_provinces = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale='10m',
        facecolor='none',edgecolor='black')

countries = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_countries',
        scale='10m',
        facecolor='none',edgecolor='black')

## 
enlace = 'http://nomads.ncep.noaa.gov:80/dods/gfs_0p25_1hr/gfs20200322/gfs_0p25_1hr_12z'
salida = ''
## cargo la topografia
topografia = Dataset('.../etopo_bedrock.nc', 'r')
lat_topo  = topografia.variables[u'lat'][:]
lon_topo  = topografia.variables[u'lon'][:]
topo = topografia.variables[u'Band1'][:]
topografia.close()
#################################################################################################################################################
### GRAFICADO DE 500 VORTICIDAD
fecha_ini = datetime.strptime('22-03-2020 12:00:00', '%d-%m-%Y %H:%M:%S')
interruptor = 'on'
if interruptor == 'on':
	for dd in range(0,10) :
		######################## LEYENDO LOS DATOS #########################
		## Se cargan los datos de la pagina
		datos = Dataset(enlace, 'r')
		lat  = datos.variables[u'lat'][120:300]
		lon  = datos.variables[u'lon'][1080:1320]
		hgt = datos.variables['hgtprs'][dd,12,120:300, 1080:1320]
		ugrd = datos.variables['ugrdprs'][dd,12,120:300, 1080:1320]
		vgrd = datos.variables['vgrdprs'][dd,12,120:300, 1080:1320]
		datos.close()

		## calculo la vorticidad 
		dx, dy = mpcalc.lat_lon_grid_deltas(lon, lat)	
		f = mpcalc.coriolis_parameter(np.deg2rad(lat)).to(units('1/sec'))
		vor = mpcalc.vorticity(ugrd, vgrd, dx, dy, dim_order='yx')
		#vor = ndimage.gaussian_filter(vor, sigma=3, order=0) * units('1/sec')

		####### GRAFICADO ######## 
		fig=plt.figure(figsize=(15,12))
		ax1 = plt.subplot(1, 1, 1, projection=ccrs.PlateCarree())
		ax1.set_extent([lon[0], lon[len(lon)-1], lat[0], lat[len(lat)-1]], crs=ccrs.PlateCarree())
		# en contornos el geopotencial
		cs_1 = ax1.contour(lon, lat, hgt, 30, colors = 'black' , transform=ccrs.PlateCarree())
		ax1.clabel(cs_1, fmt='%2.1f',inline=True, fontsize=8)
		# en sombreado la vorticidad
		cint = np.arange(-15, 15)
		cm = ax1.contourf(lon, lat, vor*100000, cint[cint != 0], extend='both', cmap='bwr', transform=ccrs.PlateCarree())
		# enmascaro el terreno en negro
		top = ax1.contourf(lon_topo, lat_topo, topo, np.arange(2500,7000, 250), colors=['black'], transform=ccrs.PlateCarree())

		# Agregamos la línea de costas
		ax1.coastlines(resolution='10m',linewidth=0.6)   
		# Agregamos los límites de los países
		ax1.add_feature(countries,linewidth=0.4)
		# Agregamos los límites de las provincias
		ax1.add_feature(states_provinces,linewidth=0.4)
		# Definimos donde aparecen los ticks con las latitudes y longitudes
		ax1.set_yticks(np.arange(-60, -15,5), crs=ccrs.PlateCarree())
		ax1.set_xticks(np.arange(-90, -30,5), crs=ccrs.PlateCarree())
		# Le damos formato a las etiquetas de los ticks
		lon_formatter = LongitudeFormatter(zero_direction_label=True)
		lat_formatter = LatitudeFormatter()
		ax1.xaxis.set_major_formatter(lon_formatter)
		ax1.yaxis.set_major_formatter(lat_formatter)	    
		# Agregamos la barra de colores 
		cbar=plt.colorbar(cm,shrink=0.6)
		cbar.set_label('[1/seg]*e5',fontsize=10)
		plt.xlabel('Longitudes')
		plt.ylabel('Latitudes')
		plt.title('Geopotencial y vorticidad relativa en 500 mb ' + '\n ' + str((fecha_ini+timedelta(hours=dd))) + ' UTC')
		plt.savefig(salida + str(dd) + '_vort_500.png', dpi = 150, bbox_inches='tight')
		plt.close('all')
#		plt.show()


