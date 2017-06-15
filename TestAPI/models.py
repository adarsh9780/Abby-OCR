from django.db import models

class ImageModel(models.Model):

	imageName = models.CharField(max_length = 20)
	image = models.ImageField(null = False, blank= False)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.imageName