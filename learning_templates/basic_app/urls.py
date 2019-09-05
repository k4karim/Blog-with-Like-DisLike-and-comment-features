from django.conf.urls import url
from basic_app import views

# SET THE NAMESPACE!
app_name = 'basic_app'

urlpatterns=[
    url(r'^$',views.post_list,name='post_list'),
    
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),

    url(r'^post/new/$',views.post_new,name='post_new'),

    url(r'^post/(?P<pk>\d+)/edit/$',views.post_edit,name='post_edit'),

    url(r'^post/(?P<pk>\d+)/delete/$',views.post_remove,name='post_remove'),

    url(r'^post/drafts/$',views.post_draft_list,name='post_draft_list'),

    url(r'^post/myposts/$',views.myposts_list,name='myposts_list'),

    url(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
    url(r'^post/(?P<pk>\d+)/unpost_publish/$',views.unpost_publish,name='unpost_publish'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    
    url(r'^comment/(?P<pk>\d+)/uncomment_approve/$', views.uncomment_approve, name='uncomment_approve'),

    url(r'^post/(?P<pk>\d+)/upvote/$', views.upvote, name='upvote'),

    url(r'^post/(?P<pk>\d+)/downvote/$', views.downvote, name='downvote'),

    url(r'^register/$',views.register,name='register'),
    
]
