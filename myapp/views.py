from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from Resumex import settings
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail

import os
import shutil
from zipfile import ZipFile

from Resumex import test

import json

#for pdf to text conversion
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

import csv
import re
import spacy


import nltk


def home(request):
    if request.method == 'POST' and 'register' in request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/logged_home/')
    elif request.method == 'POST' and 'signin' in request.POST:
        context = {}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('/logged_home/')
        else:
            context["error"] = "provide valid credentials"
            return render(request, 'index.html', context)

    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})


def contact(request):
    if request.method == 'POST' and 'register' in request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/logged_home/')
    elif request.method == 'POST' and 'signin' in request.POST:
        context = {}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('/logged_home/')
    elif request.method == 'POST' and 'email' in request.POST:
        first_name = request.POST['first_name']
        to_email_id = [request.POST['emailid']]
        message = request.POST['message']
        from_mail = settings.EMAIL_HOST_USER
        site_admin = ['rakshith.sathish@gmail.com']
        # Mail to admin about new enquiry
        send_mail("New enquiry", message, from_mail, site_admin, fail_silently=False)

        # Mail to customer
        reply = "We got your enquiry.We will get back to you soon.Please don't reply to this mail.This is " \
                "a system generated email.Thank you!"
        send_mail("Regarding your equiry", reply, from_mail, to_email_id, fail_silently=False)
        return render(request, 'contact.html')
    else:
        form = UserCreationForm()
    return render(request, 'contact.html', {'form': form})


def about(request):
    if request.method == 'POST' and 'register' in request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/logged_home/')
    elif request.method == 'POST' and 'signin' in request.POST:
        context = {}
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return redirect('/logged_home/')
        else:
            context["error"] = "provide valid credentials"
            return render(request, 'about.html', context)

    else:
        form = UserCreationForm()
    return render(request, 'about.html', {'form': form})


@login_required
def logged_home(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('/home')


    elif request.method == 'POST' and 'upload' in request.POST:
        try:
            uploaded_file = request.FILES['document']
        except MultiValueDictKeyError:
            context = {}
            context['error'] = "Please Choose a file"
            return render(request, 'loged_home.html', context)
        if uploaded_file:
            filename = uploaded_file.name
            if re.match(r'^.*\.pdf$', filename):  # if the uploaded file is pdf
                context = {}
                fs = FileSystemStorage()
                fs.save(uploaded_file.name, uploaded_file)
                with open('techskill.csv', 'r') as f:
                    reader = csv.reader(f)
                    your_list = list(reader)
                with open('nontechnicalskills.csv', 'r') as f:
                    reader = csv.reader(f)
                    your_list1 = list(reader)
                filename = "media/" + str(filename)
                makeitastring =convert(filename)
                resume_string1 = makeitastring
                post = test.predict(makeitastring)
                makeitastring = makeitastring.replace(',', ' ')
                makeitastring = makeitastring.lower()
                s = set(your_list[0])
                s1 = set(your_list1[0])

                def technical_skills():
                    skills = []
                    for word in makeitastring.split(" "):
                        if word in s:
                            skills.append(word)
                    return list(set(skills))

                def non_techlskills():
                    nontechskills = []
                    for word in makeitastring.split(" "):
                        if word in s1:
                            nontechskills.append(word)
                    return list(set(nontechskills))

                print(extract_name(resume_string1))

                print(extract_phone_numbers(makeitastring))

                print(extract_email_addresses(makeitastring))

                print(technical_skills())
                print(non_techlskills())

                position = post[0]
                context['flag2'] = '1'
                context['position'] = 'The resumes belongs to ' + str(position)
                os.remove(filename)
                return render(request, 'loged_home.html', context)
            elif re.match(r'^.*\.zip$', filename):
                context = {}
                posts = []
                crtdict={}
                mylist=[['Task', 'Hours per Day']]
                os.mkdir('download_folder')
                fs = FileSystemStorage()
                fs.save(filename, uploaded_file)
                filename = str(filename)
                with ZipFile(("media/" + filename), 'r') as zip:
                    # extracting all the files
                    print('Extracting all the files now...')
                    zip.extractall()
                    print('Done!')
                new_name = re.sub(r'.zip$', "", filename)
                for files in os.listdir(new_name):
                    filename = os.fsdecode(files)
                    if filename.endswith(".pdf"):
                        makeitastring =convert(new_name + '/' + filename)
                        post = test.predict(makeitastring)
                        post = post[0]
                        if post in posts:
                            shutil.copy((new_name + '/' + filename), ("download_folder/" + str(post)))
                            crtdict[post]=crtdict[post]+1
                        else:
                            os.mkdir("download_folder/" + str(post))
                            shutil.copy((new_name + '/' + filename), ("download_folder/" + str(post)))
                            posts.append(post)
                            crtdict[post]=1
                    else:
                        continue

                for keys in crtdict:
                    mylist.append([keys, crtdict[keys]])

                json_list=json.dumps(mylist)
                context['chart']=json_list
                print("folder upload worked")
                shutil.rmtree(new_name)
                os.remove("media/" + str(uploaded_file.name))
                shutil.make_archive('folder', 'zip', 'download_folder')
                print("archieve created")
                shutil.rmtree('download_folder')
                print("delete successful")
                try:
                    exists = open('media/folder.zip', 'rb')
                    exists.close()
                    os.remove("media/folder.zip")
                except FileNotFoundError:
                    print("folder does't exists")
                shutil.move('folder.zip', 'media')
                link = fs.url('folder.zip')
                context['url'] = link
                context['download'] = 'Click here to download your classified resumes'
                context['flag1'] = '1'
                return render(request, 'loged_home.html', context)
            else:
                context = {}
                context['warning'] = "Please select a file in valid format"
                return render(request, 'loged_home.html', context)
    else:
        context = {}
        context['warning'] = 'Upload your file here'
        return render(request, 'loged_home.html', context)

@login_required
def logged_about(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('/home')
    else:
        return render(request, 'loged_about.html')


def logged_contact(request):
    if request.method == 'POST' and 'logout' in request.POST:
        logout(request)
        return redirect('/home')
    elif request.method=='POST' and 'email' in request.POST:
        first_name=request.POST['first_name']
        to_email_id=[request.POST['emailid']]
        message=request.POST['message']
        from_mail=settings.EMAIL_HOST_USER
        site_admin=['rakshith.sathish@gmail.com']

        #Mail to admin about new enquiry
        send_mail("New enquiry",message,from_mail,site_admin,fail_silently=False)

        #Mail to customer
        reply="We got your enquiry.We will get back to you soon.Please don't reply to this mail.This is " \
              "a system generated email.Thank you!"
        send_mail("Regarding your equiry",reply,from_mail,to_email_id,fail_silently=False)
        return render(request,'loged_contact.html')
    else:
        return render(request, 'loged_contact.html')



import nltk



def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text

def extract_name(string):
    r1 = str(string)
    nlp = spacy.load('xx')
    doc = nlp(r1)
    for ent in doc.ents:
        if(ent.label_ == 'PER'):
            return (ent.text)


def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return list(set([re.sub(r'\D', '', number) for number in phone_numbers]))

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return list(set(r.findall(string)))

