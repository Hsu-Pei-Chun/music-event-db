from django.views.generic import TemplateView, RedirectView
from django.urls import reverse_lazy

# 首頁
class HomeView(TemplateView):
    template_name = 'core/index.html'

# 登入頁面
class LoginView(TemplateView):
    template_name = 'core/login.html'

# 註冊頁面
class RegisterView(TemplateView):
    template_name = 'core/register.html'

# 登出後跳轉首頁
class LogoutView(RedirectView):
    url = reverse_lazy('home')