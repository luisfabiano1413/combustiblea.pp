from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import VehiculoForm
from .models import Vehiculo

@login_required
def mis_vehiculos(request):
    vehiculos = Vehiculo.objects.filter(usuario=request.user)
    return render(request, 'mis_vehiculos.html', {'vehiculos': vehiculos})

@login_required
def inicio(request):
    # Renderiza la plantilla inicio.html
    return render(request, 'inicio.html')

@login_required
def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            vehiculo = form.save(commit=False)
            vehiculo.usuario = request.user
            try:
                vehiculo.save()
                return redirect('inicio')  # Redirige a la página de inicio luego de guardar
            except:
                form.add_error(None, "Ya tienes un vehículo de este tipo registrado.")
    else:
        form = VehiculoForm()
    return render(request, 'registrar_vehiculo.html', {'form': form})

