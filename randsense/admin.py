from django.contrib import admin
from django.db import models as django_models

from django_json_widget.widgets import JSONEditorWidget

from randsense import models


@admin.register(models.Sentence)
class SentenceAdmin(admin.ModelAdmin):
    list_display = ["pk", "sentence", "incorrect_votes"]
    sortable_by = ["incorrect_votes"]
    list_editable = ["incorrect_votes"]

    def sentence(self, instance):
        return instance.inflected


@admin.register(models.Adverb)
@admin.register(models.Adjective)
@admin.register(models.Auxiliary)
@admin.register(models.Conjunction)
@admin.register(models.Determiner)
@admin.register(models.GenericWord)
@admin.register(models.Modal)
@admin.register(models.Noun)
@admin.register(models.Preposition)
@admin.register(models.Pronoun)
@admin.register(models.SpecialWord)
@admin.register(models.Verb)
class WordAdmin(admin.ModelAdmin):
    list_display = ["base", "active", "removal_votes", "rank"]
    list_editable = ["active", "removal_votes", "rank"]
    list_filter = ["active"]
    sortable_by = ["removal_votes", "rank"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


class FrequencySettingsInline(admin.StackedInline):
    model = models.FrequencySettings
    max_num = 1


@admin.register(models.ApiSettings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [FrequencySettingsInline]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}

    def name(self, obj):
        return "Click to edit"
