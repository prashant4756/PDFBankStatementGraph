# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render
from .models import Document
from transactions.models import Transaction
from .forms import DocumentForm
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from tabula import read_pdf
from tabula import convert_into
import csv
import pyPdf
import os 
# Create your views here.

####################################################################
#default page and link to upload pdf
####################################################################
def home(request):
	documents = Document.objects.all().order_by('-uploaded_at')
	return render(request, 'core/home.html', { 'documents': documents })

def model_form_upload(request):
	print "inside model form upload"
	print request.method
	if request.method == 'POST':
		form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
        	form.save()
        	#
        	# Code to process pdf doc
        	#
        	document_uploaded = Document.objects.latest('uploaded_at')
        	if document_uploaded is not None:
        		print document_uploaded.document
        		save_transactions(document_uploaded)
        	# done processing
        	return redirect('home')
	else:
		form = DocumentForm()
        return render(request, 'core/model_form.html', { 'form': form})


def my_link_view(request):
	print "inside my link view"
	form = DocumentForm()
	return render(request,'core/model_form.html',{'form' : form})


def save_transactions(document_uploaded):
	transaction_doc = document_uploaded
	doc_location_name = settings.MEDIA_ROOT+"/" +str(document_uploaded.document)
	reader = pyPdf.PdfFileReader(open(doc_location_name, mode='rb' ))
	n = reader.getNumPages() 
	print n
	for i in range(n):
		convert_into(doc_location_name,"out.csv",output_format="csv", pages = str(i+1))
		with open('out.csv') as csvfile:
			reader = csv.DictReader(csvfile)
			count = 0;
			for row in reader:
				row_balance = row['Balance']
				if row_balance is not None and row_balance != "":
					count+=1
					print str(count)+" and "+ str(row_balance)
					transaction_date = str(row['Txn Date'])
					transaction_date = format_date(transaction_date)
					print transaction_date
					debit = row['Debit']
					debit = format_currency(debit)
					print debit
					credit = row['Credit']
					credit = format_currency(credit)
					print credit
					balance = row_balance;
					balance = format_currency(balance)
					print balance
					# transaction =  Transaction(transaction_doc,transaction_date,debit,credit,balance)
					create_transaction(document_uploaded,transaction_date,debit,credit,balance)
					
					print "Transaction Inserted..!"

def format_currency(currency):
	if currency == "":
		currency = 0.00
	return float((str(currency)).replace(',',''))
change_val = True
year = ""
def format_date(date):
	global change_val
	global year
	print date
	parts = date.split()
	parts_length = len(parts)

	if parts_length == 3 and change_val is True:
		year = parts[2]
		change_val = False
	elif parts_length == 3 and change_val is False and int(year) < int(parts[2]):
		year = parts[2]

	if parts_length == 2:
		date = date +" "+year
		print "updated date "+ date
	return date


def create_transaction(document_uploaded,transaction_date,debit,credit,balance):
	transaction = Transaction(transaction_doc = document_uploaded)
	print transaction
	print "saving now...."
	transaction.transaction_date = transaction_date
	transaction.debit = debit
	transaction.credit = credit
	transaction.balance = balance

	print transaction
	transaction.save()


###############################################################################
#Dashboard related
###############################################################################

def for_dashboard(request):
	print "inside dashboard"
	if request.method == "POST":
		document_obj_id = request.POST['doc_obj_id']
		print "printing document obj id"
		print document_obj_id
		document = get_document_by_id(document_obj_id)
		if document is not None:
			print document.document
			debit_dict,credit_dict = get_analytics(document)
		else:
			print "Document not in database"
	return render(request,'core/dashboard.html',{'debit_dict':debit_dict, 'credit_dict':credit_dict})


def get_analytics(document):
	# print document
	debit_dict = {}
	credit_dict = {}
	transactions = Transaction.objects.filter(transaction_doc=document)
	print "printing transactions now"
	for transaction in transactions:
		print transaction.transaction_doc.document
		print transaction.transaction_date
		mt_yr = month_year(transaction.transaction_date)
		print mt_yr
		print transaction.debit
		print transaction.credit
		print transaction.balance
		
		if debit_dict.has_key(mt_yr):
			debit_dict[mt_yr] = debit_dict[mt_yr] + transaction.debit
		else:
			debit_dict[mt_yr] = transaction.debit

		if credit_dict.has_key(mt_yr):
			credit_dict[mt_yr] = credit_dict[mt_yr] + transaction.credit
		else:
			credit_dict[mt_yr] = transaction.credit

	print debit_dict
	print credit_dict
	return debit_dict,credit_dict

def month_year(date):
	parts = date.split()
	return parts[1]+"_"+parts[2]	

def get_document_by_id(document_obj_id):
	document = Document.objects.get(pk=document_obj_id)
	if document is not None:
		return document