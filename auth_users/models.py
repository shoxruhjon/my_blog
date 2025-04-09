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
    # Username hali ham mavjud va unikal bo'lishi mumkin (yoki unique=False qilsa ham bo'ladi)
    # username maydoni AbstractUser'da allaqachon mavjud

    # Emailni unikal va asosiy identifikator qilamiz
    email = models.EmailField(_('elektron pochta manzili'), unique=True)

    # Qo'shimcha maydonlar
    bio = models.TextField(_('biografiya'), max_length=500, blank=True)
    profile_picture = models.ImageField(_('profil rasmi'), upload_to='profile_pics/', null=True, blank=True)
    birth_date = models.DateField(_('tug\'ilgan sana'), null=True, blank=True)
    location = models.CharField(_('joylashuv'), max_length=100, blank=True)

    # Yaratilgan vaqtni avtomatik saqlash uchun maydon
    # auto_now_add=True: Obyekt birinchi marta yaratilganda hozirgi vaqtni avtomatik yozadi
    created_at = models.DateTimeField(_('yaratilgan vaqt'), auto_now_add=True)

    # Yangilangan vaqtni avtomatik saqlash uchun (ixtiyoriy)
    # auto_now=True: Obyekt har safar saqlanganda (save()) hozirgi vaqtni avtomatik yozadi
    # updated_at = models.DateTimeField(_('yangilangan vaqt'), auto_now=True)

    USERNAME_FIELD = 'email' # Asosiy login maydoni - email
    # Email va paroldan tashqari 'createsuperuser' buyrug'ida so'raladigan maydonlar
    # Agar username'ni ham talab qilmoqchi bo'lsangiz, uni shu ro'yxatga qo'shing
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('foydalanuvchi')
        verbose_name_plural = _('foydalanuvchilar')
        ordering = ['-created_at'] # Ro'yxatlarni yaratilgan vaqt bo'yicha teskari tartiblash

