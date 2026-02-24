from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('team/', include('team.urls')),
    path('blog/', include('blog.urls')),
]
