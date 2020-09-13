from shapely.geometry import Polygon
import json
import os
import pandas as pd
import requests
import time

## When proxy required
import sys,os,os.path
os.environ['http_proxy']="http://1272471:Prince%4005@proxy.tcs.com:8080"
os.environ['https_proxy']="http://1272471:Prince%4005@proxy.tcs.com:8080"

## When proxy not required
# import sys,os,os.path
# os.environ['http_proxy']=""
# os.environ['https_proxy']=""

startRow =0
startCol =0
deltaLat = 0.01225
deltaLon = 0.01372
zoom = '16'
scale = '2'
format1 = 'png32'
size = '640x640'
sleep = '1000'
key = 'AIzaSyBMb9jG5J_hCFA3iafDNGBozVVX88uBAcQ'

districtData = pd.read_csv('/home/datateam/Chanpreet/District.csv')
outputFolder = '/home/datateam/Chanpreet/Downloaded_images'
outputFiles = '/home/datateam/Chanpreet/Downloaded_images_Latlong'
folder = '/home/datateam/Chanpreet/AllDistrictBoundary'

count =1
for files in os.listdir(folder):
    latlongFile = []
    latlongFile.append(['District Id','District Name','ImagePath','LatLong'])
    saveFileName = ""
    if '.geojson' in files:
        print files
        fileName = os.path.join(folder,files)
        districtId =  int(files.split('.')[0])
        districtName = districtData[districtData['districtId']==districtId]['Districtname'].values[0]
        print districtId,districtName
        saveFileName = districtName+'_'+str(districtId)
        if not os.path.exists(os.path.join(outputFolder,districtName+'_'+str(districtId))):
			os.mkdir(os.path.join(outputFolder,districtName+'_'+str(districtId)))
			# resultPath = os.path.join(outputFolder,districtName+'_'+str(districtId))
        
        resultPath = os.path.join(outputFolder,districtName+'_'+str(districtId))
        already_data = len(os.listdir(resultPath))

        try:
            with open(fileName,'r') as f:
                data = json.load(f)
            try:
                print 'try'
                cdnates =  data['features'][0]['geometry']['coordinates'][0][0]
                boundary = Polygon(cdnates)
                bounds = boundary.bounds
                startLong,startLat,endLong,endLat = bounds[0], bounds[1], bounds[2], bounds[3]
                totalRows = int((endLat - startLat) / deltaLat)
                totalCols = int((endLong - startLong) / deltaLon)
            except:
                print 'catch'
                cdnates =  data['features'][0]['geometry']['coordinates'][0]

                boundary = Polygon(cdnates)
                bounds = boundary.bounds
                startLong,startLat,endLong,endLat = bounds[0], bounds[1], bounds[2], bounds[3]
                totalRows = int((endLat - startLat) / deltaLat)
                totalCols = int((endLong - startLong) / deltaLon)
                
            print 'Startlat :',startLat, ', StartLong :',startLong,', EndLat :',endLat,', EndLong :',endLong
            
            lat = endLat
            print 'Rows :', totalRows
            print 'Cols :', totalCols
            totalImages = totalRows * totalCols
            if totalImages == already_data:
                print 'already done'
            else:
                # print already_data
                startRow = already_data / totalCols
                if already_data==0 or startRow ==0:
                    startCol = 0
                else:
                    startCol = already_data % (startRow*totalCols)
                # print startRow,' ',startCol
                for i in range(totalRows):
                    lon = startLong
                    if i >= startRow:
                        for j in range(totalCols):
                            if count % 1000 == 0:
                                time.sleep(600)

                            if (i == startRow) and (j < startCol):
                                lon += deltaLon
                                print 'gone'
                                continue

                            query = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(lon) + "&zoom=" + zoom + "&size=" + size + "&scale=" + scale + "&format=" + format1 + "&maptype=satellite&sensor=false&key=" + key;
                            # query = "http://maps.googleapis.com/maps/api/staticmap?center=24.3648430163,85.1415533747&zoom=20&size=640x640&scale=2&format=png32&maptype=satellite&sensor=false&key=AIzaSyBMb9jG5J_hCFA3iafDNGBozVVX88uBAcQ"
                            print query
                            image = requests.get(query)
                            print image
                            while '200' not in str(image):
                                print 'ander aa gya'
                                time.sleep(60*60*5)
                                query = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(lat) + "," + str(lon) + "&zoom=" + zoom + "&size=" + size + "&scale=" + scale + "&format=" + format1 + "&maptype=satellite&sensor=false&key=" + key;
                                image = requests.get(query)

                            with open(os.path.join(resultPath,'image'+str(i)+'-'+str(j)+'.jpg'),'w')  as f:
                                f.write(image.content)
                            print 'image'+str(i)+'-'+str(j)+'.jpg'
                            print districtName+'_'+str(districtId)
                            count = count +1
                            lon += deltaLon
                            temp = []
                            temp.append(districtId)
                            temp.append(districtName)
                            temp.append(os.path.join(resultPath,'image'+str(i)+'-'+str(j)+'.jpg'))
                            temp.append(str(lat)+","+str(lon))
                            latlongFile.append(temp)
                            time.sleep(10)

                    lat -= deltaLat
                                         
            
        except Exception, ex:
            print str(ex)
            print districtId,districtName

            print '-----'
    latlongFile  = pd.DataFrame(latlongFile)
    latlongFile.to_csv(os.path.join(outputFiles,saveFileName+".csv"))

# lat = 1.3614405  (111.138) km
# lon = 1.52732412 (111.321) km 

# print 'a'