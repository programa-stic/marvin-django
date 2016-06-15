# Copyright (c) 2015, Fundacion Dr. Manuel Sadosky
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.conf.urls import patterns, url
from frontpage.views import AppDetailView, VulnDetailView, PermsListView

from frontpage import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
#    url(r'^ListaApps$', AppList.as_view()),
#    url(r'^(?P<pk>\d+)/DetalleApp$', AppDetailView.as_view(),name = "appdetail"),
    url(r'^(?P<pk>\d+)/list_sources/$', views.list_sourcefiles),
    url(r'^upload/$', views.upload_file, name='upload'),
    url(r'^error/$', views.error, name='upload'),
    url(r'^search_source/$', views.search_source),
#    url(r'^search_sourcefile/$', views.search_sourcefile),
    url(r'^search_app/$', views.search_app),
    url(r'^search_malware/$', views.detected_as_malware),
    url(r'^static_vulns/$', views.list_static_vulns),
    url(r'^static_vulns/(?P<vuln_name>[\w\_]+)/Aplicaciones/$', views.list_vulnerable_apps),
    url(r'^(?P<pk>\d+)/classes/(?P<activity_name>[\w\._/$]+)/$', views.show_activity),
    url(r'^(?P<pk>\d+)/packages/(?P<package_name>[\w\._/$]+)/$', views.show_package_sources),
    url(r'^dynamic_vulns/$', views.list_dynamic_vulns),
    url(r'^search_googleplay/$', views.search_googleplay),
    url(r'^(?P<app_id>\d+)/$', views.app, name='app'),
    url(r'^(?P<app_id>\d+)/apk/$', views.apk, name='index'),
    url(r'^(?P<app_id>\d+)/src/$', views.src, name='index'),
    url(r'^(?P<app_id>\d+)/delete/$', views.delete, name='index'),
 #   url(r'^(?P<pk>\d+)/DetalleVuln/$', VulnDetailView.as_view()),   
    url(r'^(?P<pk>\d+)/DetalleVuln/$', views.vulnDetail),   
    url(r'^Vulnerabilidades/(?P<pk>\d+)/Comentarios/$', views.addComment),   
    url(r'^Comentarios/(?P<pk>\d+)/delete/$', views.deleteComment),   
    url(r'^(?P<pk>\d+)/CheckVulns/$', views.vuln_check), 
    url(r'^GetDetails/(?P<pk>[\w\._]+)/$', views.app_details), 
    url(r'^Fetch/(?P<pk>[\w\._]+)/$', views.app_fetch_queued), 
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),  
    url(r'^ListaPermisos$', PermsListView.as_view()),
    url(r'^Permisos/(?P<pk>\d+)/Aplicaciones/$', views.appsByPermission),
    url(r'^Packages/(?P<pk>\d+)/Aplicaciones/$', views.appsByPackage),
    url(r'^Autor/(?P<pk>[\w\._ ]+)/$', views.author),
    url(r'^Codigo_fuente/(?P<pk>\d+)/$', views.source_file_contents),
    url(r'^vuln/(?P<pk>\d+)/toggleDynTest$', views.toggleDynTest),
    url(r'^verified_vulns/$', views.list_verified_vulns),  
    url(r'^enabled_vulns/$', views.list_enabled_vulns),  
)
