from django import forms


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class UnitToCorrectForm(forms.Form):
    unit = forms.IntegerField(min_value=1, max_value=12)
