from django.shortcuts import render,redirect
from app.models import crimeModel
from app.forms import filterForm,dataForm
import folium
from app.functions import plot_cv_metric,plot_crime_rate,plot_crime_rate_trends,process_functions,set_up_model
import time
from django.contrib import messages


def redirect_to_home(request):
    return redirect('home')


'''view to filter crimes from the database and plot them on a map'''
def home(request):
    crimes = crimeModel.objects.all()
    form = filterForm()

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

'''view to create plots based of ML model predictions'''
def create_plot(request):
    messages.success(request, 'Increasing date windows will lead to larger loading time for data.')
    crimes = crimeModel.objects.all()
    if request.method == 'POST':
        form = dataForm(request.POST)
        if form.is_valid():
          

            start_date = str(form.cleaned_data['start_date'])
            end_date = str(form.cleaned_data['end_date'])
            crime = form.cleaned_data['crime']
       
            end_points = crimes.filter(date__lte=end_date).all() & crimes.filter(date__gte=start_date).all()

            if crime != 'ALL':
                end_points = end_points.filter(incident__istartswith=crime).all()
           
            m = set_up_model(end_points)
            funcs_with_args = []
            selected_options = form.cleaned_data['graph_options']
          
            if 'option1' in selected_options:
                funcs_with_args.append((plot_crime_rate, (m,)))

            if 'option2' in selected_options:
                funcs_with_args.append((plot_crime_rate_trends, (m,)))

            if 'option3' in selected_options:
                funcs_with_args.append((plot_cv_metric, (m,)))


            results = []
            results = process_functions(funcs_with_args)

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
    

