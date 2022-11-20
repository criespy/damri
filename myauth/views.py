from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout

class CustomLoginView(LoginView):
    template_name = 'myauth/login.html'

redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    def logout_view(selfrequest):
        logout(request)
    template_name = 'myauth/login.html'
    next_page = 'beranda'
