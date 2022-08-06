from cgitb import handler
from django.urls import URLPattern, path

from memo import views

urlpatterns = [
    path("", views.top, name = 'top'),
    path("new/", views.memo_new, name = "memo_new"),
    path("<int:memo_id>/edit/", views.memo_edit, name = "memo_edit"),
    path("<int:memo_id>/", views.memo_detail, name = "memo_detail"),
]

handler404 = 'memo.views.handlar404'