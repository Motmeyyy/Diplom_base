# import hashlib
#
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User, Group
# from .forms import UserRegisterForm
# from .forms import UserUpdateForm, ProfileUpdateForm
# from .models import Appointment, PurchaseHistory
# from .forms import AppointmentForm
# from django.shortcuts import render
# import imaplib
# import email
# from email.header import decode_header
# import os
# import webbrowser
# from receipt_parser import RuleBased
# import pandas as pd
# import re
#
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#
#             user = form.save()
#             group = form.cleaned_data['group']
#             group.user_set.add(user)
#             login(request, user)
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Ваш аккаунт создан: можно войти на сайт.')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form': form})
#
#
#
#
# @login_required
# def profile(request):
#     return render(request, 'users/profile.html')
#
# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('profile')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=request.user.profile)
#     return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
#
# @login_required
# def view_appointments(request):
#     appointments = Appointment.objects.filter(patient=request.user)
#     return render(request, 'users/appointments/view.html', {'appointments': appointments})
#
# @login_required
# def create_appointment(request):
#     if request.method == 'POST':
#         form = AppointmentForm(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.patient = request.user
#             appointment.save()
#             return redirect('view_appointments')
#     else:
#         form = AppointmentForm()
#     return render(request, 'users/appointments/create.html', {'form': form})
#
# @login_required
# def doctor_appointments(request):
#     appointments = Appointment.objects.filter(doctor=request.user)
#     return render(request, 'users/appointments/doctor_appointments.html', {'appointments': appointments})
#
# def clean(text):
#     return "".join(c if c.isalnum() else "_" for c in text)
#
# def obtain_header(msg):
#     subject, encoding = decode_header(msg["Subject"])[0]
#     if isinstance(subject, bytes):
#         subject = subject.decode('utf-8')
#     From, encoding = decode_header(msg.get("From"))[0]
#     if isinstance(From, bytes):
#         From = From.decode('utf-8')
#     return subject, From
#
# # def download_attachment(part):
# #     filename = part.get_filename()
# #     if filename:
# #         folder_name = clean(subject)
# #         if not os.path.isdir(folder_name):
# #             os.mkdir(folder_name)
# #         filepath = os.path.join(folder_name, filename)
# #         open(filepath, "wb").write(part.get_payload(decode=True))
#
# def extract_purchase_history():
#     imap = imaplib.IMAP4_SSL("imap.mail.ru")
#     imap.login("ivankov2001@bk.ru", "Nz2cNLSLUb3UhKf6eQvb")
#     status, messages = imap.select("INBOX")
#     numOfMessages = int(messages[0])
#     history = []
#
#     for i in range(numOfMessages, numOfMessages - 10, -1):
#         res, msg = imap.fetch(str(i), "(RFC822)")
#
#         for response in msg:
#             if isinstance(response, tuple):
#                 msg = email.message_from_bytes(response[1])
#                 name, address = email.utils.parseaddr(msg['From'])
#                 if(address.find("ivankov2001@gmail.com") != -1):
#                     subject, From = obtain_header(msg)
#
#                     if msg.is_multipart():
#                         for part in msg.walk():
#                             content_type = part.get_content_type()
#                             content_disposition = str(part.get("Content-Disposition"))
#
#                             try:
#                                 body = part.get_payload(decode=True).decode()
#                             except:
#                                 pass
#
#                             if content_type == "text/plain" and "attachment" not in content_disposition:
#                                 start_idx = body.find("приход") + len("приход")
#                                 end_idx = body.rfind("Итог", start_idx)
#                                 pattern = re.compile(r'(\d+)\s+(.*?)\s+Цена\*Кол\s+(\d+\.\d+)')
#                                 products = []
#
#                                 for match in pattern.finditer(body[start_idx:end_idx].strip()):
#                                     id = match.group(1)
#                                     name = match.group(2)
#                                     price = float(match.group(3))
#                                     product = {'id': id, 'name': name, 'price': price}
#                                     products.append(product)
#                                 df = pd.DataFrame(columns=['name'])
#
#                                 for product in products:
#                                     new_row = {'name': [product['name']]}
#                                     new_rows_df = pd.DataFrame(new_row)
#                                     df = pd.concat([df, new_rows_df], ignore_index=True)
#                                 rb = RuleBased()
#
#                                 history.append(rb.parse(df))
#
#                                 print(history)
#
#
#     imap.close()
#     return history
#
#
#
# def save_purchase_history(user, items):
#     for item in items:
#         receipt_hash = hashlib.md5(str(item).encode()).hexdigest()  # Вычисляем хэш чека
#         # Проверяем, существует ли чек с таким хэшем в базе данных
#         if not PurchaseHistory.objects.filter(receipt_hash=receipt_hash).exists():
#             purchase = PurchaseHistory(user=user, item=item, receipt_hash=receipt_hash)
#             purchase.save()
#
#
# def purchase_history(request):
#     # Ваш код для получения истории покупок
#     history = extract_purchase_history()
#
#     # Сохранение истории покупок в базе данных
#     save_purchase_history(request.user, history)
#
#     # Создаем пустой список для обработанных данных
#     processed_history = []
#
#     for i, item in enumerate(history):
#         processed_item = {
#             'id': i + 1,  # Используем индекс элемента для получения позиции в списке
#             'name': item['name'] if 'name' in item else '',
#             'product_norm': item['product_norm'] if 'product_norm' in item else '',
#             'brand_norm': item['brand_norm'] if 'brand_norm' in item else '',
#             'cat_norm': item['cat_norm'] if 'cat_norm' in item else ''
#         }
#         processed_history.append(processed_item)
#
#     return render(request, 'users/purchase_history.html', {'history': processed_history})
#
# def create_diet(request):
#     if request.method == 'POST':
#         form = DietForm(request.POST)
#         if form.is_valid():
#             diet = form.save()
#             return redirect('doctor_profile')  # Перенаправьте пользователя после создания диеты
#     else:
#         form = DietForm()
#     return render(request, 'create_diet.html', {'form': form})

