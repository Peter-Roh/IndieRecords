'''
things that help social logins
'''
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from users.models import User


class CustomAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):

        if sociallogin.user.username:
            return
        if request.user and request.user.is_authenticated:
            try:
                login_user = User.objects.get(username=request.user)
                sociallogin.connect(request, login_user)
            except User.DoesNotExist:
                pass

    def save_user(self, request, sociallogin, form):

        user = super(CustomAccountAdapter, self).save_user(request, sociallogin, form)

        social_app_name = sociallogin.account.provider.upper()

        if social_app_name == "GOOGLE":
            user.profile_url = user.socialaccount_set.all()[0].extra_data['picture']
            user.login_method = User.LOGIN_GOOGLE
            user.save()

        return user
