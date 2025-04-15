from django import forms

class TimetableForm(forms.Form):
    name = forms.CharField(label='Timetable Name', max_length=100)