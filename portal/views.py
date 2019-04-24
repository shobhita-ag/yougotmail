# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

import json
import csv

from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.views.generic import TemplateView
from portal.utils import is_email_data_valid
from portal.utils import is_valid_email
from portal.utils import split_and_strip
from portal.utils import store_email_data
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HomePage(APIView):
	def get(self, request):
		return render(request, template_name='index.html')

class SendEmail(APIView):
	def post(self, request):
		csvfile = request.FILES.get('file', None)
		email_data = request.data.get('email_data', None)

		#TODO: do we have to validate email data here?
		if not email_data:
			return Response({"response": "Invalid Email Data"}, status=status.HTTP_400_BAD_REQUEST)

		#validating csvfile
		if csvfile:
			if not csvfile.name.endswith('.csv'):
				return Response({"response": "Uploaded file is not CSV"}, status=status.HTTP_400_BAD_REQUEST)
			if csvfile.size > 1048576:
				return Response({"response": "Uploaded file is more than 1MB"}, status=status.HTTP_400_BAD_REQUEST)

		#converting json string to json object
		email_data = json.loads(email_data)

		#splitting comma separated values & stripping whitespaces from the list of strings
		to_list =  split_and_strip(email_data.get('to', ''))
		bcc_list = split_and_strip(email_data.get('bcc', ''))
		cc_list = split_and_strip(email_data.get('cc', ''))
		subject = email_data.get('subject', '')
		body = email_data.get('body', '')

		#parsing csvfile
		if csvfile:
			file_reader = csv.reader(csvfile, delimiter=',')
			for row in file_reader:
				to_list.append(row[0])

		if not (is_valid_email(to_list) and is_valid_email(cc_list) and is_valid_email(bcc_list)):
			return Response({"response": "Invalid Email Address"}, status=status.HTTP_400_BAD_REQUEST)

		try:
			email = EmailMessage(
			    subject,
			    body,
			    settings.EMAIL_HOST_USER,
			    to_list
			)
			if cc_list:
				email.cc = cc_list

			if bcc_list:
				email.bcc = bcc_list

			#for debugging - remove
			print(email.message())

			is_success = email.send(fail_silently=False)
			if not is_success:
				return Response({"response": "Error occured while sending emails"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

			#if successful, store the emails in DB
			store_email_data(to_list, 1, subject)
			store_email_data(cc_list, 2, subject)
			store_email_data(bcc_list, 3, subject)

		except Exception as e:
			print("Exception while sending emails:" + str(e))
			return Response({"response": "Error occured while sending emails"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		return Response({"response": "Sent successfully"}, status=status.HTTP_200_OK)		



