from django import forms

#定义评论的modelform
from comments.models import Comment


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields =['name','email','url','content']








