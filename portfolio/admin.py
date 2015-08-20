# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User, Group
from portfolio.models import Project, Message, Entity

from django.forms import TextInput, ModelForm, Textarea, Select

from suit_ckeditor.widgets import CKEditorWidget
from suit_redactor.widgets import RedactorWidget
from suit.admin import SortableTabularInline, SortableModelAdmin, SortableStackedInline
from suit.widgets import SuitDateWidget, SuitSplitDateTimeWidget, EnclosedInput, LinkedSelect, AutosizedTextarea


# Inline
class EntityInline(SortableTabularInline):
    #form = EntityInlineForm
    #fields = ('title', 'description', 'image',)
    model = Entity
    extra = 0
    verbose_name_plural = 'Picture'
    exclude = ("thumbnail",)
    fields = ("image", "title")
    sortable = 'order'

class ProjectAdminForm(ModelForm):
    class Meta:
        widgets = {
        'description': RedactorWidget(editor_options={
'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic']})
        }

@admin.register(Entity)
class EntityAdmin(SortableModelAdmin):
    list_display = ('title', )
    exclude = ("thumbnail",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = ProjectAdminForm
    search_fields = ('title',)
    list_display = ('title',)
    inlines = (EntityInline,)
    sortable = 'order'


#class ProjectAdmin(admin.ModelAdmin):
#    list_display = ('title', 'image', 'thumbnail', 'date_created')
#    #fields = ('author', 'email', 'message')#, 'date_created')
#    class Meta():
#        pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'email', 'message', 'date_created')
    fields = ('author', 'email', 'message')#, 'date_created')
    class Meta():
        pass

admin.site.unregister(User)
admin.site.unregister(Group)