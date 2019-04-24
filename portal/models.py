# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import localtime
from model_utils.models import TimeStampedModel

# Create your models here.
class EmailLog(TimeStampedModel):
	EMAIL_TYPES = (
		(1, "to"),
		(2, "cc"),
		(3, "bcc"),
	)
	email = models.CharField(max_length=254)
	email_type = models.IntegerField(choices=EMAIL_TYPES, default=1)
	subject = models.TextField(blank=True)

	def __str__(self):
		return "Email:[{}] on Date:[{}] - Subject:[{}]".format(self.email, localtime(self.created), self.subject)
