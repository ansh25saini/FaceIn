from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

YEARS= [x for x in range(2021,2031)]

class usernameForm(forms.Form):
	username=forms.CharField(max_length=30)

class DateForm(forms.Form):
	date=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"), years= YEARS))


class UsernameAndDateForm(forms.Form):
	username=forms.CharField(max_length=30)
	date_from=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years= YEARS))
	date_to=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years= YEARS))


class DateForm_2(forms.Form):
	date_from=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years= YEARS))
	date_to=forms.DateField(widget = forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years= YEARS))
 
