from django.http import HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.template.response import TemplateResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Q
from django.middleware import csrf
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.template.loader import render_to_string
from .forms import UserRegisterForm
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Appointment, Profile
from django.shortcuts import render
from django.http import JsonResponse

from .forms import AppointmentForm
from django.shortcuts import render, get_object_or_404
import imaplib
import email
from django.views.decorators.csrf import csrf_exempt
from email.header import decode_header
from django.views.decorators.csrf import csrf_exempt
from .serializers import HeartRateSerializer
import os
import webbrowser
from receipt_parser import RuleBased
import pandas as pd
import re
from .models import Message
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user)
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'users/appointments/view.html', {'appointments': appointments})


@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('view_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'users/appointments/create.html', {'form': form})


@login_required
def doctor_appointments(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'users/appointments/doctor_appointments.html', {'appointments': appointments})


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)


def obtain_header(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding)
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode(encoding)
    return subject, From


def download_attachment(part):
    filename = part.get_filename()
    if filename:
        folder_name = clean(subject)
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        filepath = os.path.join(folder_name, filename)
        open(filepath, "wb").write(part.get_payload(decode=True))


def extract_purchase_history():
    imap = imaplib.IMAP4_SSL("imap.mail.ru")
    imap.login("ivankov2001@bk.ru", "Nz2cNLSLUb3UhKf6eQvb")
    status, messages = imap.select("INBOX")
    numOfMessages = int(messages[0])
    history = []

    for i in range(numOfMessages, numOfMessages - 10, -1):
        res, msg = imap.fetch(str(i), "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                name, address = email.utils.parseaddr(msg['From'])
                if (address.find("ivankov2001@gmail.com") != -1):
                    subject, From = obtain_header(msg)

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            try:
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                start_idx = body.find("приход") + len("приход")
                                end_idx = body.rfind("Итог", start_idx)
                                pattern = re.compile(r'(\d+)\s+(.+?)\s+Цена\*Кол\s+(\d+\.\d+)')
                                products = []
                                for match in pattern.finditer(body[start_idx:end_idx].strip()):
                                    id = match.group(1)
                                    name = match.group(2)
                                    price = float(match.group(3))
                                    product = {'id': id, 'name': name, 'price': price}
                                    products.append(product)
                                history.extend(products)
                            elif "attachment" in content_disposition:
                                download_attachment(part)
                    else:
                        content_type = msg.get_content_type()
                        body = msg.get_payload(decode=True).decode()
                        if content_type == "text/plain":
                            start_idx = body.find("приход") + len("приход")
                            end_idx = body.rfind("Наличные", start_idx)
                            product = {'id': '1', 'name': 'ДОБР.Нап.КОЛА б/алк.ПЭТ 1.5л', 'price': 100.0}
                            history.append(product)
    imap.close()
    return history


def purchase_history(request):
    history = extract_purchase_history()
    return render(request, 'users/purchase_history.html', {'history': history})


def user_list(request):
    doctors = User.objects.filter(groups__name='Мед.персонал')
    return render(request, 'users/user_list.html', {'doctors': doctors})


@login_required
def message_send(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            message = Message.objects.create(sender=request.user, recipient=recipient, text=message_text)
            if request.user.groups.filter(name='Пациент').exists():
                return redirect('message_view_patient')
            elif request.user.groups.filter(name='Мед.персонал').exists():
                return redirect('message_view_doctor')
    return HttpResponse('Что-то пошло не так.')


def message_view(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    messages = Message.objects.filter(sender=request.user, recipient=recipient) | Message.objects.filter(
        sender=recipient, recipient=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'users/message_view.html', {'messages': messages, 'recipient': recipient})


def message_view_doctor(request):
    if request.user.groups.filter(name='Мед.персонал').exists():
        all_patients = User.objects.filter(groups__name='Пациент')

        if request.method == 'POST':
            patient_id = request.POST.get('patient')
            patient = get_object_or_404(User, pk=patient_id)
            message_text = request.POST.get('message')
            if message_text:
                message = Message.objects.create(sender=request.user, recipient=patient, text=message_text)
                return redirect('message_view_doctor')

        chats = []
        for patient in all_patients:
            messages = Message.objects.filter(Q(sender=request.user, recipient=patient) | Q(sender=patient, recipient=request.user)).order_by('-timestamp')
            if messages:
                chat = {
                    'patient': patient,
                    'messages': messages
                }
                chats.append(chat)

        return render(request, 'users/message_view_doctor.html', {'chats': chats, 'all_patients': all_patients})
    else:
        return HttpResponse('У вас нет доступа к этой странице.')

@login_required
def chat_delete_patient(request, doctor_id):
    doctor = get_object_or_404(User, pk=doctor_id)

    # Получаем все сообщения между пациентом и врачом
    messages = Message.objects.filter(sender=request.user, recipient=doctor) | \
               Message.objects.filter(sender=doctor, recipient=request.user)

    if messages.exists():
        messages.delete()
        return redirect('message_view_patient')
    else:
        return HttpResponse('У вас нет доступа к удалению этого чата.')
@login_required
def chat_delete(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)

    # Получаем все сообщения между отправителем и получателем
    messages = Message.objects.filter(sender=request.user, recipient=recipient) | \
               Message.objects.filter(sender=recipient, recipient=request.user)

    if messages.exists():
        messages.delete()
        return redirect('message_view_doctor')
    else:
        return HttpResponse('У вас нет доступа к удалению этого чата.')

def message_view_patient(request):
    if request.user.groups.filter(name='Пациент').exists():
        all_doctors = User.objects.filter(groups__name='Мед.персонал')

        if request.method == 'POST':
            doctor_id = request.POST.get('doctor')
            doctor = get_object_or_404(User, pk=doctor_id)
            message_text = request.POST.get('message')
            if message_text:
                message = Message.objects.create(sender=request.user, recipient=doctor, text=message_text)
                return redirect('message_view_patient')

        chats = []
        for doctor in all_doctors:
            messages = Message.objects.filter(Q(sender=request.user, recipient=doctor) | Q(sender=doctor, recipient=request.user)).order_by('-timestamp')
            if messages:
                chat = {
                    'doctor': doctor,
                    'messages': messages
                }
                chats.append(chat)

        return render(request, 'users/message_view_patient.html', {'chats': chats, 'all_doctors': all_doctors})
    else:
        return HttpResponse('У вас нет доступа к этой странице.')


logger = logging.getLogger(__name__)


def get_csrf_token(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        return HttpResponse(csrf_token)


class HeartRateView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username='matveyss')
        profile = Profile.objects.get(user=user)
        heart_rate = profile.heart_rate
        return JsonResponse({'heart_rate': heart_rate})

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            heart_rate = int(data.get('heart_rate'))

            user = get_object_or_404(User, username='matveyss')
            profile = get_object_or_404(Profile, user=user)
            profile.heart_rate = heart_rate
            profile.save()

            return HttpResponse('Success')

        except Exception as e:
            response_data = {'status': 'error', 'error_message': str(e)}
            return JsonResponse(response_data)

    def get_heart_rate(self, request):
        user = get_object_or_404(User, username='matveyss')
        profile = get_object_or_404(Profile, user=user)
        return JsonResponse({'heart_rate': profile.heart_rate})



