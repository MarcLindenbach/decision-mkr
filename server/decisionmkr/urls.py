from django.contrib import admin
from django.conf.urls import url, include
from app.viewsets import DecisionTreeViewSet, DecisionNodeViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'decisiontrees', DecisionTreeViewSet)
router.register(r'decisionnodes', DecisionNodeViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
