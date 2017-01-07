from . import views
from django.conf.urls import url,include
from django.contrib import admin

app_name = 'brmadmin'

urlpatterns = [
	url(r'^login/$',views.signIn,name='signIn'),
	url(r'^logout/$',views.signOut,name='signOut'),
	url(r'^register/$', views.register , name = 'register'),
	url(r'^$',views.branchAndYear.as_view(),name='index'),
	url(r'^(?P<pk>[0-9]+)/$', views.detailsBranchAndYear.as_view() , name = 'detail'),
	url(r'^update/$',views.update,name='update'),
	url(r'^userVerification/$',views.userVerification,name='userVerification'),
	url(r'^course/add/$',views.CourseAdd.as_view(),name='addCourse'),
	url(r'^course/(?P<pk>[0-9]+)/delete/$',views.CourseDelete.as_view(),name='deleteCourse'),
	url(r'^subject/add/$',views.SubjectAdd.as_view(),name='addSubject'),
	url(r'^subject/(?P<pk>[0-9]+)/delete/$',views.SubjectDelete.as_view(),name='deleteSubject'),
	url(r'^verify/(?P<id>[0-9]+)/$',views.verify,name='verify'),
	url(r'^block/(?P<id>[0-9]+)/$',views.block,name='block'),
	url(r'^userBlock/$',views.userBlock,name='userBlock'),
	url(r'^(?P<id>[0-9]+)/(?P<pk>[0-9]+)$',views.detailSubject,name='detailSubject'),
	url(r'^chapter/add/$',views.chapterAdd.as_view(),name='addChapter'),
	url(r'^chapter/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/delete/$',views.chapterDelete.as_view(),name='deleteChapter'),
]