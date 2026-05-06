from django.contrib import admin
from .models import CustomerRecord
@admin.register(CustomerRecord)
class CustomerRecordAdmin(admin.ModelAdmin):
    list_display=('applicant_no','name','ifsc','branch','city','credit','debit','balance')
    search_fields=('applicant_no','name','ifsc','city')
    list_filter=('branch','city')
