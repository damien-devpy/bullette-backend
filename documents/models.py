from django.db import models

class Document(models.Model):

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('documents.DocumentType', on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    changed_at = models.DateField(auto_now=True)
    end_at = models.DateField(blank=True, null=True)
    add_vote = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    comments = models.ManyToManyField('users.User', through='contributions.Comment',
                                      related_name="document_comments")
    votes = models.ManyToManyField('users.User', through='contributions.Vote',
                                   related_name="document_votes")

    def __str__(self):
        return self.title

class DocumentType(models.Model):
    type = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Types de document'

    def __str__(self):
        return self.type