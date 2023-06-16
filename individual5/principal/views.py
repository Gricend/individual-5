from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from principal.forms import FormularioContactoForm, LoginForm
from principal.models import FormularioContacto
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

def landing(request):
    return render(request, 'principal/landing.html')

def lista_usuario(request) -> HttpResponse:
    users = User.objects.all()
    return render(request, 'principal/usuarios.html', {'users': users})

class ContactoView(TemplateView):
    template_name = 'principal/contacto.html'
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["info"] = "Información complementaria"
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["formulario"] = FormularioContactoForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FormularioContactoForm(request.POST)
        mensajes = {
            "enviado": False,
            "resultado": None
        }
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            registro = FormularioContacto(
                nombre=nombre,
                telefono=telefono,
                email=email,
                mensaje=mensaje
            )
            registro.save()

            mensajes = { "enviado": True, "resultado": "Mensaje enviado correctamente" }
            return redirect('landing')
        else:
            mensajes = { "enviado": False, "resultado": form.errors }
        return render(request, self.template_name, { "formulario": form, "mensajes": mensajes})


class Login(TemplateView):
    template_name = 'principal/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, { "form": form })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('landing')
            form.add_error('username', 'Credenciales incorrectas')
            return render(request, self.template_name, { "form": form })
        else:
            return render(request, self.template_name, { "form": form })

class PermisoUsuarios(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'principal/usuarios.html'
    permission_required = 'principal.puede_ver_usuarios'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.exclude(is_superuser=True)
        context['users'] = users
        return context

    def get(self, request, *args, **kwargs):
        titulo = "Restringido"
        if titulo is None:
            return redirect('landing')
        return super().get(request, *args, **kwargs)

class PagRestringida(PermissionRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'principal/restringido.html'
    permission_required = 'principal.puede_ver_pagina'
    def get(self, request, *args, **kwargs):
        titulo = "Restringido"
        contexto = {
        'titulo': titulo,
        }
        if titulo is None:
            return redirect('landing')
        return render(request, self.template_name, contexto)