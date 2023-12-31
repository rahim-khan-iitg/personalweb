from django.db import models

# Create your models here
class link_db(models.Model):
    link=models.CharField(max_length=1000)
    link_id=models.CharField(max_length=6)
    
    def __str__(self):
        return "link"+self.link_id