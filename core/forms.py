from django import forms
from .models import CustomerRecord
import re
IFSC_REGEX = re.compile(r"^[A-Za-z]{4}0[A-Za-z0-9]{6}$")
class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerRecord
        fields = ["applicant_no","name","ifsc","credit","debit","balance","city","branch"]
        widgets = {
            "applicant_no": forms.NumberInput(attrs={"class":"form-control form-control-lg","placeholder":"Applicant number"}),
            "name": forms.TextInput(attrs={"class":"form-control form-control-lg","placeholder":"Full name"}),
            "ifsc": forms.TextInput(attrs={"class":"form-control form-control-lg","placeholder":"IFSC e.g. HDFC0001234"}),
            "credit": forms.NumberInput(attrs={"step":"0.01","class":"form-control form-control-lg"}),
            "debit": forms.NumberInput(attrs={"step":"0.01","class":"form-control form-control-lg"}),
            "balance": forms.NumberInput(attrs={"step":"0.01","class":"form-control form-control-lg"}),
            "city": forms.TextInput(attrs={"class":"form-control form-control-lg"}),
            "branch": forms.NumberInput(attrs={"class":"form-control form-control-lg"}),
        }
    def clean_ifsc(self):
        # normalize: uppercase and remove surrounding whitespace
        raw = self.cleaned_data.get("ifsc", "")
        code = raw.upper().strip()
        # be tolerant of accidental punctuation (e.g. trailing dot or spaces) by removing non-alphanumerics
        code = re.sub(r"[^A-Za-z0-9]", "", code)
        # IFSC format is 4 letters, then a 0, then 6 alphanumeric characters (total length 11)
        if not IFSC_REGEX.match(code):
            # give a more helpful error message including an example
            raise forms.ValidationError("Invalid IFSC code format. Expected 11 characters: 4 letters, '0', then 6 alphanumerics (e.g. HDFC0001234).")
        return code
class CustomerUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomerRecord
        fields = ["name","city","branch"]
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control form-control-lg"}),
            "city": forms.TextInput(attrs={"class":"form-control form-control-lg"}),
            "branch": forms.NumberInput(attrs={"class":"form-control form-control-lg"}),
        }
