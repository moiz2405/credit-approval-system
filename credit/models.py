from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)  # Optional if you prefer an explicit ID
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    monthly_salary = models.IntegerField()  # Matches "monthly_salary" in Excel
    approved_limit = models.IntegerField()
    current_debt = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.customer_id})"
class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.FloatField()
    tenure = models.IntegerField()
    interest_rate = models.FloatField()
    monthly_installment = models.FloatField()  # Matches "monthly repayment (emi)"
    emis_paid_on_time = models.IntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} for Customer {self.customer.customer_id}"
