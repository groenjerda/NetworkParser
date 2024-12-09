from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('parser:parser')

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        group, _ = Group.objects.get_or_create(name='candidate')
        new_user.groups.add(group)
        login(self.request, new_user)
        messages.success(self.request, 'Вы успешно зарегистрировались в системе')
        messages.success(self.request, 'Для дальнейшей работы подтвердите вашу учетную запись у администратора')
        return valid
