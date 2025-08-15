from multiprocessing import Pool
import pandas as pd
from django_pandas.io import read_frame
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric,add_changepoints_to_plot
from prophet.diagnostics import performance_metrics
import base64
from io import BytesIO



'''sets ip forcasint model'''
def set_up_model(point):

    dataLength = len(point)
    dataList =[]
    df = read_frame(point)
    df.sort_values('date',inplace=True)
    for i in range(1,dataLength+1):
        dataList.append(i)
    df['crimeCommitted'] = dataList
    df= df[['date',"crimeCommitted"]]
    df.columns =['ds','y']
    df['ds'] = pd.DatetimeIndex(df.ds)
    df['ds']=df['ds'].dt.tz_localize(None)
    m = Prophet()         
    m.fit(df)
    return m

'''plots crime rate trend and future predicted crime rate'''
def plot_crime_rate(m):

    pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
    forcast = m.predict(pred)
    fig = m.plot(forcast,xlabel='DATE',ylabel='PROJECTED CRIME RATE',)
    plz = add_changepoints_to_plot(fig.gca(),m,forcast)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph1 = base64.b64encode(image_png).decode('utf-8')
    return graph1

'''plots crime rate trends and forcasts future for weekly,monthly, and yearly'''
def plot_crime_rate_trends(m):
    pred = m.make_future_dataframe(periods=9,freq='ME',include_history=True)
    forcast = m.predict(pred)
    comp = m.plot_components(forcast)
    buffer_comp = BytesIO()
    comp.savefig(buffer_comp, format='png')
    buffer_comp.seek(0)
    image_png1 = buffer_comp.getvalue()
    buffer_comp.close()
    graph2 = base64.b64encode(image_png1).decode('utf-8')
    return graph2

'''plots cross validation metric'''
def plot_cv_metric(m):
    df_cv = cross_validation(m, initial='45 days', period='5 days', horizon = '10 days')
    fig = plot_cross_validation_metric(df_cv, metric='mape',point_color='red',color='red')
    buffer_cv = BytesIO()
    fig.savefig(buffer_cv, format='png')
    buffer_cv.seek(0)
    image_png2 = buffer_cv.getvalue()
    buffer_cv.close()
    graph3 = base64.b64encode(image_png2).decode('utf-8')
    return graph3


'''uses multiprocessing to  process the functions and graphs in parallel'''
def process_functions(funcs_with_args):
    with Pool() as pool:
        results = [pool.apply_async(func, args) for func, args in funcs_with_args]
        return [result.get() for result in results]