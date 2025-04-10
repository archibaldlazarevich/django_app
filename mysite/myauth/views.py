from random import random

from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext_lazy as _, ngettext
from django.views.decorators.cache import cache_page

from .models import Profile


class HelloView(View):
    welcome_message = _("welcome hello word")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>" f"\n<h2>{products_line}</h2>"
        )


class AboutMeView(UpdateView):
    template_name = "myauth/about-me.html"
    model = Profile
    fields = ("avatar",)
    success_url = reverse_lazy("myauth:about-me")

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)


class UpdateProfile(UserPassesTestMixin, UpdateView):
    template_name = "myauth/update-profile.html"
    model = Profile
    fields = ("avatar",)
    success_url = reverse_lazy("myauth:about-me")

    def test_func(self):
        if self.request.user.is_staff:
            return True
        if self.request.user.pk == self.get_object().user_id:
            return True


class UsersListView(ListView):
    template_name = "myauth/users-list.html"
    context_object_name = "profiles"
    queryset = Profile.objects.all()
    success_url = reverse_lazy("myauth:user-details")


class UserUpdateProfile(DetailView):
    template_name = "myauth/user-details.html"
    model = Profile
    fields = ("avatar",)
    success_url = reverse_lazy("myauth:update-profile")

    def get_object(self, queryset=None):
        user_id = self.kwargs["user_id"]
        return get_object_or_404(Profile, user_id=user_id)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            username=username,
            password=password,
        )

        login(request=self.request, user=user)
        return response


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("myauth:login")


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
