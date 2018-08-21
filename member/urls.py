from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('로그인/', auth_views.login, {'template_name':'member/login.html'}),
	path('로그아웃/', auth_views.logout, {'next_page' : '/'}),
	path('회원/', views.memberlist, name='memlist'),
	path('회원/<str:field>/<str:order>/', views.memberlist_order),
	path('회원/<int:id>/', views.memberinfo),
	path('회원/등록/', views.register),
	path('가입/', views.signup),
	path('가입완료/', views.signup_done, name='signup_done'),
	path('삭제/<int:id>/', views.memberdel),
]