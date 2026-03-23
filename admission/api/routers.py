from rest_framework.routers import DefaultRouter
from .viewset.admission_form_viewset import AdmissionFormViewSet
from .viewset.admission_upload_document import AdmissionDocumentViewSet
from .viewset.admission_viewset import AdmissionViewSet

router_admission = DefaultRouter()
router_admission.register("", AdmissionViewSet, basename="admissions")
router_admission.register("forms", AdmissionFormViewSet, basename="forms")
router_admission.register("documents", AdmissionDocumentViewSet, basename="documents")

urlpatterns = router_admission.urls