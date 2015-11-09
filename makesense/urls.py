"""makesense URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('makesense.views',
    url(r'^$','home'),
    url(r'^lexicon/$','lexicon'),
    url(r'^chapter/(?P<chapter_num>\d+)/(?P<slug>[\w-]+)/$','chapter'),
    url(r'^chapter/(?P<chapter_num>\d+)/page/(?P<page_num>\d+)/(?P<slug>[\w-]+)/$','page'),
    url(r'^page/(?P<page_num>\d+)/(?P<slug>[\w-]+)/$','page_redirect'),
    url(r'^term/(?P<word_type_slug>\w+)/(?P<term_slug>[\w-]+)/$','term'),
    url(r'^search/$','search'),
    url(r'^dedication/$','dedication'),
    url(r'^introduction/$','introduction'),
    url(r'^about/$','about'),
    url(r'^acknowledgements','acknowledgements'),
    url(r'^resources/$','resources'),
    url(r'^djax/',include('djax.urls')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     url(r'^admin/', include(admin.site.urls)),
# ]
