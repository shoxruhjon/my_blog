# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
# Formalarni import qilamiz
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic.edit import FormView


from django.views import View

class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get(self, request):
        # GET so'rov uchun forma yaratamiz
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # POST so'rov uchun forma bilan ishlaymiz
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()  # Foydalanuvchini saqlaymiz
            login(request, user)  # Foydalanuvchini tizimga kiritamiz
            messages.success(
                request,
                f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz."
            )
            return redirect('home')  # 'home' URL nomini o'zingiznikiga moslang
        else:
            # Agar forma valid bo'lmasa, xatoliklarni ko'rsatamiz
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
        
        # Agar forma noto'g'ri bo'lsa, forma bilan birga sahifani qayta render qilamiz
        return render(request, self.template_name, {'form': form})

# Ro'yxatdan o'tish funksiyasi (register_view) o'zgarishsiz qoladi
# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
#             return redirect('home') # 'home' URL nomini o'zingiznikiga moslang
#         else:
#             for field, errors in form.errors.items():
#                  for error in errors:
#                       messages.error(request, f"{form.fields[field].label}: {error}")
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'registration/register.html', {'form': form})


# # Login funksiyasini yangilaymiz
# def login_view(request):
#     if request.user.is_authenticated:
#          return redirect('home')

#     if request.method == 'POST':
#         # Endi CustomAuthenticationForm dan foydalanamiz
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             # Formaning o'zi autentifikatsiyani `clean` metodi orqali bajaradi
#             # Biz faqat foydalanuvchini `get_user()` orqali olamiz
#             user = form.get_user()
#             if user is not None:
#                 login(request, user)
#                 messages.info(request, f"Xush kelibsiz, {user.username}!") # Yoki user.email
#                 next_url = request.POST.get('next')
#                 if next_url:
#                     return redirect(next_url)
#                 else:
#                     return redirect('home')
#             # Agar user None bo'lsa, formaning o'zi xatolikni ko'rsatadi
#             # Shuning uchun bu yerda qo'shimcha xatolik xabari shart emas
#             # else:
#             #     messages.error(request, "Login yoki parol noto'g'ri.") # Bu kerak emas
#         else:
#             # Agar forma valid bo'lmasa (masalan, maydonlar bo'sh bo'lsa yoki boshqa xatolik)
#             # Formaning o'zi xatoliklarni ko'rsatadi, lekin umumiy xabar ham berishimiz mumkin
#              messages.error(request, "Login yoki parol noto'g'ri yoki hisob faol emas.")
#     else:
#         form = CustomAuthenticationForm()

#     next_url = request.GET.get('next', '')
#     # Templatega 'login' formasi o'rniga 'form' ni uzatamiz
#     return render(request, 'registration/login.html', {'form': form, 'next': next_url})





class LoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')  # Muvaffaqiyatli kirishdan keyin qaytish URL

    def dispatch(self, request, *args, **kwargs):
        # Agar foydalanuvchi allaqachon tizimga kirgan bo'lsa, 'home' ga yo'naltiramiz
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Forma valid bo'lganda, foydalanuvchini autentifikatsiya qilamiz
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"Xush kelibsiz, {user.username}!")  # Yoki user.email
            next_url = self.request.POST.get('next')
            if next_url:
                return redirect(next_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        # Forma valid bo'lmasa, xatolik haqida xabar beramiz
        messages.error(self.request, "Login yoki parol noto'g'ri yoki hisob faol emas.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # Templatega qo'shimcha context ma'lumotlarini uzatamiz
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context
    
    

# Chiqish funksiyasi (logout_view) o'zgarishsiz qoladi
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')



from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html', {'title': 'Home'})