from django.shortcuts import render
from .models import ImageModel
from .forms import ImageForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views import View
from AbbyyOnlineSdk import AbbyyOnlineSdk
from time import sleep
import os

class Upload(View):

    def get(self, request, *args, **kwargs):
        form = ImageForm()

        context = {
            'form' : form,
            # 'CSS' : CSS,
        }
        # print("Success")
        return render(request, 'TestAPI/upload.html', context)

    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.save()
            return HttpResponseRedirect('/upload/')
        
        # CSS = os.path.join(settings.BASE_DIR, 
        #     'TestAPI', 'templates', 'TestAPI', 'css', 'bootstrap.min.css')
        
        # JSS = os.path.join(settings.BASE_DIR, 
        #     'TestAPI', 'templates', 'TestAPI', 'css', "bootstrap.min.js")

        context = {
        'form' : form,
        # 'CSS' : CSS,
        }
        return render(request, 'TestAPI/upload.html', context)


class Settings:
  Language = "English"
  OutputFormat = "txt"

class ViewText(View):
    
    def get(self, request, *args, **kwargs):

        model = ImageModel.objects.all().order_by('-timestamp')[0]
        path = os.path.join(settings.MEDIA_ROOT, model.image.name )
        a = AbbyyOnlineSdk()
        #returns an object with valuable info
        task = a.ProcessImage(path, Settings)

        task_status = a.GetTaskStatus(task)
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
        
        # CSS = os.path.join(settings.BASE_DIR, 
        #     'TestAPI', 'templates', 'TestAPI', 'css', 'bootstrap.min.css')

        # JSS = os.path.join(settings.BASE_DIR, 
        #     'TestAPI', 'templates', 'TestAPI', 'css', "bootstrap.min.js")

        context = {
        'text':text,
        # 'CSS':CSS,
        }

        file_to_open.close()
        return render(request, 'TestAPI/view.html', context)
