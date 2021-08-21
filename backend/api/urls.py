from django.urls import include, path

from . import views

app_name = "api"
urlpatterns = [
    path("create", views.BoardCreateApiView.as_view(), name="create_room"),
    path('detail/<int:pk>', views.BoardRetrieveApiView.as_view()),
]
