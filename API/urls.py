from rest_framework.routers import DefaultRouter
from .views import (
    OrganisationViewSet,
    AdminViewSet,
    EnqueteViewSet,
    EnqueteurViewSet,
    EnqueteAssignmentViewSet,
)

router = DefaultRouter()
router.register('organisations', OrganisationViewSet, basename='organisation')
router.register('admins', AdminViewSet, basename='admin')
router.register('enquetes', EnqueteViewSet, basename='enquete')
router.register('enqueteurs', EnqueteurViewSet, basename='enqueteur')
router.register('assignments', EnqueteAssignmentViewSet, basename='assignment')

urlpatterns = router.urls
