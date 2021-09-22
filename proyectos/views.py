import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.views import SinPrivilegios
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q
from .models import Imagen, Proyecto, Pago, Documento, Cambio, Actividad
from .forms import ProyectoForm, PagoForm, DocumentoForm, ImagenForm, CambioForm, ActividadForm


############################
## Vistas Modelo Proyecto ##
############################
class ListaProyectos(SinPrivilegios, ListView):
    permission_required = "proyectos.view_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/listado_proyectos.html'
    context_object_name = 'proyectos_list'


# class DetalleProyecto(SinPrivilegios, DetailView):
#     permission_required = "proyectos.view_proyecto"
#     model = Proyecto
#     template_name = 'proyectos/proyecto_detalle.html'
#     context_object_name = 'proyecto'


#     def get_context_data(self, **kwargs):
#         context = super(DetalleProyecto,self).get_context_data(**kwargs)
#         context['cambios'] = Cambio.objects.filter(proyecto_id=detalle_cambio(id))
#         return context

@login_required(login_url='login')
def detalle_proyecto(request, id):
    proyecto = get_object_or_404(Proyecto, id=id)
    duracion_c = Cambio.objects.filter(id=id)
    print(duracion_c)
    cambios = Cambio.objects.filter(proyecto_id=id)
    imagenes = Imagen.objects.filter(proyecto_id=id)
    return render(request, 'proyectos/proyecto/proyecto_detalle.html', {
        'proyecto':proyecto, 
        'cambios':cambios,
        'imagenes':imagenes
        })


