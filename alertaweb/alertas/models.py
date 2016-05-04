from django.db import models
from django.contrib.auth.models import User

class Organ(models.Model):
    nome_orgao = models.CharField("nome do órgão",max_length=400)
    telefone_administracao = models.CharField("telefone da administração do órgão", max_length=20)
    telefone_porta_voz = models.CharField("telefone do porta voz do órgão", max_length=20)
    endereco = models.CharField("endereço do órgão", max_length=400)
    responsavel = models.CharField("responsável pelo órgão", max_length=400)

    def __str__(self):
        return self.nome_orgao


class UserOrgan(models.Model):
    ACESSOS = ( (1,'Operacional'), (2, 'Supervisor'), (3,'Administrador'), )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_organ = models.ForeignKey(Organ)
    user_permission = models.IntegerField(choices=ACESSOS, default=1)

    def __str__(self):
        return self.user_organ.nome_orgao

class PhaseType(models.Model):
    # 1 - Prevenção
    # 2 - Resposta
    phase_type = models.CharField("fase da PNPDEC", max_length=50)

    def __str__(self):
        return self.phase_type

class AlertIcon(models.Model):
    icon_name = models.CharField("nome do ícone", max_length=100)
    icon_name_minified = models.CharField("nome do ícone pequeno", max_length=100, null=True)
    icon_url = models.URLField("url da imagem do ícone", max_length=200)
    def __str__(self):
        return self.icon_name


class AlertColor(models.Model):
    color_name = models.CharField("nome da cor", max_length=100)
    stroke_color = models.CharField("cor em hexadecimal da borda", max_length=10,default='#FF0000')
    fill_color = models.CharField("cor em hexadecimal do preenchimento",max_length=10,default='#FF0000')

    def __str__(self):
        return self.color_name



class AlertType(models.Model):
    description = models.CharField("descrição", max_length=100)
    alert_color = models.ForeignKey(AlertColor, null=True, verbose_name="cor")
    stroke_opacity = models.FloatField("opacidade da borda", default=0.8)
    fill_opacity = models.FloatField("opacidade do preenchimento", default=0.35)
    stroke_weight = models.FloatField("grossura da borda", default=2)
    phase_type = models.ForeignKey(PhaseType, verbose_name="fase relacionada")
    alert_icon = models.ForeignKey(AlertIcon, null=True, verbose_name="icon")

    def __str__(self):
        return self.description


class AlertStatus(models.Model):
    status_code = models.IntegerField("código do status", unique=True)
    status_desc = models.CharField("descrição do status", max_length=50)

    def __str__(self):
        return self.status_desc

    class Meta:
        ordering = ['status_code']


class Alert(models.Model):
    title = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_detail_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    alert_organ = models.ForeignKey(Organ)

    alert_type = models.ForeignKey(AlertType)
    status = models.ForeignKey(AlertStatus)

    def __str__(self):
        return self.title

    def get_public_detail(self):
        return self.alertdetail_set.filter(private=False)

    def ativado(self):
        return "Sim" if self.active else "Não"


class ReportedAlert(models.Model):
    title = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_detail_date = models.DateTimeField(null=True, blank=True)
    alert_organ = models.ForeignKey(Organ, null=True)
    message = models.CharField(max_length=500)
    alert_type = models.ForeignKey(AlertType)
    visitor_name = models.CharField(max_length=150)
    visitor_phone = models.CharField(max_length=20, blank=True)
    visitor_email = models.EmailField()
    status = models.ForeignKey(AlertStatus)


    def __str__(self):
        return self.title

    def get_public_detail(self):
        return self.alertdetail_set.filter(private=False)

    def ativado(self):
        return "Sim" if self.active else "Não"



class AlertDetail(models.Model):
    alert = models.ForeignKey(Alert)
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=500)
    private = models.BooleanField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    def privado(self):
        return "Sim" if self.private else "Não"

    class Meta:
        ordering = ['-last_updated']


class AlertApproval(models.Model):
    alert = models.ForeignKey(Alert)
    date_created = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(User)

    def __str__(self):
        return self.message

class Announcement(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300)
    message = models.CharField(max_length=500, blank=True)
    url = models.CharField(max_length=500)

    status = models.ForeignKey(AlertStatus)
    announcement_organ = models.ForeignKey(Organ)
