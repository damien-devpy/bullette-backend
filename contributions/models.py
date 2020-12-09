from django.db import models

class Comment(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateField(auto_now=True)

    class Meta:
        verbose_name = 'Commentaire'


class Vote(models.Model):
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    document = models.ForeignKey('documents.Document', on_delete=models.CASCADE)
    value = models.ForeignKey('contributions.VoteValue', on_delete=models.PROTECT)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'document'], name='unique_vote')
        ]

    def save(self, *args, **kwargs):
        if self.value not in self.document.votes_values.all():
            return
        else:
            super().save(*args, **kwargs)


class VoteValue(models.Model):
    value = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Types de vote'

    def __str__(self):
        return self.value