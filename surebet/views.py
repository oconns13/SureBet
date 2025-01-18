from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth import logout, login
from django.views.generic import FormView

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)

def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler400(request, exception):
    return render(request, '400.html', status=400)

def userlogout(request):
	logout(request)
	return redirect('home')

class LoginFormView(FormView):
	template_name = "login.html"
	form_class = forms.AuthenticateUserForm
	success_url = '/home'
	
	def form_valid(self, form):
		login(self.request, form.get_user())
		return super().form_valid(form)

class RegisterFormView(FormView):
	template_name = "register.html"
	form_class = forms.CreateUserForm
	success_url = '/home'
	
	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return super().form_valid(form)