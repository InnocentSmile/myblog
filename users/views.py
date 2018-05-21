from django.shortcuts import render,redirect,reverse
from django.contrib import messages
# Create your views here.
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import RegisterForm
from users.models import User


def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            messages.success(request, '注册成功,请登录')
            if redirect_to:
                login(request,user)
                return redirect(redirect_to)
            else:
                return redirect(reverse('login'))
    else:
        return render(request,'users/register.html',{'form':form,'next':redirect_to})


class EditUserView(UpdateView):
    model = User
    fields = ['nickname','headshot','email','signature']
    success_url = reverse_lazy('blog:index')



















