from datetime import datetime

from django.db import connection
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from pydantic import ValidationError
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Tenant, Transaction, Apartment, Lease, MonthlyReportRequest
from .queries import TENANT_INFO_QUERY, ALL_TENANT_INFO_QUERY, MONTHLY_REPORT_QUERY, MONTHLY_REPORT_COUNT_QUERY, \
    LEASE_TRANSACTION_REPORT_QUERY
from .serializers import TenantSerializer, LeaseSerializer, TransactionSerializer, ApartmentSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def get_queryset(self):
        # Check if the 'status' query parameter is in the request
        status = self.request.query_params.get('status', None)

        # If 'status' is 'true', filter the queryset to include only apartments with apartment_status=True
        if status == 'true':
            return Apartment.objects.filter(apartment_status=True)

        # If 'status' is not 'true' or not provided, return all apartments
        return Apartment.objects.all()


class LeaseViewSet(viewsets.ModelViewSet):
    queryset = Lease.objects.all()
    serializer_class = LeaseSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


@api_view(['GET'])
def apartment_status_count(request):
    true_count = Apartment.objects.filter(apartment_status=True).count()
    false_count = Apartment.objects.filter(apartment_status=False).count()

    return Response({
        'occupied_count': true_count,
        'vacant_count': false_count
    })


@api_view(['GET'])
def active_lease_rent_sum(request):
    rent_sum = Lease.objects.filter(lease_status='Active').aggregate(Sum('rent_amount'))

    return Response({
        'active_lease_rent_sum': rent_sum['rent_amount__sum']
    })


@api_view(['GET'])
def current_month_year_transaction_sum(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    transaction_sum = Transaction.objects.filter(month=current_month, year=current_year).aggregate(Sum('amount_paid'))

    return Response({
        'current_month_year_transaction_sum': transaction_sum['amount_paid__sum']
    })




@api_view(['GET'])
def rent_and_transaction_summary(request):
    # Calculate the sum of the rent_amount for lease_status = 'Active'
    rent_sum = Lease.objects.filter(lease_status='Active').aggregate(Sum('rent_amount'))['rent_amount__sum']

    # Calculate the total amount_paid for transactions where month equals the current month and year equals the
    # current year
    current_month = datetime.now().month
    current_year = datetime.now().year
    transaction_sum = Transaction.objects.filter(month=current_month, year=current_year).aggregate(Sum('amount_paid'))[
        'amount_paid__sum']

    # Calculate the percentage of rent collected
    if rent_sum > 0:
        percentage_collected = (transaction_sum / rent_sum) * 100
    else:
        percentage_collected = 0

    return Response({
        'active_lease_rent_sum': rent_sum,
        'current_month_year_transaction_sum': transaction_sum,
        'percentage_of_rent_collected': percentage_collected
    })


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


@api_view(['GET'])
def tenant_info(request):
    with connection.cursor() as cursor:
        cursor.execute(TENANT_INFO_QUERY)
        tenant_info = dictfetchall(cursor)
    return JsonResponse(tenant_info, safe=False)


@api_view(['GET'])
def tenant_detail(request, tenant_id):
    with connection.cursor() as cursor:
        cursor.execute(ALL_TENANT_INFO_QUERY, [tenant_id])
        tenant_info = dictfetchall(cursor)
    if tenant_info:
        return JsonResponse(tenant_info[0], safe=False)
    else:
        return JsonResponse({"error": "Tenant not found"}, status=404)


@api_view(['POST'])
def monthly_report(request):
    try:
        # Create an instance of the MonthlyReportRequest class from the request data
        report_request = MonthlyReportRequest(**request.data)
    except ValidationError as e:
        # If the request data is not valid, return a 400 Bad Request response with the validation errors
        return JsonResponse({'error': e.errors()}, status=400)

    offset = (report_request.page_number - 1) * report_request.page_size
    with connection.cursor() as cursor:

        first_day_of_month = datetime(report_request.year, report_request.month, 1)
        year_month = first_day_of_month.strftime('%Y-%m-%d')

        # Execute the COUNT query to get the total number of records
        cursor.execute(MONTHLY_REPORT_COUNT_QUERY.format(report_request.month, report_request.year, year_month))
        total_records = cursor.fetchone()[0]

        # Execute the MONTHLY_REPORT_QUERY with LIMIT and OFFSET
        formatted_query = MONTHLY_REPORT_QUERY.format(year_month, report_request.month, report_request.year,
                                                      report_request.page_size, offset)
        cursor.execute(formatted_query)
        report = dictfetchall(cursor)

        # Execute the LEASE_TRANSACTION_REPORT_QUERY
        formatted_query = LEASE_TRANSACTION_REPORT_QUERY.format(year_month)
        cursor.execute(formatted_query)
        lease_transaction_report = dictfetchall(cursor)

        # Include pagination details in the response
        response = {
            'page_size': report_request.page_size,
            'page_number': report_request.page_number,
            'total_records': total_records,
            'report': report,
            'leased_apartment_count': lease_transaction_report[0]['leased_apartment_count'],
            'total_rent_amount': lease_transaction_report[0]['total_rent_amount'],
            'total_amount_paid': lease_transaction_report[0]['total_amount_paid'],
            'transaction_count': lease_transaction_report[0]['transaction_count'],
        }
    return JsonResponse(response, safe=False)

