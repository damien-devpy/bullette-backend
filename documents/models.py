from django.db import models

class DocumentManager(models.Manager):

    def get_document_by_id(self, pk):
        return self.get(id=pk)

    def get_all_documents(self):
        return self.all()

class Document(models.Model):

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('documents.DocumentType', on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edit_at = models.DateTimeField(auto_now=True)
    end_at = models.DateField(blank=True, null=True)
    add_vote = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    comments = models.ManyToManyField('users.User', through='contributions.Comment',
                                      related_name="document_comments")
    votes = models.ManyToManyField('users.User', through='contributions.Vote',
                                   related_name="document_votes")

    votes_values = models.ManyToManyField('contributions.VoteValue', blank=True)

    objects = models.Manager()
    documents = DocumentManager()

    def __str__(self):
        return self.title

    def get_votes_details(self):
        votes = {}
        for value in self.votes_values.all():
            votes[value.value] = self.votes.through.objects.filter(value=value).count()
        return votes

class DocumentType(models.Model):
    type = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Types de document'

    def __str__(self):
        return self.type