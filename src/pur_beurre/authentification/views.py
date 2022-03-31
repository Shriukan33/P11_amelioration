from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .forms import UserRegisterForm


class MyLoginView(LoginView):
    template_name = 'authentification/login.html'
    redirect_field_name = "next"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["next"] = reverse_lazy("product_lookup:product_lookup")
        return context


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'authentification/create_account.html'
    success_url = reverse_lazy('authentification:login')
    form_class = UserRegisterForm
    success_message = "Votre compte a été créé avec succès !"


class MyLogoutView(LogoutView):
    """This view de-auth the user, and redirects to login"""
    next_page = reverse_lazy('authentification:login')


class UserProfile(LoginRequiredMixin, DetailView):
    """This view displays the user profile"""
    model = User
    template_name = 'authentification/user_profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
