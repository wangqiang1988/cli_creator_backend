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

class foodlist(models.Model):  
    userid = models.TextField(max_length=30)
    name = models.TextField(max_length=30)
    des = models.TextField()
    history = models.TextField()
    make = models.TextField()
    tips = models.TextField()
    time = models.DateTimeField(max_length=30)
    def __str__(self):
        return '%s %s %s'%( self.userid, self.name, self.des, self.history, self.make, self.tips, self.time)
    class Meta:
        app_label = 'firewall'