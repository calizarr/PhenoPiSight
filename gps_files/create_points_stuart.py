# This file is meant to be used from the GQIS console
# It is highly specific to the DDPSC project.
from __future__ import print_function
from fractions import Fraction
import os
points = []
coordinates = []
raspberries = []
width = 6
height = 30
# offset = 10
offset = 11

# Initial GPS point that existed from standing in Greenhouse 9C and checking my location.
# initial_lat = -10062973.096
# initial_long = 4675266.934
# initial_lat, initial_long = [float(x) for x in "-10062973.124,4675266.263".split(',')]


# rPI_145 is 2.794 meters (x) and 0.5461 meters (y) from the initial lat/long point
# rPI_145_lat = initial_lat + 2.794
# rPI_145_long = initial_long + 0.5461
# rPI_145 = QgsPoint(rPI_145_lat, rPI_145_long)
# points.append(rPI_145)
# We need to use the X, Y coordinates to convert latitude and longitude.
# init_x = (abs(145-(width*height)-offset) % width) + 1
# init_y = (abs(145-(width*height)-offset) / width) + 1
# init_x = (abs(145-offset) % width) + 1
# init_y = (abs(145-offset) / width) + 1

# Coordinates that the Raspberry PIs are separated by in an ideal grid.
# Still have to adjust for the first column that is off by a few.
# rPIs are separated by rPI_x in meters
rPI_x = 0.9779
# rPIs are separated by rPI_y in meters
rPI_y = 0.4572
# If they're in column 4 and 5 they have a different offset.
rPI_x_new = 0.9652
rPI_y_new = 0.2667

# Deriving initial rPI coordinates.
# We start at 10.9.0.11 or ShakoorCamera11 and proceed to generate points from there.
rPI_21_lat = -10062969.22919243
rPI_21_long = 4675278.246040583
rPI_21 = QgsPoint(rPI_21_lat, rPI_21_long)
init_x = (abs(21-offset) % width) + 1
init_y = (abs(21-offset) / width) + 1
# Points are the QgsPoint coordinates in meters
# points.append(rPI_11)
# Coordinates are the floats that make up the QgsPoint coordinates in meters.
# coordinates.append([rPI_11_lat, rPI_11_long])
# Raspberries is the IP address of the Raspberry PI/inventory_hostname
# raspberries.append("10.9.0.11")
# We need to use the X, Y coordinates to convert latitude and longitude.
# init_x = (abs(11-(width*height)-offset) % width) + 1
# init_y = (abs(11-(width*height)-offset) / width) + 1

# Trackback variables that get updated at the end of each for loop
# updated to the just recently calculated Raspbery Pi
prev_x = init_x
prev_y = init_y
# prev_lat = rPI_11_lat
# prev_long = rPI_11_long
prev_lat = rPI_21_lat
prev_long = rPI_21_long
# Starting from ShakoorCamera12 to ShakoorCamera190
# Remember python ranges go to n-1
for ind in range(11, 191):
    # Formula to calculate x, y coordinates
    # formula = abs(ind-(width*height)-offset)
    formula = abs(ind - offset)
    y = (formula / width) + 1
    x = (formula % width) + 1
    # Adding shift for the first column
    shift_indices = []
    shift_indices = shift_indices + range(11, 191, 6) + range(12, 191, 6)
    rPI_x_mod = rPI_x
    rPI_y_mod = rPI_y
    # rPI_lat = prev_lat + (rPI_x_mod * (prev_x - x))
    # rPI_long = prev_long + (rPI_y_mod * (prev_y - y))
    # rPI_lat = prev_lat + (rPI_x_mod * (x - prev_x))
    # rPI_long = prev_long + (rPI_y_mod * (prev_y - y))
    if x < prev_x:
        rPI_lat = prev_lat - (rPI_x_mod * (prev_x - x))
    elif x > prev_x:
        rPI_lat = prev_lat + (rPI_x_mod * (x - prev_x))
    else:
        rPI_lat = prev_lat
    if y < prev_y:
        rPI_long = prev_long + (rPI_y_mod * (prev_y - y))
    elif y > prev_y:
        rPI_long = prev_long - (rPI_y_mod * (y - prev_y))
    else:
        rPI_long = prev_long
    # Calculating latitude longitude changes via grid coords
    # if x < prev_x:
    #     rPI_lat = prev_lat + (rPI_x_mod * (prev_x - x))
    # elif x > prev_x:
    #     rPI_lat = prev_lat - (rPI_x_mod * (x - prev_x))
    # else:
    #     rPI_lat = prev_lat
    # # Doing the same for y / longitude
    # if y < prev_y:
    #     rPI_long = prev_long - (rPI_y_mod * (prev_y - y))
    # elif y > prev_y:
    #     rPI_long = prev_long + (rPI_y_mod * (y - prev_y))
    # else:
    #     rPI_long = prev_long
    if ind in shift_indices:
        # rPI_lat += rPI_x_new
        rPI_long += -1 * rPI_y_new
    rPI_point = QgsPoint(rPI_lat, rPI_long)
    rPI_coords = [rPI_lat, rPI_long]
    points.append(rPI_point)
    coordinates.append(rPI_coords)
    raspberries.append("10.9.0."+str(ind))
    # Updating the trackback variables.
    # prev_x = x
    # prev_y = y
    # prev_lat = rPI_lat
    # prev_long = rPI_long

