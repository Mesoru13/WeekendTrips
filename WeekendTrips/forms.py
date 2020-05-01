from django import forms
import datetime
from bootstrap_datepicker_plus import DatePickerInput
from WeekendTrips.widgets import CustomCheckboxSelectMultiple
from WeekendTrips.settings import STATIC_ROOT
import io


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
    travelling_time_choices = (('far', 'Much'),
                               ('fair', 'Average'),
                               ('near', 'A little'))

    persons_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                       'hidden': 'true'}),
                                       min_value=1,
                                       initial=1,
                                       required=True)
    min_date = get_nearest_weekend() - datetime.timedelta(days=1)
    if datetime.date.today() == get_nearest_weekend():
        min_date = get_nearest_weekend()

    start_date = forms.DateField(widget=DatePickerInput(
        format='%Y-%m-%d',
        options={
            'minDate': str(min_date),
        }),
        initial=get_nearest_weekend(),
        required=True)
    end_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d',
                                                      options={
                                                          'minDate': str(min_date)
                                                      }),
                               initial=get_nearest_weekend() + datetime.timedelta(days=1),
                               required=True)
    max_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                   initial=10000,
                                   required=True)
    time_for_travel = forms.TypedMultipleChoiceField(widget=CustomCheckboxSelectMultiple(
        attrs={'class': 'form-check form-check-inline'}),
        choices=travelling_time_choices,
        initial=['far', 'fair', 'near'],
        required=True)

    departure_city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control basicAutoComplete',
        'style': 'position: relative',
        'name': 'simple_select',
        'placeholder': 'Type to search...',
        'autocomplete': 'off'}),
        initial='Москва')

    def clean_start_date(self):
        data = self.cleaned_data['start_date']
        return data

    def clean_end_date(self):
        data = self.cleaned_data['end_date']
        return data

    def clean_departure_city(self):
        data = self.cleaned_data['departure_city']

        cities = []
        path = STATIC_ROOT + '/cities.txt'
        was_found = False;
        with io.open(path, encoding='utf-8') as file:
            for line in file:
                if data in line:
                    was_found = True

        if not was_found:
            raise forms.ValidationError('Sorry, but your departure city is not supported now. Please try the nearest '
                                        'city with a railway station or an airport.')

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
