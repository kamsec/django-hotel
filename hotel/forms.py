from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class SignUpForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    class Meta:
        model = User
        # fields = ("username", "email", "password1", "password2")
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
            group_client, _ = Group.objects.get_or_create(name='Client')
            group_client.user_set.add(user)
        return user
