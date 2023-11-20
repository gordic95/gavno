from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class AccountSignupForm(SignupForm):
    def save(self, request):
        user = super(AccountSignupForm, self).save(request)
        account_group = Group.objects.get(name='account')
        account_group.user_set.add(user)
        return user

