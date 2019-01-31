from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm

import re
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML

from django.contrib.auth.models import User
from .models import Profile, Resource, TimeBlock

from .deep_fried_form import DeepFriedForm


class SignUpForm(UserCreationForm):
    '''Extend the UserCreationForm to create a 
    custom signup form
    '''
    
    # Add the email field to the user creation form
    email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.')
    
    class Meta:
        model = User
        fields = 'username','email', 'password1', 'password2'
    
    def clean_email(self):
        '''Validate teacher email
        '''
        
        email = self.cleaned_data['email']
        domain = re.search("@[\w.]+", email) # must be @worcesterschools.net
        uname = re.search("^student", email) # Must not begin with 'student' (should be None)
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
            
        if(domain.group() == '@worcesterschools.net' and uname is None): 
            return email
        # Invalid. Raise exception
        raise ValidationError("You must register a valid wps teacher email to sign up for this service.")

    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''
        super(SignUpForm, self).__init__(*args, **kwargs)
       
        # Create the label for email
        self.fields['email'].label = "Email"
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Register',
                cancel_url='/signin/',
                cancel_text='Sign In'
            )
        )
        self.helper.form_show_labels = False # surpress labels


class LogInForm(AuthenticationForm):
    '''Custom Login Form
    '''

    class Meta:
        model = User
        fields = 'username','password'
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(LogInForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Sign In",
                cancel_url="/signup/",
                cancel_text="Sign Up"
            )
        )
        self.helper.form_show_labels = False # surpress labels


'''Custom User and Profile Form
'''


class UserForm(forms.ModelForm):
    '''User Form
    '''
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')
    
    '''Extend Crispy Forms helper and layout objects.
    '''
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons = False
            )
        )
        self.helper.form_show_labels = False # surpress labels
        self.helper[0:2].wrap_together(Fieldset, '{{ request.user }}')
        self.helper.form_tag=False
        

class ProfileForm(forms.ModelForm):
    '''Profile Form 
    '''
    
    class Meta:
        model = Profile
        fields = ('location', )
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms helper and layout objects.
        '''
        
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Save Profile",
                cancel_url="/home/",
                cancel_text="Cancel"
            )
        )  
        
        self.helper.layout.insert(
            0, # Index of layout items.
            HTML(
                '<small class="helper-text">Choosing a building is required for making reservations.</small>'
            ),
        )
        self.helper.form_tag=False
        self.helper.form_show_labels = False # surpress labels


class EditSchoolAdminForm(forms.ModelForm):
    '''Custom Profile form to edit school admin access
    '''
    class Meta:
        model = Profile 
        fields = ('school_admin',)
    
    def __init__(self, *args, **kwargs):
        '''Extend crispy forms layout objects 
        '''
        super(EditSchoolAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Access",
            )
        )
        self.helper.form_show_labels = False # surpress labels 


class EditTimeBlockForm(forms.ModelForm):
    '''Custom Edit Blocks Form
    for building admins
    '''
    class Meta:
        model = TimeBlock
        fields = ('name','sequence','enabled')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(EditTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Block",
            )
        )
        
        self.helper.form_show_labels = False # surpress labels 


class DeleteTimeBlockForm(forms.ModelForm):
    '''Custom Delete block Form for building admins
    '''
    class Meta:
        model = TimeBlock
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(DeleteTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
            )
        )
        
        self.helper.form_show_labels = False # surpress labels 


class NewTimeBlockForm(forms.ModelForm):
    '''Custom Create Block Form  
    for Building Admins
    '''
    
    class Meta:
        model = TimeBlock 
        fields=('name', 'sequence',)
        
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects. 
        '''
        super(NewTimeBlockForm, self).__init__(*args, **kwargs)
        # Get the crispy helper
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text='Create New Block',
            )
        )
        self.helper.form_show_labels = False

        
class NewResourceForm(forms.ModelForm):
    '''Custom Create Resource Form
    for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(NewResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Create Resource",
            )
        )
        self.helper.form_show_labels = False # surpress labels
        

class EditResourceForm(forms.ModelForm):
    '''Custom Edit Resource Form
    for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name','enabled')
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(EditResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Update Resource",
            )
        )
        
        self.helper.form_show_labels = False # surpress labels

class DeleteResourceForm(forms.ModelForm):
    '''Custom Delete Resource Form for building admins
    '''
    class Meta:
        model = Resource
        fields = ('name',)
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(DeleteResourceForm, self).__init__(*args, **kwargs)
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                render_buttons=False,
                render_delete_buttons=True,
            )
        )
        
        self.helper.form_show_labels = False # surpress labels

class PasswordResetFormAion(PasswordResetForm):
    '''Custom Password Reset Form
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordResetFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Reset Password",
            )
        )
        self.helper.form_show_labels = False # surpress labels

class PasswordResetConfirmFormAion(SetPasswordForm):
    '''Custom Password Reset Confirm Form 
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordResetConfirmFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False # surpress labels
        
class PasswordChangeFormAion(PasswordChangeForm):
    '''Custom PasswordChangeForm
    '''
    
    def __init__(self, *args, **kwargs):
        '''Extend Crispy Forms layout objects.
        '''
        
        super(PasswordChangeFormAion, self).__init__(*args, **kwargs)
        
        # Get the crispy helper and layout objects ready
        self.helper = FormHelper(self)
        self.helper.layout = Layout()
        self.helper.layout.append(
            DeepFriedForm(
                submit_text="Change Password",
            )
        )
        self.helper.form_show_labels = False
    
class AjaxMakeReservationForm(forms.Form):
    resource_id = forms.IntegerField(required=True)
    time_block_id = forms.IntegerField(required=True)
    date = forms.DateField(required=True)

class AjaxCancelReservationForm(forms.Form):
    reservation_id = forms.IntegerField(required=True)
    