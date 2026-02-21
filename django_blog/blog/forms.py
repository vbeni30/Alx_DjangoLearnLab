from django import forms
from .models import Post, Tag


class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        tags_input = self.cleaned_data.get('tags')
        if tags_input:
            tag_names = [t.strip().lower() for t in tags_input.split(',')]
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)

        return instance