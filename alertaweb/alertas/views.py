from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse


from .models import Alert, AlertDetail, AlertStatus, Organ, ReportedAlert, Announcement
from .forms import AlertForm, AlertDetailForm, FormCadastroOperacional, FormCadastroMensagemOperacional, ReportedAlertForm, AnnouncementForm

def index(request):
    active_alerts = Alert.objects.all().filter(active=True).filter(status__status_code=20)
    context = {'active_alerts': active_alerts}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    return render(request, 'alertas/index.html', context)

def index_mobile(request):
    active_alerts = Alert.objects.all().filter(active=True).filter(status__status_code=20)
    context = {'active_alerts': active_alerts}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    return render(request, 'alertas/index_mobile.html', context)

@login_required(login_url='/login/')
def cadastro_alerta(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listagem/')
    else:
        form = AlertForm()
    context = {'form': form}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    return render(request,'alertas/cadastro.html',context)


@login_required(login_url='/login/')
def editar_alerta(request, id):
    context = {}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    if request.user.is_authenticated():
        alert = get_object_or_404(Alert, pk=id)
        form = AlertForm(instance=alert)
        if request.method == 'POST':
            form = AlertForm(request.POST, instance=alert)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/listagem/')

        context = {'form': form, 'alert': alert}

        return render(request,'alertas/edit.html',context)
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def alertas(request):
    #active_alerts = Alert.objects.all().filter(active=True)
    if request.user.is_authenticated():
        alertas = Alert.objects.all()
        context = {'alertas': alertas}
        if not request.user.is_authenticated():
            context['permission'] = 0
        else:
            context['permission'] = request.user.userorgan.user_permission
        if request.method == 'POST':
            list_actions = request.POST.getlist('alerta')
            if 'deactivate' in request.POST:
                for alert_id in list_actions:
                    alert = Alert.objects.get(pk=alert_id)
                    alert.active = False
                    alert.save()
            if 'activate' in request.POST:
                for alert_id in list_actions:
                    alert = Alert.objects.get(pk=alert_id)
                    alert.active = True
                    alert.save()
            if 'delete' in request.POST:
                for alert_id in list_actions:
                    Alert.objects.get(pk=alert_id).delete()
        return render(request, 'alertas/listagem.html', context)
    else:
        return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def detalhe_alerta(request, pk):

    alert = get_object_or_404(Alert, pk=pk)
    mensagens = AlertDetail.objects.filter(alert=alert)
    form = AlertDetailForm(initial={'alert':pk})
    bootstrap_alerts = []
    if request.method == 'POST':
        list_actions = request.POST.getlist('alert_detail')
        if 'hide' in request.POST:
            for alert_detail_id in list_actions:
                alert_detail = AlertDetail.objects.get(pk=alert_detail_id)
                alert_detail.private = True
                alert_detail.save()
            if len(list_actions) == 1:
                alert_msg = 'O alerta foi ocultado com sucesso'
            else:
                alert_msg = 'Os alertas foram ocultados com sucesso'
            bootstrap_alerts.append({'alert_type': 'alert-success','alert_title': 'glyphicon-ok', 'alert_message':alert_msg})
        elif 'unhide' in request.POST:
            for alert_detail_id in list_actions:
                alert_detail = AlertDetail.objects.get(pk=alert_detail_id)
                alert_detail.private = False
                alert_detail.save()
            if len(list_actions) == 1:
                alert_msg = 'O alerta foi exibido com sucesso'
            else:
                alert_msg = 'Os alertas foram exibidos com sucesso'
            bootstrap_alerts.append({'alert_type': 'alert-success','alert_title': 'glyphicon-ok', 'alert_message':alert_msg})
        elif 'delete' in request.POST:
            for alert_detail_id in list_actions:
                AlertDetail.objects.get(pk=alert_detail_id).delete()
            if len(list_actions) == 1:
                alert_msg = 'O alerta foi excluído com sucesso'
            else:
                alert_msg = 'Os alertas foram excluídos com sucesso'
            bootstrap_alerts.append({'alert_type': 'alert-success','alert_title': 'glyphicon-ok', 'alert_message':alert_msg})
        else:
            form = AlertDetailForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                alert_id = form.cleaned_data['alert']
                #alert = Alert.objects.get(pk=alert_id)
                message = form.cleaned_data['message']
                private = form.cleaned_data['private']
                alert_detail = AlertDetail(title=title, alert=alert_id, message=message, private=private)
                alert_detail.save()
                form = AlertDetailForm(initial={'alert':pk})
                bootstrap_alerts.append({'alert_type': 'alert-success','alert_title': 'glyphicon-ok', 'alert_message':'O alerta foi cadastrado com suceso.'})
    if not request.user.is_authenticated():
        permission = 0
    else:
        permission = request.user.userorgan.user_permission
    return render(request, 'alertas/detail_alerta.html', {'alert': alert, 'mensagens': mensagens, 'form': form, 'bootstrap_alerts':bootstrap_alerts, 'permission': permission})


@login_required(login_url='/login/')
def cadastro_operacional(request):
    status = AlertStatus.objects.get(status_code=10)
    alert_organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)

    #alert_organ = request.user.userorgan.user_organ
    if request.method == 'POST':
        form = FormCadastroOperacional(request.POST)
        if form.is_valid():
            alerta = form.save(commit=False)
            status = AlertStatus.objects.get(status_code=10)
            alert_organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)
            alerta.status = status
            alerta.alert_organ = alert_organ
            alerta.save()
            return HttpResponseRedirect(reverse('listagem_operacional'))
    else:
        form = FormCadastroOperacional(initial={'status': status, 'alert_organ': alert_organ})

    context = {'form': form}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission



    return render(request,'alertas/operacional/cadastro.html',context)


