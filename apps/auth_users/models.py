# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone # vaqtni olish uchun

class CustomUser(AbstractUser):
    """
    Kengaytirilgan maxsus foydalanuvchi modeli.
    Email yoki username orqali login qilish imkoniyati va yaratilgan vaqtni saqlash.
    """
    email = models.EmailField(_('elektron pochta manzili'), unique=True)

    bio = models.TextField(_('biografiya'), max_length=500, blank=True)
    profile_picture = models.ImageField(_('profil rasmi'), upload_to='profile_pics/', null=True, blank=True)
    birth_date = models.DateField(_('tug\'ilgan sana'), null=True, blank=True)
    location = models.CharField(_('joylashuv'), max_length=100, blank=True)

    created_at = models.DateTimeField(_('yaratilgan vaqt'), auto_now_add=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('foydalanuvchi')
        verbose_name_plural = _('foydalanuvchilar')
        ordering = ['-created_at']

