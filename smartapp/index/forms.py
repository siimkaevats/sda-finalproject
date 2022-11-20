from django import forms

class AnswerForm(forms.Form):
    message = forms.CharField(max_length=500, widget=forms.Textarea, required=True)
    RemovePunctuation = forms.BooleanField(required=False)
    UpperCase = forms.BooleanField(required=False)
    LowerCase = forms.BooleanField(required=False)
    RemoveNewLine = forms.BooleanField(required=False)
    RemoveExtraSpace = forms.BooleanField(required=False)
    CountCharacters = forms.BooleanField(required=False)
    CheckSpelling = forms.BooleanField(required=False)
    GenerateSummaryofAWord = forms.BooleanField(required=False)
    RemoveStopWords = forms.BooleanField(required=False)
