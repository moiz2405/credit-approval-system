from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from credit.models import Customer
import math

@api_view(['POST'])
def register_customer(request):
    data = request.data
    try:
        first_name = data['first_name']
        last_name = data['last_name']
        age = data['age']
        monthly_income = int(data['monthly_income'])
        phone_number = data['phone_number']

        approved_limit = round((36 * monthly_income) / 100000) * 100000  # Nearest lakh

        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            age=age,
            monthly_salary=monthly_income,
            approved_limit=approved_limit,
            phone_number=phone_number
        )

        return Response({
            "customer_id": customer.id,
            "name": f"{customer.first_name} {customer.last_name}",
            "age": customer.age,
            "monthly_income": customer.monthly_salary,
            "approved_limit": customer.approved_limit,
            "phone_number": customer.phone_number
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