import hashlib
import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AppointmentForm, DietForm
from .models import Appointment, PurchaseHistory, Diet
import imaplib
import email
from email.header import decode_header
import os
import webbrowser
from receipt_parser import RuleBased
import pandas as pd

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
        subject = subject.decode('utf-8')
    From, encoding = decode_header(msg.get("From"))[0]
    if isinstance(From, bytes):
        From = From.decode('utf-8')
    return subject, From

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
                if(address.find("ivankov2001@gmail.com") != -1):
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
                                pattern = re.compile(r'(\d+)\s+(.*?)\s+Цена\*Кол\s+(\d+\.\d+)')
                                products = []

                                for match in pattern.finditer(body[start_idx:end_idx].strip()):
                                    id = match.group(1)
                                    name = match.group(2)
                                    price = float(match.group(3))
                                    product = {'id': id, 'name': name, 'price': price}
                                    products.append(product)
                                df = pd.DataFrame(columns=['name'])

                                for product in products:
                                    new_row = {'name': [product['name']]}
                                    new_rows_df = pd.DataFrame(new_row)
                                    df = pd.concat([df, new_rows_df], ignore_index=True)
                                rb = RuleBased()

                                history.append(rb.parse(df))

                                print(history)

    imap.close()
    return history

def save_purchase_history(user, items):
    for item in items:
        receipt_hash = hashlib.md5(str(item).encode()).hexdigest()  # Вычисляем хэш чека
        # Проверяем, существует ли чек с таким хэшем в базе данных
        if not PurchaseHistory.objects.filter(receipt_hash=receipt_hash).exists():
            purchase = PurchaseHistory(user=user, item=item, receipt_hash=receipt_hash)
            purchase.save()

@login_required
def purchase_history(request):
    # Ваш код для получения истории покупок
    history = extract_purchase_history()

    # Сохранение истории покупок в базе данных
    save_purchase_history(request.user, history)

    # Создаем пустой список для обработанных данных
    processed_history = []

    for i, item in enumerate(history):
        processed_item = {
            'id': i + 1,  # Используем индекс элемента для получения позиции в списке
            'name': item['name'] if 'name' in item else '',
            'product_norm': item['product_norm'] if 'product_norm' in item else '',
            'brand_norm': item['brand_norm'] if 'brand_norm' in item else '',
            'cat_norm': item['cat_norm'] if 'cat_norm' in item else ''
        }
        processed_history.append(processed_item)

    return render(request, 'users/purchase_history.html', {'history': processed_history})

@login_required
def create_diet(request):
    diets = Diet.objects.all()
    if request.method == 'POST':
        form = DietForm(request.POST)
        if form.is_valid():
            diet = form.save()
            return redirect('diet_list')
    else:
        form = DietForm()
    return render(request, 'users/create_diet.html', {'form': form, 'diets': diets})

@login_required
def choose_diet(request, diet_id):
    diet = get_object_or_404(Diet, id=diet_id)
    recipes = diet.recipes.all()
    return render(request, 'users/choose_diet.html', {'diet': diet, 'recipes': recipes})

def diet_list(request):
    diets = Diet.objects.all()
    return render(request, 'users/diet_list.html', {'diets': diets})

def diet_detail(request, diet_id):
    diet = Diet.objects.get(id=diet_id)
    return render(request, 'users/diet_detail.html', {'diet': diet})