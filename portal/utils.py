from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from portal.models import EmailLog

def is_email_data_valid(email_data):
	return True

def is_valid_email(emails):
	try:
		is_valid = True
		for email in emails:
			validate_email(email)
	except ValidationError:
	    is_valid = False
	return is_valid

def split_and_strip(strings):
	if not strings:
		return []
	return [item.strip(' ') for item in strings.split(',') if strings != '']

def store_email_data(emails, email_type, subject):
	for email in emails:
		EmailLog.objects.create(email = email, email_type = email_type, subject = subject)