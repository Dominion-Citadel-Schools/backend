from django.apps import AppConfig


class AdmissionConfig(AppConfig):
    name = 'admission'

    def ready(self):
     import admission.signals