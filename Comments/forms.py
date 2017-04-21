from django import forms
from Comments.models import Comment

class CommentForm(forms.models.ModelForm):

    class Meta:
        model=Comment
        fields=['text']
        widgets={
            'text': forms.Textarea(attrs={
                "rows": "4",
                "cols": "25"
            })
        }

    def save(self, author):
        data=self.cleaned_data
        comment=Comment.objects.create(text=data['text'], author=author)
        return comment
