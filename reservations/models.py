"""Models.py"""
from django.db import models
from django.urls import reverse

# Profile
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Validating Reservations
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.


class Organization(models.Model):
    name=models.CharField(max_length=200, null=False, verbose_name="Organization")
    
    def __str__(self):
        return self.name
        
        
'''Schools Model
'''
class School(models.Model):
    name = models.CharField(max_length = 200, null=False)
    organzation = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

'''Resources Model
@PreviouslyKnownAs: Room
'''
class Resource(models.Model):
    name = models.CharField(max_length = 200, null=False, verbose_name="Resource Name")
    description = models.TextField(max_length=500, blank=True, null=True)
    school = models.ForeignKey(School, on_delete = models.SET_NULL, null=True)
    enabled = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name}, {self.school}"


'''Blocks Model 
This model defines the blocks for a school.
Schools can create their own block schedules and 
reserve resources based on their own schedule.
'''
class TimeBlock(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name="Block Name")
    sequence = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False)
    enabled = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    deleted_on = models.DateField(null=True, blank=True)
    
    class Meta:
       ordering = ['sequence', 'name', ]
       
    def __str__(self):
        return f"{self.name}, {self.school}, sequence: {self.sequence}"
        

'''Profile Model
'''
class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    location = models.ForeignKey(School, on_delete = models.SET_NULL, null=True, blank=True)
    organzation = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)

    school_admin = models.BooleanField(default=False)
    
    # Necessary for user signup
    email_confirmed = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        """
        Returns the url to access a model instance.
        """
        return reverse('app_user_update', args=[str(self.id)])
    
    def __str__(self):
        return '%s (profile)' % self.user
        
'''Creates user profile on first login
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
'''Save user profile function
'''
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Reservation(models.Model):
    '''Defines a reservation in Aion
    '''
    
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    time_block = models.ForeignKey(TimeBlock, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField('Reservation Date')
    
    class Meta:
        '''Prevents double bookings
        '''
        unique_together = [
            ('resource', 'time_block', 'date')
        ]
    
    def clean(self):
        '''Custom Validation Rules
        '''
        if(self.resource.school != self.time_block.school):
            raise ValidationError({
                'resource' : 'Blocks and Resources must be from the same school.',
                'block': 'Blocks and Resources must be from the same school.'
            })
        
        if(self.resource.school != self.client.profile.location):    
            raise ValidationError({
                'resource': 'Users and resources must be from the same school.',
                'client':'Users and resources must be from the same school.'
            })
        
        if(self.date < date.today()):    
            raise ValidationError({
                'date': "Your reservation date can't be in the past",
            })
    
    def __str__(self):
        return f"{self.client}: {self.resource.name}, {self.date} ({self.time_block.name}, {self.resource.school})"


class Announcement(models.Model):
    title = models.CharField(max_length=100, null=False)
    message = models.TextField(null=False)
    publish_on = models.DateField()
    expires_on = models.DateField()
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    system_wide = models.BooleanField(default=False)
    
    def clean(self):
        '''Custom Validation Rules
        '''
        # if(self.publish_on < date.today()):    
        #     raise ValidationError({
        #         'publish_on': "Your announcment date can't be in the past",
        #     })
        
        if(self.expires_on < self.publish_on):    
            raise ValidationError({
                'expires_on': "Your announcment can't expire before it  is published",
            })
        
    def __str__(self):
        return f'{self.title}, {self.publish_on} - {self.expires_on} ({self.school})'
        