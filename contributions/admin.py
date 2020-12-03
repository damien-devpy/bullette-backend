from django.contrib import admin
from .models import Comment, Vote, VoteValue

admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(VoteValue)
