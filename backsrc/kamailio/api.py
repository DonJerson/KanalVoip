from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
from datetime import timedelta
import random
import string
from django.db.models import Q

datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'

def phn():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return n[:3] + n[3:6] + n[6:]
def randomString(stringLength=10):

    """Generate a random string of fixed length """
    letters = string.ascii_letters+string.digits+string.punctuation[0]+string.punctuation[2:6]+string.punctuation[-1]
    return ''.join(random.choice(letters) for i in range(stringLength))
	
@api_view(['GET'])
#@permission_classes([])
def get_subscriber(request):
	#subscribers = Customer.objects.get(id=request.data["id"])
	#return Response(CustomerSerializer(subscribers,many=False).data)
	return Response(CustomerSerializer(request.user,many=False).data)

@api_view(['POST'])
#@permission_classes([])
def get_subscriber_admin(request):
	if(request.user.is_superuser):
		return Response(CustomerSerializer(Customer.objects.get(id=request.data["userId"]),many=False).data)
	#subscribers = Customer.objects.get(id=request.data["id"])
	#return Response(CustomerSerializer(subscribers,many=False).data)
	return Response("declined")

@api_view(['POST'])
#@permission_classes([])
def delete_subscriber(request):
	#subscribers = Customer.objects.get(id=request.data["id"])
	#return Response(CustomerSerializer(subscribers,many=False).data)
	subscriberNumber = request.data['subscriber']
	subscriber=Subscriber.objects.get(username=subscriberNumber)
	subscriber.delete()
	user=Customer.objects.get(id=request.user.id)
	return Response(CustomerSerializer(user,many=False).data)

@api_view(['GET'])
def add_device(request):
	username = phn()
	password=randomString(10)
	Subscriber.objects.create(customer=request.user,username=username,password=password)
	return Response(CustomerSerializer(request.user,many=False).data)

@api_view(['POST'])
def delete_device(request):
	subscriber = request.user.subscribers.filter(id=request.data["id"])
	print("delete subscriber")
	print(subscriber)
	subscriber.delete()
	return Response(CustomerSerializer(request.user,many=False).data)

@api_view(['POST'])
def get_history(request):
	amount = request.data['amount']
	if amount=="all":
		usageHistory = request.user.apiUsageHistoryMethod
		
		totalCalls = usageHistory.count()
	else:
		usageHistory = request.user.apiUsageHistoryMethod
		totalCalls = usageHistory.count()
		usageHistory=usageHistory[:amount]

	return Response({"history":ApiUsageSerializer(usageHistory,many=True).data,"totalCalls":totalCalls})

@api_view(['POST'])
def get_history_admin(request):
	amount = request.data['amount']
	print("la cantidad")
	print(amount)
	userId = request.data['userId']
	if(request.user.is_superuser):
		customer = Customer.objects.get(id=userId)
		
		if amount=="all":

			
			usageHistory = customer.apiUsageHistoryMethod
			
			totalCalls = usageHistory.count()

		else:
			usageHistory = customer.apiUsageHistoryMethod
			totalCalls = usageHistory.count()
			usageHistory=usageHistory[:amount]
	print("user ID COMING")
	print(userId)
	print(totalCalls)
	return Response({"history":ApiUsageSerializer(usageHistory,many=True).data,"totalCalls":totalCalls})

@api_view(['POST'])
def get_recargas_history(request):
	if(request.user.is_authenticated):
		recargasHistory = request.user.recargasHistory
		return Response({"history":RecargaSerializer(recargasHistory,many=True).data})
	else:
		return Response("")

@api_view(['POST'])
def filter_number(request):
	myId = request.data['id']
	numbers = request.data['numbers']
	print(numbers)
	results = ApiUsage.objects.none()
	for number in numbers:
		new = ApiUsage.objects.filter(
			Q(dst_user__contains=number,consumer_id=myId) |
			Q(src_user__contains=number,consumer_id=myId))
		results = results | new

	return Response(ApiUsageSerializer(results,many=True).data)

@api_view(['POST'])
@permission_classes([])
def new_customer(request):
	email = request.data["email"]
	password = request.data["password"]
	name = request.data["name"]
	phoneNumber = request.data["phoneNumber"]
	print(email)
	print(password)
	newCustomer = Customer.objects.create_user(username=email,password=password,email=email,name=name,phoneNumber=phoneNumber)
	newCustomer.save()
	username = phn()
	password=randomString(10)
	newSubscriber = Subscriber.objects.create(username=username,password=password,customer=newCustomer)
	
	return Response(CustomerSerializer(newCustomer,many=False).data)

