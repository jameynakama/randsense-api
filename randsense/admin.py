from django.contrib import admin
from django.db import models as django_models

from django_json_widget.widgets import JSONEditorWidget

from randsense import models


@admin.register(models.Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ["base", "category"]
    list_filter = ["category"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}
