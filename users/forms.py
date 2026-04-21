from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator

User = get_user_model()
#######################################################################################################################

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=66,
                             widget=forms.EmailInput(attrs={'class': 
                                                            'input-register form-control', 
                                                            'placeholder': 'Your email',}))
    first_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 
                                                            'input-register form-control', 
                                                            'placeholder': 'Your email',}))
    last_name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 
                                                            'input-register form-control', 
                                                            'placeholder': 'Your email',}))
    password1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                                              'plaseholder': 'Your password'}))
    
    password2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                                            'plaseholder': 'Your password'}))
    
    marketing_consent1 = forms.BooleanField(required=False, label='I agree to receive commerical, promotional, and marketing communication.',
                                            widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'}))
    
    marketing_consent2 = forms.BooleanField(required=False, label='I agree to receive personalized, commerical communications.',
                                        widget=forms.CheckboxInput(attrs={'class': 'checkbox-input-register'}))
    
    class Meta:
        model = User
        fields =['first_name', 'last_name', 'email', 'password1', 'password2', 
                'marketing_consent1', 'marketing_consent2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = None
        user.marketing_consent1 = self.cleaned_data['marketing_consent1']
        user.marketing_consent2 = self.cleaned_data['marketing_consent2']
        
        if commit:
            user.save()
        return user
#######################################################################################################################
class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Email",
                               widget=forms.TextInput(attrs={"autofocus": True,
                                                             'class': 'input-register form-control',
                                                             'placeholder': 'Your email'}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autofocus": True,
                                        'class': 'input-register form-control',
                                        'placeholder': 'Your email'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive")
        return self.cleaned_data
    
#######################################################################################################################
class CustomUserUpdateForm(forms.ModelForm):
    phone = forms.CharField(required=False, validators=[RegexValidator(r'^\*?1?\d[9, 15]$', "Enter a valid phone number")],
                            widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your phone number'}))
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your first name'})
    )

    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your last name'})
    )

    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your email'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address1', 'address2',
                  'city', 'country', 'province', 'postal_code', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your email'}),
            'first_name': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your last name'}),
            'address1': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your Address line 1'}),
            'address2': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your Address line 2'}),
            'city': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your city'}),
            'country': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your country'}),
            'province': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your province'}),
            'postal_code': forms.TextInput(attrs={'class': 'input-register form-control',
                                                          'placeholder': 'Your postal_code'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("this email is alredy in use.")
        return email
    
    def clean(self):
        cleanned_data = super().clean()
        if not cleanned_data.get('email'):
            cleanned_data['email'] = self.instance.email

            for field in ['address1', 'address2', 'city', 'country', 'province', 'postal_code', 'phone']:
                if cleanned_data.get(field):
                    cleanned_data[field] = strip_tags(cleanned_data[field])
                
                return cleanned_data
