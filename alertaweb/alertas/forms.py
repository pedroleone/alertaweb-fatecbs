from django import forms
from django.forms import ModelForm
from .models import Alert, AlertType, AlertDetail, ReportedAlert, Announcement


class LoginForm(forms.Form):
    login = forms.CharField(label="Login",max_length=50)
    password = forms.CharField(label="Senha",widget=forms.PasswordInput())

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        fields = ['title','latitude','longitude','radius','active','alert_type','status','alert_organ']
        widgets = {
            'radius': forms.NumberInput(attrs={'step': '10'})
        }
        labels = {
            'title': 'Título',
            'radius': 'Raio em Metros',
            'active': 'Ativo?',
            'alert_type': 'Tipo de Alerta'
        }

class FormCadastroOperacional(AlertForm):
    class Meta(AlertForm.Meta):
        widgets = {
            'status': forms.HiddenInput(),
            'alert_organ': forms.HiddenInput()
        }

class ReportedAlertForm(ModelForm):
    class Meta:
        model = ReportedAlert
        fields = ['title', 'visitor_name','visitor_phone','visitor_email','latitude','longitude','radius', 'alert_type', 'alert_organ', 'message','status']
        widgets = {
            'status': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': '10'}),
        }
        labels = {
            'title': 'Qual a sua reclamação?',
            'visitor_name': 'Nome',
            'visitor_phone': 'Telefone para Contato',
            'visitor_email': 'Email para Contato',
            'radius': 'Área da Ocorrência (em metros)',
            'alert_type': 'Tipo da ocorrência',
            'alert_organ': 'Que orgão público você sugere que verifique?',
            'message': 'Descreva a sua ocorrência'
        }

class AlertDetailForm(ModelForm):
    class Meta:
        model = AlertDetail
        fields = ['alert','title','message','private']
        widgets = {
            'alert': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': '5'}),
        }
        labels = {
            'title': 'Título',
            'message': 'Mensagem',
            'private': 'Privado',
        }

class FormCadastroMensagemOperacional(AlertDetailForm):
    class Meta(AlertDetailForm.Meta):
        widgets = {
            'alert': forms.HiddenInput(),
            'private': forms.HiddenInput(),
            'message': forms.Textarea(attrs={'rows': '5'}),
        }


class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        fields = ['title','url', 'status', 'announcement_organ']
        widgets = {
            'status': forms.HiddenInput(),
            'announcement_organ': forms.HiddenInput()
        }