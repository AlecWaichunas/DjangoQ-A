"""Website URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
# from django.contrib.sitemaps.views import sitemap
# from django.contrib.sitemaps import GenericSitemap
from App.models import *
#from App.

# info_dict = {
#     'queryset': Question.objects.all(),
#     # 'class': UserDefinedClass.objects.all(),
#     # 'discussion': Discussion.objects.all(),
#     # 'school': School.objects.all(),
# }

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'App.views.index_view', name='index'),
    url(r'^terms_of_service$', 'App.views.terms_of_service', name='terms_of_service'),
    
    # Profile URLS
    url(r'^login/$', 'App.views.login_view', name='login'),
    url(r'^logout/$', 'App.views.logout_view', name='logout'),
    url(r'^profile/(?P<messages_show>\d+)$', 'App.views.profile_view', name='profile'),
    url(r'^register/$', 'App.views.register', name='register'),
    url(r'^notification/(?P<notification_id>\d+)/$', 'App.views.redirect_notifications', name='redirect_notifications'),
    url(r'^forgot_password/$', 'App.views.forgot_password', name='forgot_password'),
    url(r'^reset_password/(?P<url_code>[\w-]+)/$', 'App.views.reset_password', name='reset_password'),
    url(r'^confirm_account/(?P<url_code>[\w-]+)/$', 'App.views.confirm_account', name='confirm_account'),
    url(r'^confirm_class/(?P<url_code>[\w-]+)/$', 'App.views.confirm_class_creation', name='confirm_class'),
    url(r'^api/get_schools/', 'App.views.school_autocomplete', name='get_schools'),

    # Class URLS ?P<slug>[\w-]+
    url(r'^classes/$', 'App.views.classes', name='classes'),
    url(r'^create_class/$', 'App.views.create_class_view', name='class_registration'),
    url(r'^c/(?P<class_id>\d+)/$', 'App.views.view_single_class', name='class_view'),
    url(r'^join_private/(?P<class_id>\d+)/(?P<class_code>[\w-]+)/$', 'App.views.join_private_class', name='join_private_class'),
    url(r'^join_public/(?P<class_id>\d+)/$', 'App.views.join_public_class', name='join_public_class'),
    
    # Questions and Answers URLS
    url(r'^c/(?P<class_id>\d+)/ask_question/$', 'App.views.add_question', name='ask_question'),
    url(r'^c/(?P<class_id>\d+)/q/(?P<question_id>\d+)/$', 'App.views.view_single_question', name='view_single_question'),
    ### url(r'^c/(?P<class_id>\d+)/q/(?P<question_id>\d+)/add_answer/$', 'App.views.add_answer', name='add_answer'),
    url(r'^c/(?P<class_id>\d+)/q/(?P<question_id>\d+)/vote_question/$', 'App.views.vote_question', name='vote_question'),
    url(r'^a/(?P<answer_id>\d+)/q/(?P<question_id>\d+)/vote_answer/(?P<positive>\d+)/$', 'App.views.vote_answer', name='vote_answer'),
    url(r'^c/(?P<class_id>\d+)/create_discussion/$', 'App.views.create_discussion', name='create_discussion'),
    url(r'^c/(?P<class_id>\d+)/d/(?P<discussion_id>\d+)/$', 'App.views.view_single_discussion', name='view_single_discussion'),
    
    # School
    url(r'^s/(?P<school_id>\d+)/$', 'App.views.view_single_school', name='view_single_school'),
    
    url(r'^search/$', 'App.views.search_view', name='search'),
    # url(r'^invite/(?P<class_id>\d+)/$', 'App.views.invite', name='invite_to_class'),
    url(r'^send_invite/(?P<class_id>\d+)/(?P<user_id>\d+)/$', 'App.views.send_user_invite', name='send_invite'),
    url(r'^accept_invite/(?P<class_id>\d+)/(?P<user_id>\d+)/$', 'App.views.accept_invite', name='accept_invite'),
    url(r'^c/(?P<class_id>\d+)/post_assignment/$', 'App.views.post_assignment', name='post_assignment'),
    
    # Testing ajax stuff
    url(r'^ajax/$', 'App.views.ajax_page', name='ajax_test'),
    url(r'^ajax_post/$', 'App.views.ajax_post_page', name='ajax_post_page'),
    
    # url(r'^ajax_page/$', 'App.views.ajax_page', name='ajax_page'),
    # url(r'^create_post/$', 'App.views.create_post', name='create_post'),
    # url(r'^sitemap\.xml$', sitemap,
    #     {'sitemaps': {'App': GenericSitemap(info_dict, priority=0.6)}},
    #     name='django.contrib.sitemaps.views.sitemap'),

]