@login_required(login_url='/login/')
def listagem_operacional(request):
    alertas_pendentes = Alert.objects.all().filter(status__status_code=10)
    alertas_rejeitados = Alert.objects.all().filter(status__status_code=11)
    context = {'alertas': alertas_pendentes, 'alertas_rejeitados': alertas_rejeitados}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    return render(request, 'alertas/operacional/listagem.html', context)


@login_required(login_url='/login/')
def editar_alerta_operacional(request, id):
    context = {}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    alert = get_object_or_404(Alert, pk=id, status__status_code=11)
    status = AlertStatus.objects.get(status_code=10)
    form = FormCadastroOperacional(instance=alert)
    if request.method == 'POST':
        form = FormCadastroOperacional(request.POST, instance=alert)
        if form.is_valid():
            alerta = form.save(commit=False)
            alerta.status = status
            alerta.save()
            return HttpResponseRedirect('/operacional/')

    context = {'form': form, 'alert': alert}
    return render(request,'alertas/edit.html',context)

@login_required(login_url='/login/')
def listagem_supervisor(request):
    alertas_pendentes = Alert.objects.all().filter(status__status_code=10)
    alertas_rejeitados = Alert.objects.all().filter(status__status_code=11)
    alertas_aprovados = Alert.objects.all().filter(status__status_code=20)
    alertas_arquivados = Alert.objects.all().filter(status__status_code=30)

    # se o usuario nao for admin, só mostrar alertas do seu proprio orgao
    user_organ = request.user.userorgan.user_organ.id
    if request.user.userorgan.user_permission < 3:
        alertas_pendentes = alertas_pendentes.filter(alert_organ__id=user_organ)
        alertas_rejeitados = alertas_rejeitados.filter(alert_organ__id=user_organ)
        alertas_aprovados = alertas_aprovados.filter(alert_organ__id=user_organ)
        alertas_arquivados = alertas_arquivados.filter(alert_organ__id=user_organ)

    context = {'alertas_pendentes': alertas_pendentes,
               'alertas_rejeitados': alertas_rejeitados,
               'alertas_aprovados': alertas_aprovados,
               'alertas_arquivados': alertas_arquivados
              }
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    if request.user.userorgan.user_permission < 2:
        return HttpResponseRedirect('/operacional/')
    return render(request, 'alertas/supervisor/listagem.html', context)

@login_required(login_url='/login/')
def aprovacao_alerta(request, id):
    alert = get_object_or_404(Alert, pk=id, status__status_code=10)
    context = {'alert': alert}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    return render(request, 'alertas/supervisor/aprovacao_alerta.html', context)


@login_required(login_url='/login/')
def aprovar_alerta(request, id):
    alert = get_object_or_404(Alert, pk=id, status__status_code=10)
    alert.status = AlertStatus.objects.get(status_code=20)
    alert.save()
    return HttpResponseRedirect('/supervisor/')

@login_required(login_url='/login/')
def rejeitar_alerta(request, id):
    alert = get_object_or_404(Alert, pk=id, status__status_code=10)
    alert.status = AlertStatus.objects.get(status_code=11)
    alert.save()
    return HttpResponseRedirect('/supervisor/')


@login_required(login_url='/login/')
def apagar_alerta(request, id):
    alert = get_object_or_404(Alert, pk=id, status__status_code__in=[10,11])
    alert.delete()
    return HttpResponseRedirect('/supervisor/')

@login_required(login_url='/login/')
def arquivar_alerta(request, id):
    alert = get_object_or_404(Alert, pk=id, status__status_code=20)
    alert.status = AlertStatus.objects.get(status_code=30)
    alert.save()
    return HttpResponseRedirect('/supervisor/')

