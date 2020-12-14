from django.db import models

class DocumentManager(models.Manager):

    def get_document_by_id(self, pk):
        """Get a specific document by id.

        Returns:
            Instance of Document model.
        """
        return self.get(id=pk)

    def get_all_documents(self):
        """Get all existing documents.

        Returns:
            Queryset containing all documents.
        """
        return self.all()

class Document(models.Model):
    """Document model.

    All publications of the plateform are document model.

    Attributes:
        author (User): Author of the document.
        type (DocumentType): Type of document.
        title (string): Title of the document.
        content (string): Content of the document.
        created_at (datetime): Creation of the document.
        edit_at (datetime): As the document been updated and when.
        add_vote (bool): Should the document propose votes.
        is_locked (bool): Is the document is_locked. Close to votes and comments.

        comments (User): All comments that have been made regarding this document.
        votes (User): All votes that have been made regarding this document.
        votes_values (VoteValue): All possible votes values for this document.
    """

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('documents.DocumentType', on_delete=models.PROTECT)
    title = models.CharField(max_length=256)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edit_at = models.DateTimeField(auto_now=True)
    end_at = models.DateField(blank=True, null=True)
    add_vote = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)

    comments = models.ManyToManyField('users.User', through='contributions.Comment',
                                      related_name="document_comments")
    votes = models.ManyToManyField('users.User', through='contributions.Vote',
                                   related_name="document_votes")

    votes_values = models.ManyToManyField('contributions.VoteValue', blank=True)

    objects = models.Manager()
    documents = DocumentManager()

    def __str__(self):
        return self.title

    def get_votes_values(self):
        """Get all possible votes values for this document.

        Returns:

            Queryset containing all possible votes values for this document.
        """
        return self.votes_values.all()

    def get_votes_details(self, value):
        """Get how much votes for this document regarding the value asked.

        Args:
            value (int): Primary key of the value asked

        Returns:
            Count for how many votes for this document regarding the value.
        """

        return self.votes.through.objects.filter(document__id=self.id, value=value).count()


    def get_comments(self):
        """Get all comments for this document.

        Returns:
            Queryset containing all comments for this document.
        """
        return self.comments.through.objects.filter(document__id=self.id)

    def get_comments_count(self):
        """Get how much comment exist for this document.

        Returns:
            Count for how many comments exist for this document.

        """

        return self.get_comments().count()

class DocumentType(models.Model):
    type = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'Types de document'

    def __str__(self):
        return self.type