from django.forms.widgets import CheckboxSelectMultiple


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'custom_checkbox_select.html'

    def __init__(self, attrs=None, options={}):
        self.options = options

        super().__init__(attrs)
