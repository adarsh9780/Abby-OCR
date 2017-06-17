from django.shortcuts import render
from .models import ImageModel
from .forms import ImageForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from AbbyyOnlineSdk import AbbyyOnlineSdk
from time import sleep
import os
import re

#Necessary for uploading the image from user to server
class Upload(View):

#if it is get request(user is coming first time to upload image )
    def get(self, request, *args, **kwargs):
        #select the form to be displayed
        form = ImageForm()
# and pass it to html page usng dictionary
        context = {
            'form' : form,
        }
        return render(request, 'TestAPI/upload.html', context)

# after uploading image return to same page again
    def post(self, request, *args, **kwargs):
        #some times usern won't be submitting anything to us via post request
        # in that case don't capture any thing & just return to same page.
        form = ImageForm(request.POST or None, request.FILES or None)
        # if user submits, verify the data, using inbuilt Django method,
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return HttpResponseRedirect('/upload/')

        context = {
        'form' : form,
        }
        return render(request, 'TestAPI/upload.html', context)

# settings required for ABBYY
class Settings:
  Language = "English"
  OutputFormat = "txt"

#when user clicks on "SHOW RESULT" send the uplloaded image to the server of abbyy
class ViewText(View):
    
    #using get method, capture the downloaded result
    def get(self, request, *args, **kwargs):

# capture the latest image uploaded by user
        model = ImageModel.objects.all().order_by('-timestamp')[0]
# location of image
        path = os.path.join(settings.MEDIA_ROOT, model.image.name )
        #instance abbyy class
        a = AbbyyOnlineSdk()
        #returns an object with valuable info
        task = a.ProcessImage(path, Settings)

#check for the status from abbyy server
        task_status = a.GetTaskStatus(task)
# if it is not completed, repeat the preocess again in the interval of 2 secs.
        while(task_status.Status != 'Completed'):
          task_status = a.GetTaskStatus(task)
          sleep(2)

        #change the url instance of task by the url which is returned by task
        task.DownloadUrl = task_status.DownloadUrl

        #path where output is to be stored
        output = 'Result'

        #download the result, using url returned by task
        a.DownloadResult(task, output)

        #open the file
        file_to_open = open(os.path.join(settings.BASE_DIR, output), 'r')
        text = file_to_open.read()

        phone = r'\d{2}-\d{3}-\d{5}|\d{10}|\+\d{2}-\d{2}-\d{3}-\d{5}|\+\d{2}-\d{5}-\d{5}'
        email = r'[a-zA-Z0-9]\S*@\S*[a-zA-Z]'
        name = r'[a-zA-Z]{1,20}'

        phn = re.findall(phone, text)
        em = re.findall(email, text)
        nm = re.findall(name, text)
        
        context = {
        'text':text,
        'phn':phn[0],
        # 'em':em[0],
        'firstName':nm[0],
        'lastName':nm[1],
        }

        file_to_open.close()
        return render(request, 'TestAPI/view.html', context)
