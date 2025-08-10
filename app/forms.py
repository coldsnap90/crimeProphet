from django import forms
from datetime import date,datetime

class filterForm(forms.Form):
  
    start_date= forms.DateTimeField(label="START",initial=datetime(2023,1,1),required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"])
    end_date = forms.DateTimeField(label="END",initial=datetime.now(),required=False,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"])
    crime = forms.ChoiceField(label='SELECT CRIME',choices=[('ALL','ALL'),('THEFT','THEFT'),('FRAUD','FRAUD'),('MISCHIEF','MISCHIEF'),('BREAK & ENTER','BREAK & ENTER'),
                                                             ('ARSON','ARSON'),('THEFT OF AUTO UNDER $5000','THEFT OF AUTO UNDER $5000'),('THEFT OF AUTO UNDER $5000','THEFT OF AUTO OVER $5000'),
                                                             ('ROBBERY','ROBBERY'),('RECOVERED OUTSIDE STOLEN VEH','RECOVERED OUTSIDE STOLEN VEH'),
                                                             ('COUNTERFEITING CURRENCY','COUNTERFEITING CURRENCY'),('Homicide','HOMICIDE'),('ASSAULT','ASSAULT'),('SEXUAL ASSAULT','SEXUAL ASSAULT')],required=False)


class dataForm(forms.Form):
  
    start_date= forms.DateTimeField(label="START",initial=datetime(2023,1,1),required=True,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"])
    end_date = forms.DateTimeField(label="END",initial=datetime.now(),required=False,widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"])
    crime = forms.ChoiceField(label='SELECT CRIME',choices=[('',''),('ALL','ALL'),('THEFT','THEFT'),('FRAUD','FRAUD'),('MISCHIEF','MISCHIEF'),('BREAK & ENTER','BREAK & ENTER'),
                                                             ('ARSON','ARSON'),('THEFT OF AUTO UNDER $5000','THEFT OF AUTO UNDER $5000'),('THEFT OF AUTO UNDER $5000','THEFT OF AUTO OVER $5000'),
                                                             ('ROBBERY','ROBBERY'),('RECOVERED OUTSIDE STOLEN VEH','RECOVERED OUTSIDE STOLEN VEH'),
                                                             ('COUNTERFEITING CURRENCY','COUNTERFEITING CURRENCY'),('HOMICIDE','HOMICIDE'),('ASSAULT','ASSAULT'),('SEXUAL ASSAULT','SEXUAL ASSAULT')],required=False)

    graph_options = forms.MultipleChoiceField(
        choices=[
            ('option1', 'Crime Rate Prediction'),
            ('option2', 'Daily, Weekly, and Monthly Crime Rate Prediction'),
            ('option3', 'Mean Absolute Percentage Error of Prediction')
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Select Graphs'
    )
