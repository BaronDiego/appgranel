from django.urls import path
from . import views

urlpatterns = [
    path('listado_proyectos/', views.ListaProyectos.as_view(), name='proyectos_list'),
    path('detalle/<int:id>/', views.detalle_proyecto, name='detalle_proyecto'),
    path('crear_proyecto/', views.CrearProyecto.as_view(), name='crear_proeycto'),
    path('editar/<pk>/', views.EditarProyecto.as_view(), name='editar_proyecto'),
    path('borrar_proyecto/<pk>/', views.BorrarProyecto.as_view(), name='borrar_proyecto'),
    path('pago/', views.CrearPago.as_view(), name='crear_pago'),
    # path('pago/<pk>/', views.DetallePago.as_view(), name='detalle_apgo'),
    path('pago_detalle/<int:id>/', views.detalle_pago, name='detalle_pago'),
    path('editar_pago/<pk>/', views.EditarPago.as_view(), name='editar_pago'),
    path('borrar_pago/<pk>', views.BorrarPago.as_view(), name='borrar_pago'),
    # path('', views.graficos, name='graficos'),
    path('documento/', views.DocumentoCreate.as_view(), name='crear_documento'),
    path('documento_detalle/<int:id>/', views.detalle_documentos, name='detalle_doc'),
    path('editar_documento/<pk>/', views.EditarDocumento.as_view(), name='editar_documento'),
    path('borrar_documento/<pk>/', views.BorrarDocumento.as_view(), name='borrar_documento'),
    path('imagen/', views.CrearImagen.as_view(), name='cargar_imagen'),
    path('imagen_detalle/<int:id>/', views.detalle_imagen, name='detalle_imagen'),
    path('borrar_imagen/<pk>/', views.BorrarImagen.as_view(), name='borrar_imagen'),
    path('crear_cambio/', views.crear_cambio, name='crear_cambio'),
    # path('detalle_cambio/<int:id>/', views.detalle_cambio, name='detalle_cambio'),
    path('editar_cambio/<pk>/', views.EditarCambio.as_view(), name='editar_cambio'),
    path('borrar_cambio/<pk>/', views.BorrarCambio.as_view(), name='borrar_cambio'),
    path('listado_costos_proyectos/', views.listado_proyectos_costo, name='listado_costos'),
    path('listado_pagos_proyectos/', views.listado_pagos_proyectos, name='listado_pagos'),
    path('listado_proy_ejec/', views.listado_proyectos_ejecucion, name='listado_proy_ejec'),
    path('listado_proy_susp/', views.listado_proy_sus, name='listado_proy_susp'),
    path('listado_proy_canc/', views.listado_proy_can, name='listado_proy_canc'),
    path('listado_proy_fin/', views.listado_proy_fin, name='listado_proy_fin'),
    path('crear_actividad/', views.CrearActividad.as_view(), name='crear_actividad'),
    path('detalle_actividad/<int:id>/', views.detalle_actividad, name='detalle_actividad'),
    path('actualizar_actividad/<pk>/', views.ActualizarActividad.as_view(), name='actualizar_actividad'),
    path('eliminar_actividad/<pk>/', views.BorrarActividad.as_view(), name='borrar_actividad'),
]