import csv
import django
from django.conf import settings

import googlemaps
import os
import random
from datetime import datetime
from app.models import crimeModel

import pandas as pd

import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from app.models import crimeModel
import googlemaps
import os
from datetime import datetime
import seaborn as sns
import numpy
import matplotlib.pyplot as plt
from django_pandas.io import read_frame
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric,add_changepoints_to_plot
from prophet.diagnostics import performance_metrics

class Command(BaseCommand):
    help = 'loads crime data from csv'
    def handle(self,*args,**kwargs):
        handle_option = 1
        if handle_option == 1:
            crimes = crimeModel.objects.all()
            point = crimes.filter(date__gte='2023-10-2').all()
            counter = 2130
            df = read_frame(point)
            df.sort_values('date',inplace=True)
            x= len(point)
            print('len ',len(df))
            r =[]
            for i in range(x):
                r.append(counter+i)
            print(r)
            print('CRIME')
            df['crimeCommitted'] = r
            print(df)
            df.to_csv(r'C:\Users\cfarb\OneDrive\Desktop\stats\app\data\Oct_Dec_2023_New_Westminster_Police_Department_report_new.csv')
        elif handle_option == 3:
            x = 'app\data\Jan_Mar_2023_New_Westminster_Police_Department_report_newest.csv'
        
            df = pd.read_csv(x)
            print('shape : ',df.shape)


        elif handle_option == 2:
                x = 'app\data\Jan_Mar_2023_New_Westminster_Police_Department_report_newest.csv'
                
                df = pd.read_csv(x)
                #df = read_frame(x)
                df.sort_values('date',inplace=True)
                counter = 0
                x= len(df)
                print('len ',len(df))
                
                print(df.head())
                print(df.tail())
            
                #df.index = pd.DatetimeIndex(df.date)
                
                print(df)
                print('creating index')
                print('index')
                df= df[['date',"crimeCommitted"]]
                #df.sort_values(df['date'],inplace=True)
                #df_prophet = pd.DataFrame(df.resample('ME').size().reset_index())
                #df = df[['date','crimeCommitted','longitude','latitude']]
                #df = df[['date','longitude','incident']]
                #df = df[['date','longitude']]
                
                print('COLUMNS')
            
                #df.columns =['ds','y','incident']
                df.columns =['ds','y']
                df['ds'] = pd.DatetimeIndex(df.ds)
                df['ds']=df['ds'].dt.tz_localize(None)

                #df_encoded = pd.get_dummies(df, columns=['incident'])
                #df_encoded.rename(columns={'incident': 'original_incident'}, inplace=True)
                #print(df_encoded)
                #prophet_df = df_encoded[['ds', 'y', 'incident_ARSON-PROPERTY']]
                #df_encoded.to_csv(r'C:\Users\cfarb\OneDrive\Desktop\stats\app\data\df.csv') 
                print(' ** PROPHET DF ** \n\n\n')
                print(df)
                m = Prophet()
                print('prophet')
                #m.add_regressor('incident_ARSON-PROPERTY')
                m.fit(df)
                pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
                df_cv = cross_validation(m, initial='60 days', period='5 days', horizon = '30 days')
                print(pred)
                forcast = m.predict(pred)
                print(forcast)
                print('plot1')
                #plot_plotly(m, forcast)
                print('plotting')
                plt = m.plot(forcast,xlabel='DATE',ylabel='PROJECTED CRIME RATE',)
                plz = add_changepoints_to_plot(plt.gca(),m,forcast)
                comp = m.plot_components(forcast)
                fig = plot_cross_validation_metric(df_cv, metric='mape',point_color='red',color='red')
                print('fig')

                plt.show()
                comp.show()
                fig.show()
                df_p = performance_metrics(df_cv)
                print(df_p)
                x=input()
                    
        
       
        
def check():    
        #x = 'app\data\Jan_Mar_2023_New_Westminster_Police_Department_report_newest.csv'
        
        df = pd.read_csv(x)
        #df = read_frame(x)
        df.sort_values('date',inplace=True)
        counter = 0
        x= len(df)
        print('len ',len(df))
        #r =[]
        #for i in range(x):
         #   counter+=1
          #  r.append(counter)
        #df['crimeCommitted'] = r
            #print(df['crime committed'])
        #print(df)
        #
   
        #df.to_csv(r'C:\Users\cfarb\OneDrive\Desktop\stats\app\data\Jan_Mar_2023_New_Westminster_Police_Department_report_newest.csv')
        print(df.head())
        print(df.tail())
      
        #df.index = pd.DatetimeIndex(df.date)
        
        print(df)
        #x = df.index

        #df= df[[df.index,"crimeCommitted"]]
        #df.sort_values(df['date'],inplace=True)
        #df_prophet = pd.DataFrame(df.resample('ME').size().reset_index())
        df = df[['date','crimeCommitted']]


        df.columns =['ds','y']
        df['ds'] = pd.DatetimeIndex(df.ds)
        df['ds']=df['ds'].dt.tz_localize(None)

   
        m = Prophet()
        print('prophet')
        m.fit(df)
        pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
    
        print(pred)
        forcast = m.predict(pred)
        print(forcast)
        print('plot1')
        #plot_plotly(m, forcast)
        print('plotting')
        plt = m.plot(forcast,xlabel='date',ylabel='crime rate')

        plt.show()
        x=input()
        
       
   
