# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from BankStatementApp.models import Document
# Create your models here.

class Transaction(models.Model):
	transaction_doc = models.ForeignKey(Document)
	transaction_date = models.CharField(max_length=255, blank = False)
	debit = models.DecimalField(max_digits=10, decimal_places=2)
	credit = models.DecimalField(max_digits=10, decimal_places=2)
	balance = models.DecimalField(max_digits=10, decimal_places=2)