from django.contrib import admin

from .models import Document, DocumentType

admin.site.register(Document)
admin.site.register(DocumentType)
