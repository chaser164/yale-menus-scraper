#user_app.urls
from django.urls import path
from .views import Sign_up, Log_in, Log_out, All_users, A_user, Validate, Resend

urlpatterns = [
    path('signup/', Sign_up.as_view(), name='signup'),
    path("login/", Log_in.as_view(), name="login"),
    path("logout/", Log_out.as_view(), name="logout"),
    path("", All_users.as_view(), name="all users"),
    path("me/", A_user.as_view(), name="my info"),
    path("<int:userid>/", A_user.as_view(), name="a user"),
    path("validate/", Validate.as_view(), name="validation"),
    path("resend/", Resend.as_view(), name="resend"),
]