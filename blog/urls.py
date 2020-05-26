from . import views
from django.urls import path

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('blog/comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
	path('blog/drafts/', views.post_draft_list, name='post_draft_list'),
	path('blog/post/<int:pk>/', views.post_detail, name='post_detail'),
	path('blog/post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
	path('blog/post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('blog/post/<int:pk>/publish/', views.post_publish, name='post_publish'),
	path('blog/post/<int:pk>/remove/', views.post_remove, name='post_remove'),	
	path('blog/post/new/', views.post_new, name='post_new'),
	path('cv/', views.cvs, name='cvs'),
	path('cv/<int:pk>/', views.cv, name='cv'),
	path('cv/none/', views.cv_none, name='cv_none'),
	path('cv/new/', views.cv_new, name='cv_new'),
	path('cv/<int:pk>/edit/', views.cv_edit, name='cv_edit'),
	path('cv/<int:pk>/remove/', views.cv_remove, name='cv_remove'),
	path('cvs/edit/', views.cvs_edit, name='cvs_edit')
]
