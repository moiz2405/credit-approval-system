from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit.models import Customer, Loan
from datetime import date

def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)

    if customer.current_debt > customer.approved_limit:
        return 0

    score = 100

    # Components
    total_loans = loans.count()
    on_time_loans = sum(loan.emis_paid_on_time for loan in loans)
    total_loan_volume = sum(loan.loan_amount for loan in loans)
    current_year_loans = loans.filter(start_date__year=date.today().year).count()

    score -= (total_loans * 2)
    score += (on_time_loans * 1.5)
    score -= (current_year_loans * 2)

    if total_loan_volume > customer.approved_limit:
        score -= 10

    return max(0, min(100, round(score)))

def calculate_emi(amount, interest_rate, tenure):
    monthly_interest = interest_rate / (12 * 100)
    emi = (amount * monthly_interest * ((1 + monthly_interest) ** tenure)) / (((1 + monthly_interest) ** tenure) - 1)
    return round(emi, 2)

@api_view(['POST'])
def check_eligibility(request):
    try:
        data = request.data
        customer_id = data['customer_id']
        loan_amount = float(data['loan_amount'])
        interest_rate = float(data['interest_rate'])
        tenure = int(data['tenure'])

        customer = Customer.objects.get(id=customer_id)
        credit_score = calculate_credit_score(customer)

        approval = False
        corrected_rate = interest_rate

        if credit_score > 50:
            approval = True
        elif 30 < credit_score <= 50:
            approval = True
            if interest_rate <= 12:
                corrected_rate = 13
        elif 10 < credit_score <= 30:
            approval = True
            if interest_rate <= 16:
                corrected_rate = 17
        elif credit_score <= 10:
            approval = False

        emis = calculate_emi(loan_amount, corrected_rate, tenure)
        current_loans = Loan.objects.filter(customer=customer)
        total_emis = sum(loan.monthly_installment for loan in current_loans)

        if (total_emis + emis) > (0.5 * customer.monthly_salary):
            approval = False

        return Response({
            "customer_id": customer.id,
            "approval": approval,
            "interest_rate": interest_rate,
            "corrected_interest_rate": corrected_rate,
            "tenure": tenure,
            "monthly_installment": emis
        })

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
