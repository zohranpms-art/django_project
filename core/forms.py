from django import forms
from .models import VisitorEntry

class VisitorEntryForm(forms.ModelForm):
    class Meta:
        model = VisitorEntry
        fields = ('visitor_name', 'visitor_phone', 'visitor_photo', 'reason', 'other_reason')
        widgets = {
            'other_reason': forms.Textarea(attrs={'rows': 3}),
        }