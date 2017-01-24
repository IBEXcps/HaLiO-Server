from django.conf.urls import url, include
from rest_framework import routers
from apirest import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'houses', views.HouseViewSet)
router.register(r'nodes', views.NodeViewSet)
router.register(r'data', views.DataViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]