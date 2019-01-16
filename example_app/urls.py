from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import BasicQuestionnaireView


urlpatterns = [
    url(r'^questionnaire/(?P<pk>[0-9]+)/$', BasicQuestionnaireView.as_view(), name='basic_questionnaire_form'),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
