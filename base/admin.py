from django.contrib import admin
from .models import *
from node.models import Node_block
# Register your models here.
admin.site.register(Profile)

@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
 list_display = ('profile','age','cash_required','cash_received','sort_factor','completed','documents','category','text_area')

@admin.register(Payment)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('sender_profile', 'receiver_profile', 'cash', 'date_created',
                    'post')

@admin.register(Block)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'cash', 'date_created',
                    'current_hash', 'previous_hash', 'nonce')


@admin.register(Node_block)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'cash', 'date_created',
                    'current_hash', 'previous_hash', 'nonce')