from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from datetime import datetime

@shared_task
def ingest_customer_data():
    df = pd.read_excel("customer_data.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.strip("'\"")

    column_map = {
        'customer id': 'customer_id',
        'first name': 'first_name',
        'last name': 'last_name',
        'phone number': 'phone_number',
        'monthly salary': 'monthly_salary',
        'approved limit': 'approved_limit',
    }

    df.rename(columns=column_map, inplace=True)
    print("Customer columns:", df.columns.tolist())

    for _, row in df.iterrows():
        defaults = {
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'phone_number': row['phone_number'],
            'monthly_salary': row['monthly_salary'],
            'approved_limit': row['approved_limit'],
            'current_debt': 0
        }
        Customer.objects.update_or_create(
            customer_id=row['customer_id'],  # ✅ Fixed here
            defaults=defaults
        )

@shared_task
def ingest_loan_data():
    df = pd.read_excel("loan_data.xlsx")
    df.columns = df.columns.str.strip().str.lower().str.strip("'\"")

    column_map = {
        'loan id': 'loan_id',
        'customer id': 'customer_id',
        'loan amount': 'loan_amount',
        'tenure': 'tenure',
        'interest rate': 'interest_rate',
        'monthly payment': 'monthly_installment',
        'emis paid on time': 'emis_paid_on_time',
        'date of approval': 'start_date',
        'end date': 'end_date'
    }

    df.rename(columns=column_map, inplace=True)
    print("Loan columns:", df.columns.tolist())

    for _, row in df.iterrows():
        try:
            customer = Customer.objects.get(customer_id=row['customer_id'])
        except Customer.DoesNotExist:
            continue

        defaults = {
            'customer': customer,
            'loan_amount': row['loan_amount'],
            'tenure': row['tenure'],
            'interest_rate': row['interest_rate'],
            'monthly_installment': row['monthly_installment'],
            'emis_paid_on_time': row['emis_paid_on_time'],
            'start_date': pd.to_datetime(row['start_date']).date(),
            'end_date': pd.to_datetime(row['end_date']).date(),
        }

        Loan.objects.update_or_create(
            loan_id=row['loan_id'],
            defaults=defaults
        )
