from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from TaskApp import views
from TaskApp.views import *


router = routers.DefaultRouter()
# router = routers.SimpleRouter()


router.register(r'task', TaskViewSet, base_name='TaskView')
router.register(r'groups', views.GroupViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'due_task', views.DueTaskViewSet)
# router.register(r'completed_task', views.CompletedTaskViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^register/$', views.CreateUserView.as_view(), name='user'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', admin.site.urls),

]
