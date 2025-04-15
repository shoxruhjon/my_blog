from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.views.generic.edit import FormView


from django.views import View

class RegisterView(View):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            messages.success(
                request,
                f"Xush kelibsiz, {user.username}! Ro'yxatdan muvaffaqiyatli o'tdingiz."
            )
            return redirect('home')  
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
        
        return render(request, self.template_name, {'form': form})


class LoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')  

    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        
        user = form.get_user()
        if user is not None:
            login(self.request, user)
            messages.info(self.request, f"Xush kelibsiz, {user.username}!")  
            next_url = self.request.POST.get('next')
            if next_url:
                return redirect(next_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        
        messages.error(self.request, "Login yoki parol noto'g'ri yoki hisob faol emas.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        return context
    
    
def logout_view(request):
    logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('login')



from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html', {'title': 'Home'})