'''
gmaps = googlemaps.Client(key=os.environ.get('G_API_KEY'))
print(os.environ.get('G_API_KEY'))

data_file = 'app\data\Jan_Mar_2023_New_Westminster_Police_Department_report.csv'
data = pd.read_csv(data_file, nrows=5)
print(data)

keys = ('ccn','date','updateDate','city','state','postalCode','blocksizedAddress','incidentType','parentIncidentType','narrative')
newdic={}
newrec=[]
records = []
with open(data_file,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
                records.append({k: row[k] for k in keys})

        recordHolder={}      
        for item in records:
            address = item['blocksizedAddress']
            city = item['city']

            if address not in recordHolder:
                #result = gmaps.geocode(f'{address},{city}')[0]
               #coords = result.get('geometry',{}).get('location',{})
                #recordHolder[address]= f'{coords['lat']}-{coords['lng']}'
                item['lat'] = 1
                item['long'] = -1

            else:
                latLon = recordHolder[address].split(',')
                item['lat'] = float(latLon[0])
                item['long'] = float(latLon[1])
                
            
print(records)

'''
data_file = 'app\data\Jan_Mar_2023_New_Westminster_Police_Department_report.csv'
keys = ('ccn','date','updateDate','city','state','postalCode','blocksizedAddress','incidentType','parentIncidentType','narrative')
records = []
dict1 ={}
akey = 'AIzaSyC8yfCMb28SfhhVnF1SLDOG6t-sW2-lHtg'


#r = gmaps.geocode('900 block 12TH ST, NEW WESTMINSTER')[0]
#print(r)
#x = r.get('geometry',{}).get('location',{})
rec=[]
#d = [{'ccn': '23-4865', 'date': '03/28/2023, 8:18:00 PM', 'updateDate': '04/22/2023, 4:07:18 PM', 'city': 'NEW WESTMINSTER', 'state': 'BC', 'postalCode': 'V3L 1P3', 'blocksizedAddress': '1 Block AVE & 6TH ST', 'incidentType': 'MISCHIEF $5000 OR UNDER', 'parentIncidentType': 'Property Crime', 'narrative': 'MISCHIEF $5000 OR UNDER' },
     #{'ccn': '23-4866', 'date': '03/28/2023, 8:18:00 PM', 'updateDate': '04/22/2023, 4:07:18 PM', 'city': 'NEW WESTMINSTER', 'state': 'BC', 'postalCode': 'V3L 1P3', 'blocksizedAddress': '1 Block AVE & 6TH ST', 'incidentType': 'MISCHIEF $5000 OR UNDER', 'parentIncidentType': 'Property Crime', 'narrative': 'MISCHIEF $5000 OR UNDER'},
     #{'ccn': '23-4867', 'date': '03/29/2023, 8:18:00 PM', 'updateDate': '04/22/2023, 4:07:18 PM', 'city': 'NEW WESTMINSTER', 'state': 'BC', 'postalCode': 'V3L 1P3', 'blocksizedAddress': '300 Block AVE & 6TH ST', 'incidentType': 'MISCHIEF $5000 OR UNDER', 'parentIncidentType': 'Property Crime', 'narrative': 'MISCHIEF $5000 OR UNDER'}
     #]
