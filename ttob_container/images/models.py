from django.db import models

# Create your models here.
class MyFile(models.Model):
    file = models.FileField(blank=False, null=False)
    projectName = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} ({})'.format(self.projectName, self.file)