from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from app.viewsets import TreeViewSet, NodeViewSet

router = DefaultRouter()
router.register(r'trees', TreeViewSet)
router.register(r'nodes', NodeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
