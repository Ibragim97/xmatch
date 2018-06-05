from django import forms

from .models import Subject


class SubjectsForm(forms.Form):

    sub_abbr_1 = forms.CharField()
    sub_title_1 = forms.CharField()
    sub_credits_1 = forms.CharField(required=False)

    sub_abbr_2 = forms.CharField(required=False)
    sub_title_2 = forms.CharField(required=False)
    sub_credits_2 = forms.CharField(required=False)

    sub_abbr_3 = forms.CharField(required=False)
    sub_title_3 = forms.CharField(required=False)
    sub_credits_3 = forms.CharField(required=False)

    sub_abbr_4 = forms.CharField(required=False)
    sub_title_4 = forms.CharField(required=False)
    sub_credits_4 = forms.CharField(required=False)

    sub_abbr_5 = forms.CharField(required=False)
    sub_title_5 = forms.CharField(required=False)
    sub_credits_5 = forms.CharField(required=False)

    sub_abbr_6 = forms.CharField(required=False)
    sub_title_6 = forms.CharField(required=False)
    sub_credits_6 = forms.CharField(required=False)

    def group1(self):
        return [self[name] for name in filter(lambda x: x.endswith('_1'), self.fields)]

    def group2(self):
        return [self[name] for name in filter(lambda x: x.endswith('_2'), self.fields)]
    
    def group3(self):   
        return [self[name] for name in filter(lambda x: x.endswith('_3'), self.fields)]        
    
    def group4(self):   
        return [self[name] for name in filter(lambda x: x.endswith('_4'), self.fields)]        
    
    def group5(self):   
        return [self[name] for name in filter(lambda x: x.endswith('_5'), self.fields)]        
        
    def group6(self):   
        return [self[name] for name in filter(lambda x: x.endswith('_6'), self.fields)]   


    def clean_sub_abbr_1(self):
        field = self.cleaned_data['sub_abbr_1']
        try:
            Subject.objects.get(abbr__iexact=field)
        except:
            raise forms.ValidationError("Subject 1 does not exist.")
    
        return field

    def clean_sub_abbr_2(self):
        field = self.cleaned_data['sub_abbr_2']
        if field:
            try:
                Subject.objects.get(abbr__iexact=field)
            except:
                raise forms.ValidationError("Subject 2 does not exist.")
        return field

    def clean_sub_abbr_3(self):
        field = self.cleaned_data['sub_abbr_3']
        if field:
            try:
                Subject.objects.get(abbr__iexact=field)
            except:
                raise forms.ValidationError("Subject 3 does not exist.")
        return field

    def clean_sub_abbr_4(self):
        field = self.cleaned_data['sub_abbr_4']
        if field:
            try:
                Subject.objects.get(abbr__iexact=field)
            except:
                raise forms.ValidationError("Subject 4 does not exist.")
        return field

    def clean_sub_abbr_5(self):
        field = self.cleaned_data['sub_abbr_5']
        if field:
            try:
                Subject.objects.get(abbr__iexact=field)
            except:
                raise forms.ValidationError("Subject 5 does not exist.")
        return field

    def clean_sub_abbr_6(self):
        field = self.cleaned_data['sub_abbr_6']
        if field:
            try:
                Subject.objects.get(abbr__iexact=field)
            except:
                raise forms.ValidationError("Subject 2 does not exist.")
        return field