@login_required(login_url='/login/')
def cadastro_mensagem_operacional(request, pk):
    alert = get_object_or_404(Alert, pk=pk)
    mensagens = AlertDetail.objects.filter(alert=alert)
    form = FormCadastroMensagemOperacional(initial={'alert':pk, 'private': True})
    bootstrap_alerts = []
    if request.method == 'POST':
        form = AlertDetailForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            alert_id = form.cleaned_data['alert']
            message = form.cleaned_data['message']
            alert_detail = AlertDetail(title=title, alert=alert_id, message=message, private=True)
            alert_detail.save()
            form = AlertDetailForm(initial={'alert':pk, 'private': True })
            bootstrap_alerts.append({'alert_type': 'alert-success','alert_title': 'glyphicon-ok', 'alert_message':'A mensagem foi cadastrada com suceso.'})
    if not request.user.is_authenticated():
        permission = 0
    else:
        permission = request.user.userorgan.user_permission
    return render(request, 'alertas/operacional/mensagem.html', {'alert': alert, 'mensagens': mensagens, 'form': form, 'bootstrap_alerts':bootstrap_alerts, 'permission': permission})

def operacional_lista_alertas_mensagem(request):
    alertas_pendentes = Alert.objects.all().filter(status__status_code=10)
    alertas_rejeitados = Alert.objects.all().filter(status__status_code=11)
    alertas_aprovados = Alert.objects.all().filter(status__status_code=20)

    # se o usuario nao for admin, só mostrar alertas do seu proprio orgao
    user_organ = request.user.userorgan.user_organ.id
    if request.user.userorgan.user_permission < 3:
        alertas_pendentes = alertas_pendentes.filter(alert_organ__id=user_organ)
        alertas_rejeitados = alertas_rejeitados.filter(alert_organ__id=user_organ)
        alertas_aprovados = alertas_aprovados.filter(alert_organ__id=user_organ)



    context = {'alertas_pendentes': alertas_pendentes,
               'alertas_rejeitados': alertas_rejeitados,
               'alertas_aprovados': alertas_aprovados
              }
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    return render(request, 'alertas/operacional/lista_mensagem.html', context)


def reporte_visitante(request):
    status = AlertStatus.objects.get(status_code=2)

    if request.method == 'POST':
        form = ReportedAlertForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            status = AlertStatus.objects.get(status_code=2)
            report.status = status
            report.save()
            return HttpResponseRedirect('/obrigado/')
    else:
        form = ReportedAlertForm(initial={'status': status})

    context = {'form': form}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    return render(request,'alertas/cadastro_visitante.html',context)

def relatos_operacional(request):
    relatos_pendentes = ReportedAlert.objects.all().filter(status__status_code=2)
    relatos_rejeitados = ReportedAlert.objects.all().filter(status__status_code=11)
    relatos_aprovados = ReportedAlert.objects.all().filter(status__status_code=20)
    context = {'relatos_pendentes': relatos_pendentes,
               'relatos_rejeitados': relatos_rejeitados,
               'relatos_aprovados': relatos_aprovados
              }
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    return render(request, 'alertas/operacional/verificar_relato.html', context)


@login_required(login_url='/login/')
def detalhe_relato(request, id):
    relato = get_object_or_404(ReportedAlert, pk=id, status__status_code=2)
    context = {'relato': relato}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    return render(request, 'alertas/operacional/detalhe_relato.html', context)


@login_required(login_url='/login/')
def rejeitar_relato(request, id):
    relato = get_object_or_404(ReportedAlert, pk=id, status__status_code=2)
    relato.status = AlertStatus.objects.get(status_code=11)
    relato.save()
    return HttpResponseRedirect('/operacional/relatos/')

@login_required(login_url='/login/')
def criar_alerta_relato(request, id):
    context = {}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    relato = get_object_or_404(ReportedAlert, pk=id, status__status_code=2)
    status = AlertStatus.objects.get(status_code=10)
    alert_organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)

    form = FormCadastroOperacional(initial={'title':relato.title, 'latitude': relato. latitude,
                                            'longitude': relato.longitude, 'radius': relato.radius,
                                            'alert_type': relato.alert_type, 'status': status,
                                            'alert_organ': alert_organ})
    if request.method == 'POST':
        form = FormCadastroOperacional(request.POST)
        if form.is_valid():
            alerta = form.save(commit=False)
            alerta.status = status
            alerta.organ = alert_organ
            alerta.save()
            relato = get_object_or_404(ReportedAlert, pk=id, status__status_code=2)
            relato.status = AlertStatus.objects.get(status_code=20)
            relato.save()
            return HttpResponseRedirect('/operacional/')

    context = {'form': form, 'relato': relato}
    return render(request,'alertas/operacional/cria_alerta_relato.html',context)

