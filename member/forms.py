from django import forms
from django.forms import EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Member

class RegistForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'gender', 'birthday', 'homeplace', 'workplace', 'favorite', 'introduction', 'joindate', 'recentdate']
        labels = {
            'name': '이름',
            'gender': '성별',
            'birthday': '생일',
            'homeplace': '거주지',
            'workplace': '직장',
            'favorite': '좋아하는 영화',
            'introduction':'자기소개',
            'joindate':'가입일',
            'recentdate':'최근활동',
        }
    def __init__(self, *args, **kwargs):
        super(RegistForm, self).__init__(*args, **kwargs)
        self.fields['birthday'].required = False
        self.fields['homeplace'].required = False
        self.fields['workplace'].required = False
        self.fields['favorite'].required = False
        self.fields['introduction'].required = False

class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="이름")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label="이메일")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['password1', 'password2']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'email',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        labels = {
            "username" : "아이디",
        }