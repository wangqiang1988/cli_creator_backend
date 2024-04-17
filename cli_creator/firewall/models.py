from django.db import models

# Create your models here.

class cli_logs(models.Model):  
    ip_address = models.TextField(max_length=30)
    time = models.DateTimeField(max_length=30)
    info = models.TextField(max_length=255)
    def __str__(self):
        return '%s %s %s'%( self.ip_address, self.time, self.info)
    class Meta:
        app_label = 'firewall'