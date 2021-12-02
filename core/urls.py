from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('events/', include('events.urls', namespace='events')),
    path('', include('website.urls', namespace='website')),

    path('api/accounts/', include('accounts.api.urls',
                                  namespace='api_account')),
    path('api/events/', include('events.api.urls',
                                namespace='api_events')),
    path('api-auth/', include('rest_framework.urls')),
]
if settings.DEBUG:
  urlpatterns += static(settings.STATIC_URL,
                        document_root=settings.STATIC_ROOT)
  urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
