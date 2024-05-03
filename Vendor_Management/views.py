from django.shortcuts import render
from .models import HistoricalPerformance
from django.db.models import Avg, Count
from django.db.models import Avg, F
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from datetime import timedelta
from django.utils import timezone

@api_view(['GET'])
def get_vendor_list(request):
    vendors = Vendor.objects.all()
    data = []
    for vendor in vendors:
        vendor_data = {
            'id': vendor.id,
            'name': vendor.name,
            'contact_details': vendor.contact_details,
            'address': vendor.address,
            'vendor_code': vendor.vendor_code,
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        data.append(vendor_data)
    return Response(data)

@api_view(['POST'])
def create_vendor(request):
    data = request.data
    vendor = Vendor.objects.create(
        name=data['name'],
        contact_details=data['contact_details'],
        address=data['address'],
        vendor_code=data['vendor_code']
    )
    return Response({'id': vendor.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor_data = {
        'id': vendor.id,
        'name': vendor.name,
        'contact_details': vendor.contact_details,
        'address': vendor.address,
        'vendor_code': vendor.vendor_code,
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate
    }
    return Response(vendor_data)

@api_view(['PUT'])
def update_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    data = request.data
    vendor.name = data.get('name', vendor.name)
    vendor.contact_details = data.get('contact_details', vendor.contact_details)
    vendor.address = data.get('address', vendor.address)
    vendor.vendor_code = data.get('vendor_code', vendor.vendor_code)
    vendor.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_vendor(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    vendor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_purchase_order(request):
    data = request.data
    try:
        vendor_id = int(data['vendor'])
        vendor = Vendor.objects.get(pk=vendor_id)
    except (KeyError, ValueError, Vendor.DoesNotExist):
        return Response({'error': 'Invalid vendor ID'}, status=status.HTTP_400_BAD_REQUEST)

    purchase_order = PurchaseOrder.objects.create(
        po_number=data['po_number'],
        vendor=vendor,
        order_date=data['order_date'],
        delivery_date=data.get('delivery_date', None),
        items=data['items'],
        quantity=data['quantity'],
        status=data.get('status', 'pending'),
        quality_rating=data.get('quality_rating', None),
        acknowledgment_date=data.get('acknowledgment_date', None)
    )
    return Response({'id': purchase_order.id}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_purchase_orders(request):
    if 'vendor' in request.query_params:
        vendor_id = request.query_params['vendor']
        try:
            vendor_id = int(vendor_id)
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        except ValueError:
            return Response({'error': 'Invalid vendor ID'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        purchase_orders = PurchaseOrder.objects.all()
    
    data = []
    for purchase_order in purchase_orders:
        po_data = {
            'po_number': purchase_order.po_number,
            'vendor': purchase_order.vendor_id,
            'order_date': purchase_order.order_date,
            'delivery_date': purchase_order.delivery_date,
            'items': purchase_order.items,
            'quantity': purchase_order.quantity,
            'status': purchase_order.status,
            'quality_rating': purchase_order.quality_rating,
            'acknowledgment_date': purchase_order.acknowledgment_date
        }
        data.append(po_data)
    
    return Response(data)


@api_view(['GET'])
def get_purchase_order_detail(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    po_data = {
        'po_number': purchase_order.po_number,
        'vendor': purchase_order.vendor_id,
        'order_date': purchase_order.order_date,
        'delivery_date': purchase_order.delivery_date,
        'items': purchase_order.items,
        'quantity': purchase_order.quantity,
        'status': purchase_order.status,
        'quality_rating': purchase_order.quality_rating,
        'acknowledgment_date': purchase_order.acknowledgment_date
    }
    return Response(po_data)

@api_view(['PUT'])
def update_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    data = request.data
    try:
        vendor_id = int(data['vendor'])
        vendor = Vendor.objects.get(pk=vendor_id)
    except (KeyError, ValueError, Vendor.DoesNotExist):
        return Response({'error': 'Invalid vendor ID'}, status=status.HTTP_400_BAD_REQUEST)

    purchase_order.po_number = data.get('po_number', purchase_order.po_number)
    purchase_order.vendor = vendor
    purchase_order.order_date = data.get('order_date', purchase_order.order_date)
    purchase_order.delivery_date = data.get('delivery_date', purchase_order.delivery_date)
    purchase_order.items = data.get('items', purchase_order.items)
    purchase_order.quantity = data.get('quantity', purchase_order.quantity)
    purchase_order.status = data.get('status', purchase_order.status)
    purchase_order.quality_rating = data.get('quality_rating', purchase_order.quality_rating)
    purchase_order.acknowledgment_date = data.get('acknowledgment_date', purchase_order.acknowledgment_date)
    purchase_order.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def delete_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
    purchase_order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    total_completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
    if total_completed_pos > 0:
        on_time_delivered_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', delivery_date__lte=F('acknowledgment_date')).count()
        on_time_delivery_rate = (on_time_delivered_pos / total_completed_pos) * 100
    else:
        on_time_delivery_rate = 0

    quality_rating_avg = PurchaseOrder.objects.filter(vendor=vendor, quality_rating__isnull=False).aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] or 0

    avg_response_time_timedelta = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']
    if avg_response_time_timedelta is not None:
        avg_response_time_seconds = avg_response_time_timedelta.total_seconds()
        avg_response_time_hours = avg_response_time_seconds / 3600  # Convert seconds to hours
    else:
        avg_response_time_hours = 0

    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    if total_pos > 0:
        fulfilled_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed').count()
        fulfillment_rate = (fulfilled_pos / total_pos) * 100
    else:
        fulfillment_rate = 0

    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = avg_response_time_hours
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    HistoricalPerformance.objects.update_or_create(
        vendor=vendor,
        date=timezone.now(),
        defaults={
            'on_time_delivery_rate': on_time_delivery_rate,
            'quality_rating_avg': quality_rating_avg,
            'average_response_time': avg_response_time_hours,
            'fulfillment_rate': fulfillment_rate
        }
    )

    performance_data = {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': avg_response_time_hours,
        'fulfillment_rate': fulfillment_rate
    }
    return Response(performance_data)