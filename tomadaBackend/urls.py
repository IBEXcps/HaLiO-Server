from django.conf.urls import url, include
from rest_framework import routers
from apirest import views
from django.conf.urls import url
from django.contrib import admin


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
    url(r'^admin/', admin.site.urls),
    url(r'^dash$', views.index, name='index'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^stats_setup/$', views.stats_setup),
    url(r'^stats_update/$', views.stats_update),
    url(r'^switchnode/(?P<node_id>\d+)/(?P<state>(true|false))/$', views.toggle_node, name='last data'),
]