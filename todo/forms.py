from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError

from todo.models import Tag, Task


class TaskForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control",
            }
        )
    )

    def clean_deadline(self):
        current_time = timezone.now()
        if self.cleaned_data["deadline"] and self.cleaned_data["deadline"] < current_time:
            raise ValidationError("Deadline should be in the future")
        return self.cleaned_data["deadline"]

    class Meta:
        model = Task
        fields = "__all__"
