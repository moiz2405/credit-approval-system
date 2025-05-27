from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit.models import Loan, Customer  

# view loan by customer id 
@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        loans = Loan.objects.filter(customer_id=customer_id)
        loan_list = []

        for loan in loans:
            repayments_left = loan.tenure - loan.emis_paid_on_time
            loan_list.append({
                "loan_id": loan.loan_id,
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": loan.monthly_installment,
                "repayments_left": repayments_left
            })

        return Response(loan_list)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
