"""
mixin definition
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect


class LoggedOutOnlyView(UserPassesTestMixin):

    """ mixin to prevent users to view certain pages if they are not logged out """

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect("music:main")
