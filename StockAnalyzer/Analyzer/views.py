from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from Analyzer.models import Stock
from Analyzer.serializers import StockSerializer

# Create your views here.
@csrf_exempt
def StockList(request):
    """
    List all stocks, or create a new stock.
    """
    if request.method == 'GET':
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def StockDetail(request, pk):
    """
    Retrieve, update or delete a stock.
    """
    try:
        stock = Stock.objects.get(pk=pk)
    except Stock.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StockSerializer(stock)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = StockSerializer(stock, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        stock.delete()
        return HttpResponse(status=204)