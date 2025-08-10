from multiprocessing import Pool
import seaborn as sns
import numpy
import matplotlib.pyplot as plt
import pandas as pd
from django_pandas.io import read_frame
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric,add_changepoints_to_plot
from prophet.diagnostics import performance_metrics
import base64
from io import BytesIO
import time


def set_up_model1(point):
    print(point)
    x = len(point)
    r =[]
    df = read_frame(point)
    df.sort_values('date',inplace=True)
    for i in range(1,x+1):
        r.append(i)
    df['crimeCommitted'] = r
    df= df[['date',"Van"]]
    df.columns =['ds','y']
    df['ds'] = pd.DatetimeIndex(df.ds)
    df['ds']=df['ds'].dt.tz_localize(None)
    m = Prophet()         
    m.fit(df)
    return m

def set_up_model(point):
    print(point)
    x = len(point)
    r =[]
    df = read_frame(point)
    df.sort_values('date',inplace=True)
    for i in range(1,x+1):
        r.append(i)
    df['crimeCommitted'] = r
    df= df[['date',"crimeCommitted"]]
    df.columns =['ds','y']
    df['ds'] = pd.DatetimeIndex(df.ds)
    df['ds']=df['ds'].dt.tz_localize(None)
    m = Prophet()         
    m.fit(df)
    return m

def plot_crime_rate(m):
    # Simulate a time-consuming task
    a = time.time()
    pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
    forcast = m.predict(pred)
    fig = m.plot(forcast,xlabel='DATE',ylabel='PROJECTED CRIME RATE',)
    plz = add_changepoints_to_plot(fig.gca(),m,forcast)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
            # Encode PNG image to base64 string
    graph1 = base64.b64encode(image_png).decode('utf-8')
    b = time.time()
    print('plot crime rate time : ',b-a)

    return graph1

def plot_crime_rate_trends(m):
    a= time.time()
    pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
    forcast = m.predict(pred)
    comp = m.plot_components(forcast)
    buffer_comp = BytesIO()
    comp.savefig(buffer_comp, format='png')
    buffer_comp.seek(0)
    image_png1 = buffer_comp.getvalue()
    buffer_comp.close()
    graph2 = base64.b64encode(image_png1).decode('utf-8')
    b = time.time()
    print('plot crime rate trend : ',b-a)
    return graph2


def plot_cv_metric(m):
    a= time.time()
    df_cv = cross_validation(m, initial='45 days', period='5 days', horizon = '10 days')
    fig = plot_cross_validation_metric(df_cv, metric='mape',point_color='red',color='red')
    buffer_cv = BytesIO()
    fig.savefig(buffer_cv, format='png')
    buffer_cv.seek(0)
    image_png2 = buffer_cv.getvalue()
    buffer_cv.close()
    graph3 = base64.b64encode(image_png2).decode('utf-8')
    b = time.time()
    print('plot cv time : ',b-a)
    return graph3


def process_functions(funcs_with_args):
    with Pool() as pool:
        t1 = time.time()
        results = [pool.apply_async(func, args) for func, args in funcs_with_args]
        t2 = time.time()
        print('time : ',t2-t1)
        return [result.get() for result in results]