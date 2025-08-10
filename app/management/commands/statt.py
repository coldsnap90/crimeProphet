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
1

if 1==1:
                x = 'app/data/van.csv'
                
                dataChecker = csv.reader(open(x))
                for i in dataChecker:
                        print(i)
                        
                
                print(type(x), x)              
                df = pd.read_csv(x,quotechar='"', delimiter=",")
                print(df.head())
                print('true')
                df= df[['date',"onsite"]]
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
                m.fit(df)
                pred = m.make_future_dataframe(periods=1,freq='ME',include_history=True)
            
                print(pred)
                forcast = m.predict(pred)
                forecast_positive = forcast[forcast['yhat'] >= 0]
                print(forcast)
                print('plot1')
                #plot_plotly(m, forcast)
                print('plotting')
                
                plt = m.plot(forcast,xlabel='DATE',ylabel='NUMBER OF TIMES VAN SPOTTED')
                ax = plt.gca()
                ax.set_ylim(0,45)
                plz = add_changepoints_to_plot(plt.gca(),m,forcast)
                comp = m.plot_components(forcast)
                plt.show()
                comp.show()
                plt.savefig('prophet_forecast.png', dpi=300)
                x = input()
                print('fig')
                