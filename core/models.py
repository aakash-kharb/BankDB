from django.db import models
class CustomerRecord(models.Model):
    applicant_no = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=11, db_index=True)
    credit = models.FloatField(default=0.0)
    debit = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    city = models.CharField(max_length=50)
    branch = models.IntegerField()
    class Meta:
        db_table = "customer_records"
        ordering = ["applicant_no"]
    def __str__(self):
        return f"{self.applicant_no} - {self.name}"
