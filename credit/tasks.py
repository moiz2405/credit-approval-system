from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def ingest_customer_data():
    df = pd.read_excel("customer_data.xlsx")
    for _, row in df.iterrows():
        Customer.objects.get_or_create(
            customer_id=row['customer_id'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            phone_number=row['phone_number'],
            monthly_salary=row['monthly_salary'],
            approved_limit=row['approved_limit'],
            current_debt=row['current_debt']
        )

@shared_task
def ingest_loan_data():
    df = pd.read_excel("loan_data.xlsx")
    for _, row in df.iterrows():
        customer = Customer.objects.get(customer_id=row['customer id'])
        Loan.objects.create(
            customer=customer,
            loan_amount=row['loan amount'],
            tenure=row['tenure'],
            interest_rate=row['interest rate'],
            monthly_installment=row['monthly repayment (emi)'],
            emis_paid_on_time=row['EMIs paid on time'],
            start_date=pd.to_datetime(row['start date']),
            end_date=pd.to_datetime(row['end date']),
        )
