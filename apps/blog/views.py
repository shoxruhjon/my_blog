from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import F
from django.urls import reverse_lazy # URL manzilini qaytarish uchun
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # Kirish va huquqlarni tekshirish uchun
from django.http import Http404 # 404 xatolik uchun
from .models import Post
from .forms import PostForm # PostForm'ni import qilamiz (keyinroq yaratamiz)

class PostListView(generic.ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_approved=True).order_by('-created_at')
    
    def get_queryset(self):
        queryset = Post.objects.filter(is_approved=True).order_by('-created_at')
        print("Tasdiqlangan postlar ro'yxati:", queryset)
        return queryset


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.is_approved:
            Post.objects.filter(pk=obj.pk).update(views=F('views') + 1)
            obj.refresh_from_db()
        elif self.request.user == obj.author or self.request.user.is_staff:
            # Muallif yoki admin tasdiqlanmagan postni ko'rishi mumkin
            pass
        else:
            raise Http404("Post topilmadi yoki tasdiqlanmagan.")
        return obj

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_authenticated:
            return qs.filter(is_approved=True)
        elif not self.request.user.is_staff and self.request.user.is_authenticated:
            # Muallif bo'lmagan autentifikatsiya qilingan foydalanuvchilar uchun faqat tasdiqlangan postlar
            return qs.filter(is_approved=True)
        # Adminlar va mualliflar barcha postlarni ko'rishi mumkin (bu yerda filtrlash kerak emas)
        return qs

# --- Yangi ko'rinishlar ---

class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Yangi post yaratish uchun ko'rinish. Faqat tizimga kirgan foydalanuvchilar uchun.
    """
    model = Post
    form_class = PostForm # forms.py'da yaratilgan formani ishlatamiz
    template_name = 'blog/post_form.html'
    # success_url = reverse_lazy('blog:post_list') # Muvaffaqiyatli yaratilgandan so'ng qaytish manzili

    def form_valid(self, form):
        """
        Forma to'g'ri to'ldirilganda avtomatik ravishda muallifni belgilaydi.
        """
        form.instance.author = self.request.user
        # Yangi postlar odatda tasdiqlanmagan bo'ladi (agar admin yaratmasa)
        if not self.request.user.is_staff:
             form.instance.is_approved = False
        else:
             # Agar admin yaratsa, darhol tasdiqlashi mumkin (ixtiyoriy)
             form.instance.is_approved = True # Yoki buni False qoldirib, keyin admin panelda tasdiqlash
        return super().form_valid(form)

    def get_success_url(self):
        print(f"Yangi post ID: {self.object.pk}")
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Shablonga qo'shimcha kontekst qo'shish (masalan, sahifa sarlavhasi)."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Yangi Post Yaratish"
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """
    Mavjud postni tahrirlash uchun ko'rinish. Faqat muallif yoki adminlar uchun.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # success_url post detail sahifasiga yo'naltiriladi (get_success_url orqali)

    def test_func(self):
        """
        Foydalanuvchi post muallifi yoki admin ekanligini tekshiradi.
        """
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def form_valid(self, form):
        """Tahrirlanganda is_approved statusini o'zgartirmaslik (agar kerak bo'lsa)"""
        # Agar admin tahrirlamasa va post tasdiqlangan bo'lsa, statusni o'zgartirmaymiz
        # Yoki admin tahrirlasa, statusni o'zgartirishi mumkin
        # Bu logikani o'zingizga moslashtiring
        if not self.request.user.is_staff:
            original_post = Post.objects.get(pk=self.object.pk)
            form.instance.is_approved = original_post.is_approved # Avvalgi statusni saqlash
        # Agar admin tahrirlasa, formadagi is_approved qiymati saqlanadi (agar formada bo'lsa)
        # Agar is_approved formaga qo'shilmagan bo'lsa, uni alohida handle qilish kerak
        return super().form_valid(form)

    def get_success_url(self):
        """Muvaffaqiyatli tahrirlangandan so'ng post detail sahifasiga yo'naltirish."""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        """Shablonga qo'shimcha kontekst qo'shish."""
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Postni Tahrirlash"
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    """
    Postni o'chirish uchun ko'rinish. Faqat muallif yoki adminlar uchun.
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home') # O'chirilgandan so'ng asosiy sahifaga qaytish

    def test_func(self):
        """
        Foydalanuvchi post muallifi yoki admin ekanligini tekshiradi.
        """
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff