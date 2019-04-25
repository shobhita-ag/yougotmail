from __future__ import absolute_import
from __future__ import unicode_literals

import csv
import datetime

import StringIO

from celery import task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from portal.models import EmailLog
from portal.serializers import EmailLogSerializer

@task()
def send_report():
	today = datetime.date.today()
	emails = EmailLog.objects.filter(created__contains = today)
	email_data = EmailLogSerializer(emails, many=True).data
	email_count = emails.count()

	email_body = """\
    <html>
      <body>
        <p>Total emails sent today:%s</p>
        <p>Find the stats in the attached csv doc</p>
      </body>
    </html>
    """ % (email_count)

	csvfile = StringIO.StringIO()
	csvwriter = csv.writer(csvfile)
	csvwriter.writerow(['Email address', 'Email type', 'Email subject', 'Timestamp'])
	for row in email_data:
		csvwriter.writerow([row['email'], row['email_type'], row['subject'], row['created']])

	#fetch admin user details
	superuser_emails = User.objects.filter(is_superuser=True).values_list('email', flat=True)

	#send email with csv file as attachment and content type as html
	try:
		email = EmailMessage("Today's email statistics", email_body, settings.EMAIL_HOST_USER, superuser_emails)
		email.attach('email_statistics.csv', csvfile.getvalue(), 'text/csv')
		email.content_subtype = "html"
		is_success = email.send(fail_silently=False)
		if is_success:
			print("Admin email sent successfully to " + str(superuser_emails))
		else:
			print("Error occured while sending admin email")
	except Exception as e:
		print("Exception while sending admin email:" + str(e))


