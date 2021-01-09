from django.contrib import admin
from django.db import models as django_models

from django_json_widget.widgets import JSONEditorWidget

from randsense import models


@admin.register(models.GenericWord)
class GenericWordAdmin(admin.ModelAdmin):
    list_display = ["base", "category"]
    list_filter = ["category"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Noun)
class NounAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}


@admin.register(models.Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ["base"]
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


@admin.register(models.SpecialWord)
class SpecialWordAdmin(admin.ModelAdmin):
    list_display = ["base"]
    search_fields = ["base"]
    formfield_overrides = {django_models.JSONField: {"widget": JSONEditorWidget}}
