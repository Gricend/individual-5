from django import forms

class FormularioContactoForm(forms.Form):
    nombre = forms.CharField(label='Nombre', required=True,
                                max_length=50,
                                error_messages={
                                'required': 'El nombre es obligatorio',
                                'max_length': 'El nombre no puede superar los 50 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                'placeholder': 'Ingrese su nombre',
                                'class': 'form-control'
                                }),
                                help_text='Queremos conocerle, ingrese su nombre completo'
                                )
    email = forms.EmailField(label='Email', required=True,
                                max_length=150, min_length=5,
                                error_messages={
                                'required': 'El email es obligatorio',
                                'max_length': 'El email no puede superar los 150 caracteres',
                                'min_length': 'El email debe tener al menos 5 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                'placeholder': 'Ingrese su correo electrónico',
                                'class': 'form-control'
                                })
                                )
    telefono = forms.CharField(label='Teléfono', required=True,
                                max_length=15, min_length=9,
                                error_messages={
                                'required': 'El email es obligatorio',
                                'max_length': 'El email no puede superar los 15 caracteres',
                                'min_length': 'El email debe tener al menos 9 caracteres'
                                },
                                widget=forms.TextInput(attrs={
                                'placeholder': 'No olvide tus número de teléfono',
                                'class': 'form-control'
                                })
                                )
    mensaje = forms.CharField(label='Mensaje', required=True,
                                max_length=1000,
                                error_messages={
                                'required': 'El email es obligatorio',
                                'max_length': 'El email no puede superar los 1000 caracteres',
                                'min_length': 'El email debe tener al menos 50 caracteres'
                                },
                                widget=forms.Textarea(attrs={
                                'placeholder': 'Cuál es su mensaje para nosotros',
                                'class': 'form-control'
                                })
                                )