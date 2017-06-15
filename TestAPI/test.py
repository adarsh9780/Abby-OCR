

#complete path of image, in this case image is in same directory, so only name is used
path = 'a.jpg'


#instance of AbbyyOnlineSdk
a = AbbyyOnlineSdk()

#returns an object with valuable info
task = a.ProcessImage(path, Settings)

task_status = a.GetTaskStatus(task)

print(task_status.Status)

#change the url instance of task by the url which is returned by task
task.DownloadUrl = task_status.DownloadUrl

#path where output is to be stored
output = "a"

#download the result, using url returned by task
a.DownloadResult(task, output)
