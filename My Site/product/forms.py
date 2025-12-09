from dataclasses import fields
from django import forms
from matplotlib import widgets
from .models import Comments , Product
from django.forms import widgets


class Buy(forms.Form):

    def __init__(self,*args,**kwargs):
        quantity_m = kwargs.pop("quantity_m")
        PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range (1,quantity_m+1)]
        super(Buy, self).__init__(*args,**kwargs)
        self.fields['quantity'] = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
        
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)
        widgets = {
            'comment': forms.Textarea(attrs={'cols': 50, 'rows': 3 , 'style':'resize:none;'}),
        }
        # widgets={
        #     'product':forms.HiddenInput,
        #     'writer':forms.HiddenInput,
        # }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','price','available','number','description',)
        