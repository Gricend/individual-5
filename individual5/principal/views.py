from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from principal.forms import FormularioContactoForm
from principal.models import FormularioContacto

# Create your views here.

def landing(request):
    return render(request, 'landing.html')

def lista_usuario(request) -> HttpResponse:
    users = User.objects.all()
    return render(request, 'usuarios.html', {'users': users})

class ContactoView(TemplateView):
    template_name = 'contacto.html'
    
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