'''
recordHolder={}    
with open(data_file,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
         
                records.append({k: row[k] for k in keys})

        recordHolder={}   
   
        for item in records:
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
                print( item['date'],' ',p)
                item['date'] = p
    
            except:
                p = datetime.strptime(x,z)
                if p.hour < 12:
                     print( item['date'],' ',p)
                     x = input('wait')
                if p.hour == 12:
                    p = p.replace(hour=p.hour-12)   
                    print( item['date'],' ',p)
                item['date'] = p

            try:
                p = datetime.strptime(h,a)
                if p.hour < 12:
                    p = p.replace(hour=p.hour+12)
                    print( item['updateDate'],' ',p)
                item['updateDate'] = p
    
            except:
                p = datetime.strptime(h,z)
                if p.hour == 12:
                    p = p.replace(hour=p.hour-12)  
                    print( item['updateDate'],' ',p)
                item['updateDate'] = p
              

            k = item['blocksizedAddress']
            z = item['city']
            y = item['postalCode']
            if k not in recordHolder:

                #r = gmaps.geocode(f'{k},{z}')[0]
                #x = r.get('geometry',{}).get('location',{})
              
                m = random.randint(0,1000)
                n = random.randint(0,1000)
                recordHolder[k]= f'{m},{n}'
                item['lat'] = 49.2026537
                item['long'] = -122.9059804
            else:
        
                g = recordHolder[k].split(',')
                item['lat'] = float(g[0])
                item['long'] = float(g[1])

            dict2={
            'ccn' : item['ccn'],
                'date': item['date'],
                'update_date' : item['updateDate'],
            'city' :item['city'],
            'province' : item['state'],
            'postal_code' : item['postalCode'],
            'address' : item['blocksizedAddress'],
            'incident' : item['incidentType'],
            'incident_class' : item['parentIncidentType'],
            'narrative' : item['narrative'],
            'latitude' : item['lat'],
            'longitude' : item['long']
            }
            rec.append(dict2)
#print(records)
#print(len(records))

      

date_str_split = date_str.split('-')
            date_str2_split = date_str2.split('-')

            print(date_str,date_str2)
            print(date_str[0],type(date_str))
          
            date_obj = datetime(int(date_str_split[0]),int(date_str_split[1]),int(date_str_split[2]),0,0,0,tzinfo=timezone(timedelta(seconds=7200)))
            date_obj2 = datetime(int(date_str2_split[0]),int(date_str2_split[1]),int(date_str2_split[2]),0,0,0,tzinfo=timezone(timedelta(seconds=7200)))
            try:
                crimes = crimes.filter(date__gte=date_obj).values() | crimes.filter(date__gte =date_obj2).values()
                print('crimes2 : ',crimes)
            except:
                print('fail 2 loop')
                
            date_obj = str(date_obj)
            date_obj2 = str(date_obj2)
            print('date object',date_obj,type(date_obj),date_obj2,type(date_obj2))
            start_date = datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S%z')
            end_date = datetime.strptime(date_obj2, '%Y-%m-%d %H:%M:%S%z')
         
            print(start_date,end_date)
            crimes = crimes.filter(date__gte=start_date).values() | crimes.filter(date__gte =end_date).values()
            print('crimes 3 : ',crimes)
'''
'''
   x = crimeModel.objects.all()
        z = len(x)
        print(z)
        
        for i in range(1,2):
            print(records[i]['date'],type(records[i]['date']))
            dstrt= datetime.strptime(records[i]['date'], '%Y-%m-%d %H:%M:%S%z')
            dstr = datetime.strptime(records[i]['updateDate'], '%Y-%m-%d %H:%M:%S%z')
            print(dstrt,type(dstrt))
            crimeModel.objects.filter(id=i).update(date=dstrt,update_date=dstr)
'''

'''
for item in records[0:2]:
       

       k = item['blocksizedAddress']
       z = item['city']
       y = item['postalCode']
       r = gmaps.geocode(f'{k},{z}')[0]
       x = r.get('geometry',{}).get('location',{})
       
       
       item['lat'] = x['lat']
       item['long'] = x['lng']
       print(k,y,z,x)
       print(x['lat'],type(x['lat']))
       print(x['lng'],type(x['lng']))
       reverse_geocode_result = gmaps.reverse_geocode((x['lat'], x['lng']))[0]
       #print('RV ',reverse_geocode_result)
       

print('/n ',records[0:2])


#print(dict1)
'''
'''
def create_plot1(request):
    messages.success(request, 'Increasing date windows will lead to larger loading time for data.')
    crimes = crimeModel.objects.all()
    if request.method == 'POST':
        form = dataForm(request.POST)
        if form.is_valid():
          

            start_date = str(form.cleaned_data['start_date'])
            end_date = str(form.cleaned_data['end_date'])
            crime = form.cleaned_data['crime']
            print('crime : ',crime)
       
            end_points = crimes.filter(date__lte=end_date).all() & crimes.filter(date__gte=start_date).all()
            print('end points1 : ',end_points)
            if crime != 'ALL':
                end_points = end_points.filter(incident__istartswith=crime).all()
                print('end points all : ',end_points)
          
           
            m = set_up_model(end_points)

            funcs_with_args = []
            selected_options = form.cleaned_data['graph_options']
          
            if 'option1' in selected_options:
                print('appending')
                funcs_with_args.append((plot_crime_rate, (m,)))

            if 'option2' in selected_options:
                print('appending')
                funcs_with_args.append((plot_crime_rate_trends, (m,)))

            if 'option3' in selected_options:
                print('appending')
                funcs_with_args.append((plot_cv_metric, (m,)))

            x = time.time()
            results = []
            results = process_functions(funcs_with_args)
 
            y = time.time()
            print('total time async: ',y-x)
            form = dataForm()
            context = {'chart':True,'form':form}
            counter=1
            for pic in results:
                    context[ f'graph{counter}']= pic
                    counter+=1

            #Render the HTML template with the graph
           
            return render(request, 'graphs.html', context)
    else:
        form = dataForm()
        context = {'form':form,'chart':False}
        return render(request, 'graphs.html',context)
'''