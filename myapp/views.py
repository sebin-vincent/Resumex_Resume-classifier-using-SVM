from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
import re
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
import PyPDF2
import os
import shutil
from zipfile import ZipFile
import glob

from Resumex import test


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
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


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
                filename = "media/" + str(filename)
                newfile = open('res.txt', 'w')
                file = open(filename, 'rb')
                pdfreader = PyPDF2.PdfFileReader(file)
                # print(pdfreader.getNumPages())
                pageobj = pdfreader.getPage(0)
                newfile.write(pageobj.extractText())
                file.close()
                newfile.close()
                text_file = open('res.txt', 'r')
                resume = text_file.readlines()
                makeitastring = ''.join(map(str, resume))
                post = test.predict(makeitastring)
                position = post[0]
                context['position'] = 'The resumes belongs to ' + str(position)
                os.remove(filename)
                return render(request, 'loged_home.html', context)
            elif re.match(r'^.*\.zip$', filename):
                context = {}
                posts = []
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
                        newfile = open('res.txt', 'w')
                        file = open((new_name + '/' + filename), 'rb')
                        pdfreader = PyPDF2.PdfFileReader(file)
                        # print(pdfreader.getNumPages())
                        pageobj = pdfreader.getPage(0)
                        newfile.write(pageobj.extractText())
                        file.close()
                        newfile.close()
                        text_file = open('res.txt', 'r')
                        resume = text_file.readlines()
                        makeitastring = ''.join(map(str, resume))
                        post = test.predict(makeitastring)
                        if post in posts:
                            shutil.copy((new_name + '/' + filename), ("download_folder/" + str(post)))
                        else:
                            os.mkdir("download_folder/" + str(post))
                            shutil.copy((new_name + '/' + filename), ("download_folder/" + str(post)))
                            posts.append(post)
                    else:
                        continue
                print("folder upload worked")
                shutil.rmtree('resumes')
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
                return render(request, 'loged_home.html', context)
    else:
        context = {}
        context['warning'] = 'Upload your file here'
        return render(request, 'loged_home.html', context)


@login_required
def logged_about(request):
    return render(request, 'loged_about.html')


def logged_contact(request):
    return render(request, 'loged_contact.html')


from django.shortcuts import render

# Create your views here.
