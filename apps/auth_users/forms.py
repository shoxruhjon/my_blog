from django import forms
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    """
    CustomUser modeli uchun foydalanuvchi ro'yxatdan o'tish formasi.
    (Avvalgi kod bilan deyarli bir xil, faqat model CustomUser)
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'})
            if field_name == 'email':
                 field.label = "Elektron pochta (Login uchun)"
            elif field_name == 'username':
                 field.label = "Foydalanuvchi nomi (ixtiyoriy emas)"
            elif field_name == 'password1':
                field.label = "Parol"
            elif field_name == 'password2':
                field.label = "Parolni tasdiqlang"
            elif field_name == 'first_name':
                field.label = "Ism"
            elif field_name == 'last_name':
                field.label = "Familiya"


class CustomAuthenticationForm(AuthenticationForm):
    """
    Email yoki Username orqali tizimga kirish formasi.
    """
    login = forms.CharField(
        label=_("Email yoki Foydalanuvchi nomi"),
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
            'placeholder': 'Email yoki foydalanuvchi nomingiz'
            })
    )
    username = None

    password = forms.CharField(
        label=_("Parol"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
             'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm',
             'placeholder': 'Parolingiz'
             }),
    )

    error_messages = {
        'invalid_login': _(
            "Iltimos, to'g'ri %(username)s yoki parol kiriting. "
            "Ikkala maydon ham регистрga sezgir bo'lishi mumkin."
        ),
        'inactive': _("Bu hisob faol emas."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        Formani initsializatsiya qilish.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs) 

    def clean(self):
        
        login_input = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if login_input is not None and password:
            
            self.user_cache = authenticate(self.request, email=login_input, password=password)
            
            if self.user_cache is None:
                 self.user_cache = authenticate(self.request, username=login_input, password=password)

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def get_user(self):
        return self.user_cache

    
    def get_invalid_login_error(self):
         return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': _('Email yoki Foydalanuvchi nomi')}
        )

class CustomUserChangeForm(UserChangeForm):
    """
    Foydalanuvchi profilini tahrirlash formasi.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'bio', 'profile_picture', 'birth_date', 'location')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
            })