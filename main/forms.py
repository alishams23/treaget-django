from django import forms

from .models import contact,BuyStudio,OrderUser

class PostFormContact(forms.ModelForm):

    class Meta:
        model = contact
        fields = '__all__'

# class ProductFormContact(forms.Form):
#     name = forms.CharField(max_length=100)
#     body = forms.CharField(widget=forms.Textarea)
#     number = forms.CharField(max_length=15)


class ProductFormContact(forms.ModelForm):

    class Meta:
        model = BuyStudio
        fields = '__all__'

class OrderUserForm(forms.ModelForm):

    class Meta:
        model = OrderUser
        fields = '__all__'
