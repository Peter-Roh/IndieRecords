from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.shortcuts import reverse


class LoggedOutOnlyView(UserPassesTestMixin):

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("music:main")