class CrearProyecto( SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proyectos.add_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/crear_proyecto.html'
    context_object_name = 'proyecto_create'
    form_class = ProyectoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Proyecto creado correctamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


class EditarProyecto(SuccessMessageMixin , SinPrivilegios, UpdateView):
    permission_required = "proeyctos.change_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/editar_proyecto.html'
    context_object_name = 'proyecto_editar'
    form_class = ProyectoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Proyecto editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarProyecto( SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_proyecto"
    model = Proyecto
    template_name = 'proyectos/proyecto/borrar_proyecto.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Proyecto elimiando satisfactoriamente"


########################
## Vistas Modelo Pago ##
########################
class CrearPago( SuccessMessageMixin,SinPrivilegios, CreateView):
    permission_required = "proyectos.add_pago"
    model = Pago
    template_name = 'proyectos/pago/crear_pago.html'
    form_class = PagoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Pago creado satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


# class DetallePago(LoginRequiredMixin, DeleteView):
#     model = Pago
#     queryset = Pago.objects.filter(pk=proyecto_id)
#     template_name = 'proyectos/pago_detalle.html'
#     context_object_name = 'obj'

@login_required(login_url='login')
def detalle_pago(request, id):
    pagos = Pago.objects.filter(proyecto_id=id)
    total_pagos = Pago.objects.filter(proyecto_id=id).aggregate(Total_Pagos=Sum('valor_pago'))
    if total_pagos['Total_Pagos'] == None:
       total_pagos['Total_Pagos'] = 0
    try:
        e = Pago.objects.get(id=id)
    except Pago.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
        vpp = vp.valor_proyecto  - total_pagos['Total_Pagos']
    else:
        vp = Proyecto.objects.get(id=e.id)
        vpp = vp.valor_proyecto  - total_pagos['Total_Pagos']
    return render(request, 'proyectos/pago/pago_detalle.html', {'pagos':pagos,'total_pagos':total_pagos,'vp':vp,'vpp':vpp})


class EditarPago(SuccessMessageMixin,SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_pago"
    model = Pago
    template_name = 'proyectos/pago/editar_pago.html'
    context_object_name = 'pago_editar'
    form_class = PagoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Pago editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarPago(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_pago"
    model = Pago
    template_name = 'proyectos/pago/borrar_pago.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Pago eliminado correctamente"


#########################
## Datos Para Gráficos ##
#########################
@login_required(login_url='login')
def graficos(request):
    labels = []
    data = []
    queryset = Proyecto.objects.all()
    cant_proy_bun = Proyecto.objects.filter(terminal="BUN").count()
    cant_proy_ctg = Proyecto.objects.filter(terminal="CTG").count()
    cant_proy_bog = Proyecto.objects.filter(terminal="BOG").count()
    cant_proy_bun_eje = Proyecto.objects.filter(terminal="BUN", estado="EJ").count()
    cant_proy_ctg_eje = Proyecto.objects.filter(terminal="CTG", estado="EJ").count()
    cant_proy_bog_eje = Proyecto.objects.filter(terminal="BOG", estado="EJ").count()
    cant_proy_bun_sus = Proyecto.objects.filter(terminal="BUN", estado="S").count()
    cant_proy_ctg_sus = Proyecto.objects.filter(terminal="CTG", estado="S").count()
    cant_proy_bog_sus = Proyecto.objects.filter(terminal="BOG", estado="S").count()
    cant_proy_bun_canc = Proyecto.objects.filter(terminal="BUN", estado="C").count()
    cant_proy_ctg_canc = Proyecto.objects.filter(terminal="CTG", estado="C").count()
    cant_proy_bog_canc = Proyecto.objects.filter(terminal="BOG", estado="C").count()
    cant_proy_bun_fin = Proyecto.objects.filter(terminal="BUN", estado="F").count()
    cant_proy_ctg_fin = Proyecto.objects.filter(terminal="CTG", estado="F").count()
    cant_proy_bog_fin = Proyecto.objects.filter(terminal="BOG", estado="F").count()
    suma_cantidad_proyectos = cant_proy_bun + cant_proy_ctg + cant_proy_bog
    suma_cant_proy_eje = cant_proy_bun_eje + cant_proy_ctg_eje + cant_proy_bog_eje
    suma_cant_proy_sus = cant_proy_bun_sus + cant_proy_ctg_sus + cant_proy_bog_sus
    suma_cant_proy_canc = cant_proy_bun_canc + cant_proy_ctg_canc + cant_proy_bog_canc
    suma_cant_proy_fin = cant_proy_ctg_fin + cant_proy_bun_fin + cant_proy_bog_fin
    total_proyecto = []
    total_proyecto.append(cant_proy_bun)
    total_proyecto.append(cant_proy_ctg)
    total_proyecto.append(cant_proy_bog)
    total_costo_proyectos = Proyecto.objects.all().aggregate(total_costo_proyectos=Sum('valor_proyecto'))
    total_pagos_proyectos = Pago.objects.all().aggregate(Total_Pagos_proyectos=Sum('valor_pago'))
    # porcentaje_ejecucion = (total_pagos_proyectos['Total_Pagos_proyectos']) / (total_costo_proyectos['total_costo_proyectos']) * 100

    for p in queryset:
        labels.append(p.nombre)
        data.append(p.valor_proyecto)
        
    return render(request, 'proyectos/graficas/bar_chart.html', {
        'labels':labels, 
        'data':data, 
        'total_proyecto':total_proyecto, 
        'queryset':queryset,
        'total_costo_proyectos':total_costo_proyectos,
        'total_pagos_proyectos':total_pagos_proyectos,
        'suma_cantidad_proyectos':suma_cantidad_proyectos,
        'suma_cant_proy_eje':suma_cant_proy_eje,
        'suma_cant_proy_sus':suma_cant_proy_sus,
        'suma_cant_proy_fin':suma_cant_proy_fin,
        # 'porcentaje_ejecucion':porcentaje_ejecucion,
        'suma_cant_proy_canc':suma_cant_proy_canc
        })


#############################
## Vistas Modelo Documento ##
#############################
class DocumentoCreate(SuccessMessageMixin,SinPrivilegios, CreateView):
    permission_required = "proyectos.add_documento"
    model = Documento
    template_name = 'proyectos/documento/crear_documento.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Documento cargado correctamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_documentos(request, id):
    documentos = Documento.objects.filter(proyecto_id=id)
    try:
        e = Documento.objects.get(id=id)
    except Documento.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/documento/documento_detalle.html',{'documentos':documentos, 'vp':vp})


class EditarDocumento(SuccessMessageMixin,SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_documento"
    model = Documento
    template_name = 'proyectos/documento/editar_documento.html'
    context_object_name = 'obj'
    form_class = DocumentoForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Documento editado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarDocumento(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_documento"
    model = Documento
    template_name = 'proyectos/documento/borrar_documento.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Documento borrado correctamente"


##########################
## Vistas Modelo Imágen ##
##########################
class CrearImagen( SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proeyctos.add_imagen"
    model = Imagen
    template_name = 'proyectos/imagen/crear_imagen.html'
    form_class = ImagenForm
    success_url = reverse_lazy('proyectos_list')
    success_message = "Imágen cargada correctamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_imagen(request, id):
    imagenes = Imagen.objects.filter(proyecto_id=id)
    try:
        e = Imagen.objects.get(id=id)
    except Imagen.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/imagen/imagen_detalle.html',{'imagenes':imagenes,'vp':vp})


class BorrarImagen(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_imagen"
    model = Imagen
    template_name = 'proyectos/imagen/borrar_imagen.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Imágen cargada correctamente"


##########################
## Vistas Modelo Cambio ##
##########################
@login_required(login_url='login')
@permission_required('proyectos.add_cambio', login_url='sin_privilegios')
def crear_cambio(request):
    if request.method == "POST":
        form = CambioForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            costo = cd['costo']
            duracion = cd['duracion']
            proyecto = Proyecto.objects.filter(id=request.POST['proyecto']).values()

            if costo == None:
                valor_proyecto = proyecto[0]['valor_proyecto']
            else:
                valor_proyecto = proyecto[0]['valor_proyecto'] + costo

            if duracion == None:
                duracion_proy = proyecto[0]['fecha_fin']
            else:   
                duracion_proy = proyecto[0]['fecha_fin'] + datetime.timedelta(days=duracion)

            Proyecto.objects.filter(id=request.POST['proyecto']).update(valor_proyecto=valor_proyecto)
            Proyecto.objects.filter(id=request.POST['proyecto']).update(fecha_fin=duracion_proy)
            form.instance.uc = request.user
            proyecto.um=request.user.id
            form.save()
            messages.success(request, 'Cambio creado correctamente')
            return redirect('proyectos_list')

    else:
        form = CambioForm()
        return render(request, 'proyectos/cambio/crear_cambio.html', {'form':form})


class EditarCambio(SuccessMessageMixin,SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_cambio"
    model = Cambio
    template_name = 'proyectos/cambio/editar_cambio.html'
    form_class = CambioForm
    success_url = reverse_lazy('proyectos_list')
    context_object_name = 'obj'
    success_message = "Control de cambio actualizado correctamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarCambio(SuccessMessageMixin,SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_cambio"
    model = Cambio
    template_name = 'proyectos/cambio/borrar_cambio.html'
    context_object_name = 'obj'
    success_url = reverse_lazy('proyectos_list')
    success_message = "Control de cambio borrado correctamente"


#######################
## Lisdatos Gráficas ##
#######################
@login_required(login_url='login')
def listado_proyectos_costo(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/listas/listado_costo_proyectos.html', {'proyectos':proyectos})


@login_required(login_url='login')
def listado_pagos_proyectos(request):
    pagos = Pago.objects.all().order_by('-fecha_pago')
    print(pagos)
    return render(request, 'proyectos/listas/listado_pagos_proyectos.html', {'pagos':pagos})


@login_required(login_url='login')
def listado_proyectos_ejecucion(request):
    proy_eje = Proyecto.objects.filter(estado="EJ")
    return render(request, 'proyectos/listas/listado_proyectos_eje.html', {'proy_eje':proy_eje})


@login_required(login_url='login')
def listado_proy_sus(request):
    proy_susp = Proyecto.objects.filter(estado="S")
    return render(request, 'proyectos/listas/listado_proyectos_susp.html', {'proy_susp':proy_susp})


@login_required(login_url='login')
def listado_proy_can(request):
    proy_canc = Proyecto.objects.filter(estado="C")
    return render(request, 'proyectos/listas/listado_proyectos_canc.html', {'proy_canc':proy_canc})


@login_required(login_url='login')
def listado_proy_fin(request):
    proy_fin = Proyecto.objects.filter(estado="F")
    return render(request, 'proyectos/listas/listado_proyectos_fin.html', {'proy_fin':proy_fin})


#############################
## Vistas Modelo Actividad ##
#############################
class CrearActividad(SuccessMessageMixin, SinPrivilegios, CreateView):
    permission_required = "proyectos.add_actividad"
    model = Actividad
    template_name = 'proyectos/actividad/crear_actividad.html'
    form_class = ActividadForm
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad creada correctamente'

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)


@login_required(login_url='login')
def detalle_actividad(request, id):
    actividades = Actividad.objects.filter(proyecto_id=id)
    try:
        e = Actividad.objects.get(id=id)
    except Actividad.DoesNotExist:
        e = None
    if e == None:
        vp = Proyecto.objects.get(id=id)
    else:
        vp = Proyecto.objects.get(id=e.id)
    return render(request, 'proyectos/actividad/actividad_detalle.html', {'actividades': actividades, 'vp':vp})


class ActualizarActividad(SuccessMessageMixin, SinPrivilegios, UpdateView):
    permission_required = "proyectos.change_actividad"
    model = Actividad
    form_class = ActividadForm
    template_name = 'proyectos/actividad/actualizar_actividad.html'
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad actualizada correctamente'

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)


class BorrarActividad(SuccessMessageMixin, SinPrivilegios, DeleteView):
    permission_required = "proyectos.delete_actividad"
    model = Actividad
    context_object_name = 'obj'
    template_name = 'proyectos/actividad/borrar_actividad.html'
    success_url = reverse_lazy('graficos')
    success_message = 'Actividad borrada correctamente'