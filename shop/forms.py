from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team1', 'team2', 'match_date']
        widgets = {
            'match_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
