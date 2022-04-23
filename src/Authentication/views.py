from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from django.contrib.auth.views import LoginView


class SignIn(LoginView):
    template_name = 'Authentication/sign_in.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')


class SignUp(FormView):
    template_name = 'Authentication/sign_up.html'
    redirect_authenticated_user = True
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUp, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(SignUp, self).get(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index')

