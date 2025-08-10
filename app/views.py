from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from app.models import crimeModel
from app.forms import filterForm,dataForm
import folium
from datetime import datetime,timezone,timedelta
from django.utils import dateparse
from io import BytesIO
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
from app.functions import plot_cv_metric,plot_crime_rate,plot_crime_rate_trends,process_functions,set_up_model
import time
from django.contrib import messages


def redirect_to_home(request):
    return redirect('home')

def home(request):
    crimes = crimeModel.objects.all()
    print('form')
    form = filterForm()
    print('error')
    
    map = folium.Map(location=[49.20678000,-122.91092000],zoom_start=9)
    if request.method == 'POST':
        form = filterForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Increasing date windows will lead to larger loading time for data.')
            start_date= str(form['start_date'].data)
            end_date = str(form['end_date'].data)
            crime = form['crime'].data
            if crimes.filter(city='NEW WESTMINSTER').all():
                map = folium.Map(location=[49.20678000,-122.91092000],zoom_start=12)

            end_points = crimes.filter(date__lte=end_date).all() & crimes.filter(date__gte=start_date).all()
            
            if crime != 'ALL':
                end_points = end_points.filter(incident__istartswith=crime).all()
                

            for  point in end_points:
                st = str(point.date)
                st = st[0:19]
        
                coords = (point.latitude,point.longitude)
                coord = folium.Marker(coords).add_to(map)
                text = f''' <b>Date and Time : {st} hours<b> <br><br> <b>Address : {point.address}<b> <br><br> <b>City : {point.city}<b>'''
                folium.Marker(coords,popup=text,parse_html=
                True).add_to(map)

    context = {'map':map._repr_html_(),'form':form}
    return render(request,'index.html',context)


def create_plot(request):
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



           
            # Render the HTML template with the graph
           
            return render(request, 'graphs.html', context)
    else:
        form = dataForm()
        context = {'form':form,'chart':False}
        return render(request, 'graphs.html',context)
    
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



           
            # Render the HTML template with the graph
           
            return render(request, 'graphs.html', context)
    else:
        form = dataForm()
        context = {'form':form,'chart':False}
        return render(request, 'graphs.html',context)

def index1(request):
    crimes = crimeModel.objects.all()
    
    
    #map = folium.Map(location=[49.20678000,-122.91092000],zoom_start=19)
    #if request.method == 'POST':
     #   form = filterForm(request.POST)
      #  if form.is_valid():
  
       #     for crime in crimes:
        #        coords = (crime.latitude,crime.longitude)
         #       coord = folium.Marker(coords).add_to(map)
    
    context = {'map':map._repr_html_()}
    return render(request,'index.html',context)
  