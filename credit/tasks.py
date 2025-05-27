from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def ingest_customer_data():
    df = pd.read_excel("customer_data.xlsx")
    # Normalize columns: lowercase and strip spaces
    df.columns = df.columns.str.strip().str.lower()
    print(df.columns.tolist())

    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row['customer id'],
            defaults={
                'first_name': row['first name'],
                'last_name': row['last name'],
                'phone_number': row['phone number'],
                'monthly_salary': row['monthly salary'],
                'approved_limit': row['approved limit'],
                'current_debt': 0
            }
        )

@shared_task
def ingest_loan_data():
    df = pd.read_excel("loan_data.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    print(df.columns.tolist())

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['customer id'])
        except Customer.DoesNotExist:
            continue

        Loan.objects.update_or_create(
            loan_id=row['loan id'],
            defaults={
                'customer': customer,
                'loan_amount': row['loan amount'],
                'tenure': row['tenure'],
                'interest_rate': row['interest rate'],
                'monthly_installment': row['monthly payment'],
                'emis_paid_on_time': row['emis paid on time'],
                'start_date': pd.to_datetime(row['date of approval']).date(),
                'end_date': pd.to_datetime(row['end date']).date(),
            }
        )
