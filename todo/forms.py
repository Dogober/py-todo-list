from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError

from todo.models import Tag, Task


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )

    def clean_deadline(self):
        current_time = datetime.now()
        if self.cleaned_data["deadline"] < current_time.date():
            raise ValidationError("Deadline should be in the future")
        return self.cleaned_data["deadline"]

    class Meta:
        model = Task
        fields = "__all__"
