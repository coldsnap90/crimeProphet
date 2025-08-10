import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import crimeModel
import googlemaps
import os
from datetime import datetime





class Command(BaseCommand):
    help = 'loads crime data from csv'
    def handle(self,*args,**kwargs):
        print('handle called')
        gmaps = googlemaps.Client(key=os.environ.get('G_API_KEY'))
        data_file = 'app\data\Oct_Dec_2023_New_Westminster_Police_Department_report.csv'
        keys = ('ccn','date','updateDate','city','state','postalCode','blocksizedAddress','incidentType','parentIncidentType','narrative')
        records = []
        print('file open')
        counter = 0
        with open(data_file,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                records.append({k: row[k] for k in keys})

        recordHolder={}      
        for item in records:
            address = item['blocksizedAddress']
            city = item['city']
            a = "%m/%d/%Y, %H:%M:%S PM"
            z = "%m/%d/%Y, %H:%M:%S AM"
            x = item['date']
            h = item['updateDate']
            l = len(x)
            j=x[l-2:]

            try:
                p = datetime.strptime(x,a)
                if p.hour < 12:
                    p = p.replace(hour=p.hour+12)
                item['date'] = p
    
            except:
                p = datetime.strptime(x,z)
                if p.hour == 12:
                    p = p.replace(hour=p.hour-12)   
                item['date'] = p

            try:
                p = datetime.strptime(h,a)
                if p.hour < 12:
                    p = p.replace(hour=p.hour+12)
                item['updateDate'] = p
    
            except:
                p = datetime.strptime(h,z)
                if p.hour == 12:
                    p = p.replace(hour=p.hour-12)   
                item['updateDate'] = p

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
            print(item)
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

            

          
     
        
           
       