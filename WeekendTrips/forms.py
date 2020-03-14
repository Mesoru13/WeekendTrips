from django import forms


class InputDataForm(forms.Form):
    travelling_time_choices = (('far', 'Ready for a long road'),
                               ('near', 'Want to get there fast'),
                               ('fair', 'Can spent more than nothing, but not too much'))
    persons_count = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                       min_value=1)
    trip_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'}))
    max_price = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}),
                                   min_value=1000)
    time_for_travel = forms.TypedMultipleChoiceField(widget=forms.CheckboxSelectMultiple(
                                                     attrs={'class': 'form-check form-check-inline'}),
                                                     choices=travelling_time_choices)
    departure_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))