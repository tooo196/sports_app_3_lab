# athletes/forms.py
from django import forms
from .models import Athlete

class AthleteForm(forms.ModelForm):
	class Meta:
		model = Athlete
		fields = ['name', 'surname', 'age', 'sport', 'achievements']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'surname': forms.TextInput(attrs={'class': 'form-control'}),
			'age': forms.NumberInput(attrs={'class': 'form-control'}),
			'sport': forms.Select(attrs={'class': 'form-control'}),
			'achievements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
		}

	def clean_age(self):
		age = self.cleaned_data.get('age')
		if age < 10 or age > 100:
			raise forms.ValidationError("Возраст должен быть от 10 до 100 лет")
		return age

class FileUploadForm(forms.Form):
	file = forms.FileField(
		label='Выберите файл',
		widget=forms.FileInput(attrs={'class': 'form-control'}),
		help_text='Поддерживаются файлы JSON и XML'
	)