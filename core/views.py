from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import Patient, Doctor, Visit, Prescription
from .forms import PatientRegisterForm, DoctorRegisterForm, VisitForm, PrescriptionForm


def landing(request):
    return render(request, 'core/landing.html')


# ── PATIENT VIEWS ──────────────────────────────────────────────────────────────

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('patient_dashboard')
    else:
        form = PatientRegisterForm()
    return render(request, 'core/patient_register.html', {'form': form})


def patient_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'patient':
                login(request, user)
                return redirect('patient_dashboard')
            else:
                messages.error(request, 'This account is not a patient account.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/patient_login.html', {'form': form})


@login_required
def patient_dashboard(request):
    if request.user.role != 'patient':
        return redirect('landing')
    try:
        patient = request.user.patient_profile
        visits = patient.visits.prefetch_related('prescriptions', 'doctor__user').all()
    except Patient.DoesNotExist:
        messages.error(request, 'Patient profile not found.')
        return redirect('landing')
    return render(request, 'core/patient_dashboard.html', {'patient': patient, 'visits': visits})


# ── DOCTOR VIEWS ───────────────────────────────────────────────────────────────

def doctor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role == 'doctor':
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                messages.error(request, 'This account is not a doctor account.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/doctor_login.html', {'form': form})


def doctor_register(request):
    if request.method == 'POST':
        form = DoctorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegisterForm()
    return render(request, 'core/doctor_register.html', {'form': form})


@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return redirect('landing')
    doctor = request.user.doctor_profile
    return render(request, 'core/doctor_dashboard.html', {'doctor': doctor})


@login_required
def search_patient(request):
    if request.user.role != 'doctor':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    id_number = request.GET.get('id_number', '').strip()
    try:
        patient = Patient.objects.get(id_number=id_number)
        return JsonResponse({
            'found': True,
            'patient_id': patient.id,
            'name': patient.user.get_full_name(),
            'id_number': patient.id_number,
            'phone': patient.phone_number,
        })
    except Patient.DoesNotExist:
        return JsonResponse({'found': False})


@login_required
def simulate_access(request):
    """Simulates USSD consent — returns full patient data."""
    if request.user.role != 'doctor':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    patient_id = request.GET.get('patient_id')
    try:
        patient = Patient.objects.prefetch_related(
            'visits__prescriptions', 'visits__doctor__user'
        ).get(id=patient_id)
        visits_data = []
        for v in patient.visits.all():
            prescriptions = [
                {
                    'medication': p.medication_name,
                    'dosage': p.dosage,
                    'frequency': p.frequency,
                    'duration': p.duration,
                    'instructions': p.instructions,
                }
                for p in v.prescriptions.all()
            ]
            visits_data.append({
                'id': v.id,
                'date': v.date.strftime('%d %b %Y, %H:%M'),
                'doctor': f"Dr. {v.doctor.user.get_full_name()}",
                'chief_complaint': v.chief_complaint,
                'diagnosis': v.diagnosis,
                'notes': v.notes,
                'prescriptions': prescriptions,
            })
        return JsonResponse({
            'success': True,
            'patient': {
                'id': patient.id,
                'name': patient.user.get_full_name(),
                'id_number': patient.id_number,
                'dob': patient.date_of_birth.strftime('%d %b %Y') if patient.date_of_birth else 'N/A',
                'phone': patient.phone_number,
                'blood_type': patient.blood_type or 'Unknown',
                'allergies': patient.allergies or 'None recorded',
            },
            'visits': visits_data,
        })
    except Patient.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})


@login_required
@require_POST
def add_visit(request):
    if request.user.role != 'doctor':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    data = json.loads(request.body)
    patient_id = data.get('patient_id')
    try:
        patient = Patient.objects.get(id=patient_id)
        doctor = request.user.doctor_profile
        visit = Visit.objects.create(
            patient=patient,
            doctor=doctor,
            chief_complaint=data.get('chief_complaint', ''),
            diagnosis=data.get('diagnosis', ''),
            notes=data.get('notes', ''),
        )
        prescriptions = data.get('prescriptions', [])
        for p in prescriptions:
            if p.get('medication_name'):
                Prescription.objects.create(
                    visit=visit,
                    medication_name=p['medication_name'],
                    dosage=p.get('dosage', ''),
                    frequency=p.get('frequency', ''),
                    duration=p.get('duration', ''),
                    instructions=p.get('instructions', ''),
                )
        return JsonResponse({'success': True, 'visit_id': visit.id, 'date': visit.date.strftime('%d %b %Y, %H:%M')})
    except Patient.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient not found'})


def logout_view(request):
    logout(request)
    return redirect('landing')
