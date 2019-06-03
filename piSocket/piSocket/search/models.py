# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Search(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    class Meta:
      verbose_name_plural = "sensors"

    def __str__(self):
        return self.name

