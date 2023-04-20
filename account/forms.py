from django import forms
from main.models import Picture, Timeline, SafePayment, Dispute, Request, Accept, Trello, SubsetTrello
from .models import User
from profile_items.models import Services

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = '__all__'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image', 'bio', 'category')


class UserAddForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'category','ServiceProvider',"phone_number")


# class ServiceForm(forms.ModelForm):
#     class Meta:
#         model = Services
#         fields = '__all__'


class SafePaymentForm(forms.ModelForm):
    class Meta:
        model = SafePayment
        fields = '__all__'


class DisputeForm(forms.ModelForm):
    class Meta:
        model = Dispute
        fields = '__all__'


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = '__all__'


class AcceptForm(forms.ModelForm):
    class Meta:
        model = Accept
        fields = '__all__'


class TrelloForm(forms.ModelForm):
    class Meta:
        model = Trello
        fields = '__all__'


class SubsetTrelloForm(forms.ModelForm):
    class Meta:
        model = SubsetTrello
        fields = '__all__'