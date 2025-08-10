from django.db import models

# Create your models here.
class crimeModel(models.Model):

    ccn = models.CharField(max_length=255)
    date = models.DateTimeField("date published",blank=True,null=True)
    update_date = models.DateTimeField("date published",blank=True,null=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    incident = models.CharField(max_length=255)
    incident_class = models.CharField(max_length=255)
    narrative = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.ccn},{self.date},{self.update_date},{self.city},{self.province},{self.postal_code},{self.address},{self.incident},{self.incident_class},{self.narrative},{self.longitude},{self.latitude}"