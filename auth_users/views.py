# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Formalarni import qilamiz
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Ro'yxatdan o'tish funksiyasi (register_view) o'zgarishsiz qoladi
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('home') # 'home' URL nomini o'zingiznikiga moslang
        else:
            for field, errors in form.errors.items():
                 for error in errors:
                      messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# Login funksiyasini yangilaymiz
def login_view(request):
    if request.user.is_authenticated:
         return redirect('home')

    if request.method == 'POST':
        # Endi CustomAuthenticationForm dan foydalanamiz
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Formaning o'zi autentifikatsiyani `clean` metodi orqali bajaradi
            # Biz faqat foydalanuvchini `get_user()` orqali olamiz
            user = form.get_user()
            if user is not None:
                login(request, user)
                messages.info(request, f"Xush kelibsiz, {user.username}!") # Yoki user.email
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('home')
            # Agar user None bo'lsa, formaning o'zi xatolikni ko'rsatadi
            # Shuning uchun bu yerda qo'shimcha xatolik xabari shart emas
            # else:
            #     messages.error(request, "Login yoki parol noto'g'ri.") # Bu kerak emas
        else:
            # Agar forma valid bo'lmasa (masalan, maydonlar bo'sh bo'lsa yoki boshqa xatolik)
            # Formaning o'zi xatoliklarni ko'rsatadi, lekin umumiy xabar ham berishimiz mumkin
             messages.error(request, "Login yoki parol noto'g'ri yoki hisob faol emas.")
    else:
        form = CustomAuthenticationForm()

    next_url = request.GET.get('next', '')
    # Templatega 'login' formasi o'rniga 'form' ni uzatamiz
    return render(request, 'registration/login.html', {'form': form, 'next': next_url})


# Chiqish funksiyasi (logout_view) o'zgarishsiz qoladi
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')



from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html', {'title': 'Home'})