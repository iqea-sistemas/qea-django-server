from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenRefreshView)
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *

router= routers.DefaultRouter()
router.register(r'iqea_users', IqeaUserView, 'users')
router.register(r'allProjects', adminProjectsView, 'allProjects')



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('docs/', include_docs_urls(title='Estimador API')),
    path('api/v1/projects/', ProjectsView, name='projects_by_user'),
    path('api/v1/projects/<cotizacion_id>/', ProjectsView, name='projects_by_user'),
    path('api/v1/projects/precio_estimado/<str:tipo_sistema>/<int:f>/', PrecioEstimado.as_view(), name='precio_estimado'),
    # path('api/v1/allProjects/', adminProjectsView.as_view(), name='all_projects'),
    path('api/v1/system-categories/', SystemCategoryList.as_view(), name='system-category-list'),
    path('api/v1/precios-referencia/', PreciosRefenciaList.as_view(), name='precios-referencia'),
    path('api/v1/precios-referencia/<int:pk>', PreciosRefenciaDetail.as_view(), name='precios-referencia-detail'),


    path('api/token/', MyTokenObteainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/register/', RegisterUserView.as_view(), name='register_user'),



]
