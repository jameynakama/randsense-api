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


@admin.register(models.GenericWord)
class GenericWordAdmin(admin.ModelAdmin):
    list_display = ["base", "category"]
    list_filter = ["category"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Noun)
class NounAdmin(admin.ModelAdmin):
    list_display = ["base", "rank"]
    list_editable = ["rank"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ["base", "rank"]
    list_editable = ["rank"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ["base", "rank"]
    list_editable = ["rank"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Adverb)
class AdverbAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Pronoun)
class PronounAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Auxiliary)
class AuxiliaryAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Preposition)
class SpecialWordAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Conjunction)
class SpecialWordAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.SpecialWord)
class SpecialWordAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Determiner)
class DeterminerAdmin(admin.ModelAdmin):
    list_display = ["base", "active"]
    search_fields = ["base"]
    list_editable = ["active"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Modal)
class ModalAdmin(admin.ModelAdmin):
    list_display = ["base"]
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
