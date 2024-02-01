from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (TokenRefreshView)
from rest_framework_simplejwt.views import TokenVerifyView

router= routers.DefaultRouter()
router.register(r'iqea_users', IqeaUserView, 'users')
router.register(r'projects', ProjectsView, 'projects')



urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('docs/', include_docs_urls(title='Estimador API')),

    path('api/token/', MyTokenObteainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
