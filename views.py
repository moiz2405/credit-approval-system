from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
from .serializers import CustomerSerializer, LoanSerializer
from datetime import datetime
import math

# Utility function
def round_to_nearest_lakh(value):
    return int(round(value / 100000.0)) * 100000

# Register Customer
@api_view(['POST'])
def register_customer(request):
    data = request.data
    salary = int(data.get('monthly_salary'))
    approved_limit = round_to_nearest_lakh(36 * salary)
    data['approved_limit'] = approved_limit
    serializer = CustomerSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Check Eligibility
@api_view(['POST'])
def check_eligibility(request):
    customer_id = request.data.get('customer_id')
    loan_amount = float(request.data.get('loan_amount'))
    tenure = int(request.data.get('tenure'))
    interest_rate = float(request.data.get('interest_rate'))

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    loans = Loan.objects.filter(customer=customer)
    emis_paid_on_time = sum([l.emis_paid_on_time for l in loans])
    total_emis = sum([l.tenure for l in loans]) or 1
    payment_ratio = emis_paid_on_time / total_emis

    past_loans = loans.count()
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()

    credit_score = 0
    if customer.current_debt > customer.approved_limit:
        credit_score = 0
    else:
        credit_score += min(40, payment_ratio * 40)
        credit_score += min(20, 20 - current_year_loans * 5)
        credit_score += min(40, 40 - past_loans * 2)

    approval = credit_score >= 50
    corrected_interest = interest_rate + (5 if credit_score < 50 else 0)
    monthly_installment = (loan_amount * (1 + (corrected_interest/100))) / tenure

    return Response({
        "approval": approval,
        "credit_score": credit_score,
        "corrected_interest_rate": corrected_interest,
        "monthly_installment": round(monthly_installment, 2)
    })
# Create Loan
@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data.get('customer_id')

    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    loan_amount = float(data.get('loan_amount'))
    tenure = int(data.get('tenure'))
    interest_rate = float(data.get('interest_rate'))

    # Eligibility check logic (reused)
    loans = Loan.objects.filter(customer=customer)
    emis_paid_on_time = sum([l.emis_paid_on_time for l in loans])
    total_emis = sum([l.tenure for l in loans]) or 1
    payment_ratio = emis_paid_on_time / total_emis
    past_loans = loans.count()
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()

    credit_score = 0
    if customer.current_debt > customer.approved_limit:
        credit_score = 0
    else:
        credit_score += min(40, payment_ratio * 40)
        credit_score += min(20, 20 - current_year_loans * 5)
        credit_score += min(40, 40 - past_loans * 2)

    approval = credit_score >= 50
    corrected_interest = interest_rate + (5 if credit_score < 50 else 0)
    monthly_installment = (loan_amount * (1 + (corrected_interest/100))) / tenure

    if not approval:
        return Response({
            "loan_id": None,
            "message": "Loan not approved due to low credit score"
        }, status=400)

    # Create loan
    loan = Loan.objects.create(
        customer=customer,
        loan_amount=loan_amount,
        tenure=tenure,
        interest_rate=corrected_interest,
        monthly_installment=monthly_installment,
        start_date=datetime.now().date(),
        end_date=datetime.now().date().replace(year=datetime.now().year + int(tenure/12))
    )

    # Update customer debt
    customer.current_debt += loan_amount
    customer.save()

    return Response({
        "loan_id": loan.loan_id,
        "message": "Loan approved and created"
    }, status=201)

# View Loan by loan_id
@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error": "Loan not found"}, status=404)
    
    loan_data = LoanSerializer(loan).data
    customer_data = CustomerSerializer(loan.customer).data
    return Response({
        "loan": loan_data,
        "customer": customer_data
    })

# View all loans by customer
@api_view(['GET'])
def view_loans(request, customer_id):
    loans = Loan.objects.filter(customer__id=customer_id)
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)
