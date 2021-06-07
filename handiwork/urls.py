"""
handiwork URL Configuration
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
from django.views import defaults as default_views
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include(('users.urls', 'users'), namespace='users')),
    path('workers/', include(('profession.worker_urls', 'profession'), namespace='workers')),
    path('clients/', include(('profession.client_urls', 'profession'), namespace='clients')),

    # examples for decorators and permissions
    # path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    # path('app_or_model/', permission_required('app_or_model.can_engage')(TheView.as_view())),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [
      re_path(r'^__debug__/', include(debug_toolbar.urls)),
      re_path(r'^404/$', default_views.page_not_found,
              kwargs={'exception': Exception("Page not Found")}),
      re_path(r'^500/$', default_views.server_error),
      re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception}),
      re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception})
                  ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
