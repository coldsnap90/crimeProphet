import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import crimeModel
import googlemaps
import os
from datetime import datetime




'command to automate data processing from csv'
class Command(BaseCommand):
    help = 'loads crime data from csv'
    def handle(self,*args,**kwargs):
        gmaps = googlemaps.Client(key=os.environ.get('G_API_KEY'))
        data_file = 'app\data\Oct_Dec_2023_New_Westminster_Police_Department_report.csv'
        keys = ('ccn','date','updateDate','city','state','postalCode','blocksizedAddress','incidentType','parentIncidentType','narrative')
        records = []
        counter = 0
        with open(data_file,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({key: row[key] for key in keys})

        recordHolder={}      
        for item in records:
            address = item['blocksizedAddress']
            city = item['city']
            address = item['blocksizedAddress']
            city = item['city']
            datePm = "%m/%d/%Y, %H:%M:%S PM"
            dateAm = "%m/%d/%Y, %H:%M:%S AM"
            dfDate = item['date']
            dfUpdateDate = item['updateDate']
            dateLength = len(datePm)
            dateUpdate= dateAm[dateLength-2:]


            try:
                dateString = datetime.strptime(dfDate,datePm)
                if dateString.hour < 12:
                    dateString = dateString.replace(hour=dateString.hour+12)
                item['date'] = dateString
    
            except:
                dateString = datetime.strptime(dfDate,dateAm)
                if dateString.hour == 12:
                    dateString = dateString.replace(hour=dateString.hour-12)   
                item['date'] = dateString

            try:
                dateString = datetime.strptime(dfUpdateDate,datePm)
                if dateString.hour < 12:
                    dateString = dateString.replace(hour=dateString.hour+12)
                item['updateDate'] = dateString
    
            except:
                dateString = datetime.strptime(dfUpdateDate,dateAm)
                if dateString.hour == 12:
                    dateString = dateString.replace(hour=dateString.hour-12)   
                item['updateDate'] = dateString

            if address not in recordHolder:
                result = gmaps.geocode(f'{address},{city}')[0]
                coords = result.get('geometry',{}).get('location',{})
                lat = coords['lat']
                lon = coords['lng']
                recordHolder[address]= f'{lat},{lon}'
                item['lat'] = lat
                item['long'] = lon

            else:
                latLon = recordHolder[address].split(',')
                item['lat'] = float(latLon[0])
                item['long'] = float(latLon[1])
          
            crimeModel.objects.get_or_create(ccn = item['ccn'],
                                             date = item['date'],
                                             update_date = item['updateDate'],
                                             city = item['city'],
                                             province = item['state'],
                                             postal_code = item['postalCode'],
                                             address = item['blocksizedAddress'],
                                             incident = item['incidentType'],
                                             incident_class = item['parentIncidentType'],
                                             narrative = item['narrative'],
                                             latitude = item['lat'],
                                             longitude = item['long'])

            

          
     
        
           
       