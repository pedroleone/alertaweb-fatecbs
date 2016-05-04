from django.conf.urls import url, include
from django.contrib.auth import views
import django.contrib.auth.views
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mobile/$', views.index_mobile, name='index_mobile'),
    url(r'^cadastro/', views.cadastro_alerta, name='cadastro_alerta'),
    url(r'^editar/(?P<id>[0-9]+)/$', views.editar_alerta, name='edita_alerta'),
    url(r'^listagem/', views.alertas, name='alertas'),
    url(r'^alerta/(?P<pk>[0-9]+)/$', views.detalhe_alerta,name='detalhe_alerta'),

    url(r'^json/$', views.json, name='json'),
    url(r'^api/$', views.json, name='json'),
    url(r'^relate/', views.reporte_visitante, name='reporte_visitante'),
    url(r'^anuncios/$', views.anuncios, name='anuncios'),
    url(r'^obrigado/$', TemplateView.as_view(template_name='alertas/obrigado.html')),

    url(r'^operacional/$', views.listagem_operacional, name='listagem_operacional'),
    url(r'^operacional/cadastro/$', views.cadastro_operacional, name='cadastro_operacional'),
    url(r'^operacional/editar_rascunho/(?P<id>[0-9]+)/$', views.editar_alerta_operacional, name='editar_alerta_operacional'),
    url(r'^operacional/mensagem/$', views.operacional_lista_alertas_mensagem, name='operacional_lista_alertas_mensagem'),
    url(r'^operacional/mensagem/(?P<pk>[0-9]+)/$', views.cadastro_mensagem_operacional, name='cadastro_mensagem_operacional'),
    url(r'^operacional/anuncios/$', views.cadastro_anuncio, name='cadastro_anuncio'),

    url(r'^operacional/relatos/$', views.relatos_operacional, name='relatos_operacional'),
    url(r'^operacional/relatos/(?P<id>[0-9]+)/$', views.detalhe_relato, name='detalhe_relato'),
    url(r'^operacional/relatos/(?P<id>[0-9]+)/rejeitar/$', views.rejeitar_relato, name='rejeitar_relato'),
    url(r'^operacional/relatos/criar/(?P<id>[0-9]+)/$', views.criar_alerta_relato, name='criar_alerta_relato'),


    url(r'^supervisor/$', views.listagem_supervisor, name='listagem_supervisor'),
    url(r'^supervisor/aprovacao_alerta/(?P<id>[0-9]+)/$', views.aprovacao_alerta, name='aprovacao_alerta'),
    url(r'^supervisor/arquivar_alerta/(?P<id>[0-9]+)/$', views.arquivar_alerta, name='arquivar_alerta'),
    url(r'^supervisor/apagar_alerta/(?P<id>[0-9]+)/$', views.apagar_alerta, name='apagar_alerta'),
    url(r'^supervisor/mensagem/(?P<pk>[0-9]+)/$', views.detalhe_alerta, name='mensagem'),
    url(r'^supervisor/anuncios/$', views.controle_anuncio_supervisor, name='controle_anuncio_supervisor'),


    url(r'^supervisor/aprovacao_alerta/(?P<id>[0-9]+)/aprovar/$', views.aprovar_alerta, name='aprovar_alerta'),
    url(r'^supervisor/aprovacao_alerta/(?P<id>[0-9]+)/reprovar/$', views.rejeitar_alerta, name='rejeitar_alerta'),

    url('^', include('django.contrib.auth.urls')),



    #url(r'^login/$', django.contrib.auth.views.login, name='login'),
    #url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),

    #url(r'^login/', views.login, name='login'),
    #url(r'^logout/', views.logout, name='logout'),

]