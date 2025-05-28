from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit.models import Customer, Loan
from datetime import date, timedelta
from credit.views.check_eligibility import calculate_emi


@api_view(['POST'])
def create_loan(request):
    try:
        data = request.data
        # customer = Customer.objects.get(id=data['customer_id'])
        customer = Customer.objects.get(customer_id=data['customer_id'])

        loan_amount = float(data['loan_amount'])
        interest_rate = float(data['interest_rate'])
        tenure = int(data['tenure'])

        monthly_installment = calculate_emi(loan_amount, interest_rate, tenure)
        start_date = date.today()
        end_date = start_date + timedelta(days=30 * tenure)

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=loan_amount,
            interest_rate=interest_rate,
            tenure=tenure,
            monthly_installment=monthly_installment,
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            "loan_id": loan.loan_id,
            "customer_id": customer.customer_id,
            "loan_approved": True,
            "message": "Loan successfully created",
            "monthly_installment": loan.monthly_installment
        }, status=status.HTTP_201_CREATED)

    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