@api_view(['POST'])
@permission_classes([])
def bill_call(request):
	try:
		callId = request.data["callId"]
		logStart = Acc.objects.get(consumer__isnull=True,method="INVITE",callid=callId)
		logEnd = Acc.objects.get(consumer__isnull=True,method="BYE",callid=callId)
		#logs = Acc.objects.all()
		consumer = Subscriber.objects.get(username=logStart.src_user).customer
		startDate=logStart.time
		endDate=logEnd.time
		logStart.consumer=consumer
		logEnd.consumer=consumer
		logStart.save()
		logEnd.save()
		diff = (endDate-startDate).seconds/60
		destination = logs[index].dst_user
		if destination[0]=="1":
			rate=0.010
		
		consumer.balance=float(consumer.balance)-rate*diff
		consumer.balance=-rate*diff
		consumer.save()
		#return Response(AccSerializer(logs,many=True).data)
		return Response("SUCCESS")
	except Exception as e:
		print(e)
		return Response({"BOBO":"BOBO","error":e})

@api_view(['GET'])
@permission_classes([])
def update_balance(request):
	logs = Acc.objects.filter(consumer__isnull=True)
	#logs = Acc.objects.all()
	index = 0
	while index < len(logs):
		newLogs = logs.filter(callid=logs[index].callid)
		print(newLogs)
		if len(newLogs)==2:
			consumer = Subscriber.objects.get(username=logs[index].src_user).customer
			startDate=""
			endDate=""

			for log in newLogs:
				log.consumer=consumer
				log.save()
				if log.method =="INVITE":
					startDate=log.time
				else: endDate=log.time
			diff = (endDate-startDate).seconds/60
			destination = logs[index].dst_user
			if destination[0]=="1":
				rate=0.010
			try:
				consumer.balance=float(consumer.balance)-rate*diff
			except Exception as e:
				consumer.balance=-rate*diff
			consumer.save()
			logs = logs.exclude(callid=logs[index].callid)
		else:
			index+=1
	return Response(AccSerializer(logs,many=True).data)

@api_view(['POST'])
def new_subscriber(request):
	customer = Customer.objects.get(id=request.data['id'])
	username = phn()
	#password=request.data["password"]
	password=randomString(10)
	newSubscriber = Subscriber.objects.create(username=username,password=password,customer=customer)
	return Response({"message" : "SUCCESS"})

@api_view(['POST'])
def ApiUsageOG(request):
	newData ={"consumer":{"id":request.data['id']},"serviceProvided":request.data["service"]}
	serializer = ApiUsageSerializer(data=newData)
	if serializer.is_valid():
		print("serializer")
		print(serializer)
		serializer.save()
	else:
		Response({"message" : "tienes un problema, contacte su Administrador de Softwares"})
	return Response({"message" : "SUCCESS"})

@api_view(['POST'])
def RecargaOG(request):
	newData ={"beneficiary":{"id":request.data['id']},"amount":request.data["amount"],"methodOfPayment":"CASH","validated":"false"}
	serializer = RecargaSerializer(data=newData)
	if serializer.is_valid():
		serializer.save()
	else:
		Response({"message" : "tienes un problema, contacte su Administrador de Softwares"})
	return Response({"message" : "SUCCESS"})

class RecargaViewSet(viewsets.ModelViewSet):
	queryset = Recarga.objects.all()
	serializer_class = RecargaSerializer
	pass

class ApiUsageViewSet(viewsets.ModelViewSet):
	queryset = ApiUsage.objects.all()
	serializer_class = ApiUsageSerializer
	pass

# @api_view(['POST'])
# def consumeApi(request):
# 	serializer = ApiUsageSerializer(data=request.data)
# 	if serializer.is_valid():
# 		serializer.save()
# 		return Response({"response" : "success", "message" : "Recarga exitosa"})
# 	else:
# 		Response({"response" : "error", "message" : serializer.errors})
# 	return Response({"response" : "success"})

class CustomerViewSet(viewsets.ModelViewSet):
	queryset = Customer.objects.all()
	serializer_class = CustomerSerializer
	pass

class SubscriberViewSet(viewsets.ModelViewSet):
	queryset = Subscriber.objects.all()
	serializer_class = SubscriberSerializer
	pass
