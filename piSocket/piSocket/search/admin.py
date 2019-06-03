# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Search

class SearchAdmin(admin.ModelAdmin):
	list_display = ("name", "state",)

admin.site.register(Search, SearchAdmin)

# Register your models here.