def anuncios(request):
    context = {}
    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission
    anuncios = Announcement.objects.all().filter(status__status_code=20)
    context['anuncios'] = anuncios

    return render(request,'alertas/anuncios.html',context)


def json(request):
    alertas_aprovados = Alert.objects.all().filter(status__status_code=20)
    context = {'alertas_aprovados': alertas_aprovados}
    return render(request,'alertas/json.json',context)


@login_required(login_url='/login/')
def cadastro_anuncio(request):
    try:
        id_anuncio = request.POST['id_anuncio_e']
        e_url = request.POST['url']
        e_titulo = request.POST['title']
        editar = True
    except (KeyError):
        editar = False

    if 'delete' in request.POST:
        anuncio_exclusao = get_object_or_404(Announcement, pk=request.POST['id_anuncio_d'])
        anuncio_exclusao.delete()
        return HttpResponseRedirect('/operacional/anuncios/')


    if editar:
        status = AlertStatus.objects.get(status_code=10)
        anuncio_editado = get_object_or_404(Announcement, pk=id_anuncio)
        anuncio_editado.title = e_titulo
        anuncio_editado.url = e_url
        anuncio_editado.status = status
        anuncio_editado.save()
        return HttpResponseRedirect('/operacional/anuncios/')


    context = {}
    status = AlertStatus.objects.get(status_code=10)
    announcement_organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)
    anuncios_pendentes = Announcement.objects.all().filter(status__status_code=10)
    anuncios_rejeitados = Announcement.objects.all().filter(status__status_code=11)
    context['anuncios_pendentes'] = anuncios_pendentes
    context['anuncios_rejeitados'] = anuncios_rejeitados


    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            annoucement = form.save(commit=False)

            status = AlertStatus.objects.get(status_code=10)
            organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)

            annoucement.status = status
            annoucement.organ = organ

            annoucement.save()
            return HttpResponseRedirect('/operacional/anuncios/')
    else:
        form = AnnouncementForm(initial={'status': status, 'announcement_organ': announcement_organ})
    context['form'] = form
    return render(request,'alertas/operacional/anuncio.html',context)

@login_required(login_url='/login/')
def controle_anuncio_supervisor(request):
    update = False
    deletar = False
    try:
        if 'rejeitar' in request.POST:
            update = True
            status_code = 11
        elif 'aprovar' in request.POST:
            update = True
            status_code = 20
        elif 'arquivar' in request.POST:
            update = True
            status_code = 30
        elif 'deletar' in request.POST:
            deletar = True
    except (KeyError):
        update = False
        deletar = False

    if deletar:
        anuncio_exclusao = get_object_or_404(Announcement, pk=request.POST['id_anuncio'])
        anuncio_exclusao.delete()
        return HttpResponseRedirect('/supervisor/anuncios/')

    if update:
        id_anuncio = request.POST['id_anuncio']
        status = AlertStatus.objects.get(status_code=status_code)
        anuncio = get_object_or_404(Announcement, pk=id_anuncio)
        anuncio = get_object_or_404(Announcement, pk=id_anuncio)
        anuncio.status = status
        anuncio.save()
        return HttpResponseRedirect('/supervisor/anuncios/')

    context = {}

    announcement_organ = Organ.objects.get(id=request.user.userorgan.user_organ.id)

    anuncios_pendentes = Announcement.objects.all().filter(status__status_code=10)
    anuncios_rejeitados = Announcement.objects.all().filter(status__status_code=11)
    anuncios_aprovados = Announcement.objects.all().filter(status__status_code=20)
    anuncios_arquivados = Announcement.objects.all().filter(status__status_code=30)

    if request.user.userorgan.user_permission < 3:
        anuncios_pendentes = anuncios_pendentes.filter(alert_organ__id=announcement_organ)
        anuncios_rejeitados = anuncios_rejeitados.filter(alert_organ__id=announcement_organ)
        anuncios_aprovados = anuncios_aprovados.filter(alert_organ__id=announcement_organ)
        anuncios_arquivados = anuncios_arquivados.filter(alert_organ__id=announcement_organ)

    context['anuncios_pendentes'] = anuncios_pendentes
    context['anuncios_rejeitados'] = anuncios_rejeitados
    context['anuncios_aprovados'] = anuncios_aprovados
    context['anuncios_arquivados'] = anuncios_arquivados

    if not request.user.is_authenticated():
        context['permission'] = 0
    else:
        context['permission'] = request.user.userorgan.user_permission

    return render(request,'alertas/supervisor/anuncio.html',context)
