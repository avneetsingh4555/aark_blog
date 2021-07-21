from django.db import models

# Create your models here.
class Blog_info(models.Model):
    bi_id = models.AutoField(primary_key=True)
    bi_title = models.CharField(max_length=255)
    bi_subtitle = models.CharField(max_length=255)
    bi_description = models.CharField(max_length=255)
    bi_image = models.ImageField()
    bi_event_date = models.DateTimeField('Event Date',blank=True)
    bi_creator_name = models.CharField(max_length=255)
    class Meta:
        db_table = 'Blog_info'

class Assign_project_info(models.Model):
    ap_id = models.AutoField(primary_key=True)
    ap_title = models.CharField(max_length=255)
    ap_languages = models.CharField(max_length=255)
    ap_developers = models.CharField(max_length=255)
    ap_sub_time =models.DateTimeField('Event Date',blank=True)
    class Meta:
        db_table = 'Assign_project_info'
    
class User_info(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_phno = models.CharField(max_length=255)
    user_skills = models.CharField(max_length=255)
    class Meta:
        db_table = 'User_info'
    