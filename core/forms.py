from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Patient, Doctor, Visit, Prescription


class PatientRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    id_number = forms.CharField(max_length=20, label="National ID Number")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    blood_type = forms.ChoiceField(
        choices=[('', '--'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
                 ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')],
        required=False
    )
    allergies = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'patient'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Patient.objects.create(
                user=user,
                id_number=self.cleaned_data['id_number'],
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                phone_number=self.cleaned_data.get('phone_number', ''),
                blood_type=self.cleaned_data.get('blood_type', ''),
                allergies=self.cleaned_data.get('allergies', ''),
            )
        return user


class DoctorRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    license_number = forms.CharField(max_length=30, label="Medical License Number")
    specialization = forms.CharField(max_length=100, required=False)
    hospital = forms.CharField(max_length=100, required=False, label="Hospital / Clinic")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'doctor'
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Doctor.objects.create(
                user=user,
                license_number=self.cleaned_data['license_number'],
                specialization=self.cleaned_data.get('specialization', ''),
                hospital=self.cleaned_data.get('hospital', ''),
            )
        return user


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['chief_complaint', 'diagnosis', 'notes']
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 3, 'placeholder': "Patient's presenting complaint..."}),
            'diagnosis': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Clinical diagnosis...'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes, referrals, follow-up instructions...'}),
        }


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g. Take with food'}),
            'medication_name': forms.TextInput(attrs={'placeholder': 'e.g. Amoxicillin'}),
            'dosage': forms.TextInput(attrs={'placeholder': 'e.g. 500mg'}),
            'frequency': forms.TextInput(attrs={'placeholder': 'e.g. Twice daily'}),
            'duration': forms.TextInput(attrs={'placeholder': 'e.g. 7 days'}),
        }
