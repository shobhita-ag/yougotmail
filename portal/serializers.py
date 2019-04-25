from rest_framework import serializers

from django.utils.timezone import localtime
from portal.models import EmailLog

class EmailLogSerializer(serializers.ModelSerializer):

	email_type = serializers.SerializerMethodField()
	created = serializers.SerializerMethodField()

	class Meta:
		model = EmailLog
		fields = ('email', 'email_type', 'subject', 'created')

	def get_email_type(self, obj):
		return obj.get_email_type_display()

	def get_created(self, obj):
		return localtime(obj.created)