# create a memory layer with all the rPI points
# Most of this code came from: http://gis.stackexchange.com/questions/86812/how-to-draw-polygons-from-the-python-console
layer = QgsVectorLayer('Point', 'points', 'memory')
# add the first point (initial point)
pr = layer.dataProvider()
pt = QgsFeature()
point1 = QgsPoint(initial_lat, initial_long)
pt.setGeometry(QgsGeometry.fromPoint(point1))
pr.addFeatures([pt])
layer.updateExtents()
# For loop to create all of the Raspberry Pi points.
for rPI in points:
    pr = layer.dataProvider()
    pt = QgsFeature()
    pt.setGeometry(QgsGeometry.fromPoint(rPI))
    pr.addFeatures([pt])
    layer.updateExtents()

# add the layer to the canvas
QgsMapLayerRegistry.instance().addMapLayers([layer])

# Converting points from meter coordinates (3857) to GPS / Lat & Long coordinates in WGS 4326
# ESRI:3857 WGS Pseudo-Mercator
sourceCrs = QgsCoordinateReferenceSystem(3857)
# ESRI:4326 WGS (GCS)
destCrs = QgsCoordinateReferenceSystem(4326)
# Setting up transformation vector
xform = QgsCoordinateTransform(sourceCrs, destCrs)

# Only one of these transforms is technically necessary.
# Transforming directly
transformed = []
for rPI in points:
    transformed.append(xform.transform(rPI))

# Transforming indirectly.
transformed_coords = []
for rPI_c in coordinates:
    transformed_coords.append(xform.transform(QgsPoint(rPI_c[0], rPI_c[1])))

# Chaning directory to the place on my laptop that GIS data is stored.
os.chdir("D:\\DDPSC\\Raspberry_Pi\\GIS\\")
filename_1 = "transformed_coords.txt"
filename_2 = "jpeg_exif_coords.txt"
with open(filename_1, 'w') as fn_1:
    with open(filename_2, 'w') as fn_2:
        for index in range(len(transformed_coords)):
            trans = transformed_coords[index]
            lat = trans[0]
            lng = trans[1]
            # Printed in VisualSFM format
            print("{0} {1} {2}".format(raspberries[index], lat, lng), file=fn_1)
            if lat < 1:
                lat = abs(lat)
                lat_ref = "W"
                lat = Fraction(lat).limit_denominator()
            else:
                lat = abs(lat)
                lat_ref = "E"
                lat = Fraction(lat).limit_denominator()
            if lng < 1:
                lng = abs(lng)
                lng_ref = "S"
                lng = Fraction(lng).limit_denominator()
            else:
                lng = abs(lng)
                lng_ref = "N"
                lng = Fraction(lng).limit_denominator()
            # Printed in JPEG Exif format
            print("{IP} {lng_ref}; {lng},0/1,0/1; {lat_ref}; {lat},0/1,0/1; 0; 604/1; 2".format(IP=raspberries[index], lng_ref=lng_ref, lng=lng, lat_ref=lat_ref, lat=lat), file=fn_2)
