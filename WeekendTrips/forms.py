from django import forms
import datetime
from bootstrap_datepicker_plus import DatePickerInput


def get_nearest_weekend():
    nearest_weekend = datetime.date.today()
    weekday = nearest_weekend.weekday()
    if weekday < 5:
        nearest_weekend = nearest_weekend + datetime.timedelta(days=(5 - weekday))
    else:
        # в случае субботы-воскресенья считаем, что ближайшие выходные не текущие, а следующие
        nearest_weekend = nearest_weekend + datetime.timedelta(days=(12 - weekday))
    return nearest_weekend


class InputDataForm(forms.Form):
    travelling_time_choices = (('far', 'Much (~X hours)'),
                               ('fair', 'Average (~Y hours)'),
                               ('near', 'A little (less than Z hours)'))
    persons_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                       min_value=1, initial=1, required=True)
    # временно фиксируем это поле на ближайших выходных
    start_date = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'),
                                 initial=get_nearest_weekend(), disabled=True, required=True)
    end_date = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'),
                               initial=get_nearest_weekend() + datetime.timedelta(days=1),
                               disabled=True, required=True)
    max_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                   initial=10000, required=True)
    time_for_travel = forms.TypedMultipleChoiceField(widget=forms.CheckboxSelectMultiple(
                                                     attrs={'class': 'form-check form-check-inline'}),
                                                     choices=travelling_time_choices,
                                                     initial=['far', 'near', 'fair'],
                                                     required=True)
    departure_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                     initial='Moscow',
                                     required=True)

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        return data

    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        return data

    def clean_departure_city(self):
        data = self.cleaned_data['departure_city']
        return data

    def clean_max_price(self):
        data = self.cleaned_data['max_price']
        return data

    def clean_persons_count(self):
        data = self.cleaned_data['persons_count']
        return data

    def clean_time_for_travel(self):
        data = self.cleaned_data['time_for_travel']
        return data
