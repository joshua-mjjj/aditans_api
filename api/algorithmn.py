from django.shortcuts import render
from django.http import JsonResponse
from math import sqrt, radians, cos, sin, asin, degrees, atan2
import numpy as np

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *

from .models import *

def Cluster_Algorithmn(latitude, longitude, profile_project_id):
	# save algorithmn run instance
	# serializer = User_Serializer(data=request.data)
	# if serializer.is_valid():
	# 	serializer.save()
	
	# for i in dataset:
	# 	print(i)

	def validate_point(p):
		lat, lon, prmry = p
		assert -90<=lat<=90
		assert -180<=lon<=180

	def great_circle_distance(point1, point2):
		lat1, lon1, primary1 = point1
		lat2, lon2, primary2 = point2
		# print(primary1)
		# print(primary2)

		for p in [point1, point2]:
			validate_point(p)

		lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

		dlon = lon2 - lon1
		dlat = lat2 - lat1
		R = 6371 #km -- earth's radius

		a = sin(dlat/2)**2 + cos(lat1)*cos(lat2) * sin(dlon/2)**2
		c = 2 * asin(sqrt(a))
		d = R*c
		#return dlon, dlat
		return d

	#function for getting the closest  neigbours
	def get_neighbours(train, test_row, num_neighbours):
		distances = list() # with in 10 KM
		for train_row in train:
			dist = great_circle_distance(test_row, train_row) # KM
			# we can set the min distance to 10KM
			if(dist <= 10):
				distances.append((train_row, dist))
		distances.sort(key=lambda tup: tup[1])
		print(distances)
		neighbours = list()
		for i in range(num_neighbours):
			print(distances[i][0])
			neighbours.append(distances[i][0])
		return neighbours


	lat = latitude
	lon = longitude
	vague_id = 0
	cordinate = list()
	cordinate.append(lat)
	cordinate.append(lon)
	cordinate.append(vague_id)
	print(cordinate)

	# check is dataset length exceeds before setting neighbours
	neighbours = 3 # setting 

	# clients = ServiceProvider_Motor.objects.all().order_by('-id')
	dataset = Profile.objects.filter(project_type=profile_project_id).values_list('latitude', 'longitude', 'id')

	if len(dataset) >= 3:
		print("neighbours")
		neighbours = get_neighbours(dataset, cordinate, neighbours)
	else:
		neighbours = []
	# print(neighbours)
	# neighbours are sorted from nearest to farthest

	result_serializer = list()
	for neighbour in neighbours:
		pk = neighbour[2]
		result = Profile.objects.get(id=pk)
		# change clustered to true
		serializer = ProfileSeriaizer(result, many=False)

		result_serializer.append(serializer.data)
		
	# print(result_serializer)

	cluster_array = list()

	for neighbour in neighbours:
		pk = neighbour[2]
		cluster_array.append(pk)

	stringed = ''.join(map(str,cluster_array))
	print(cluster_array)
	print(stringed)
	try:
		save_array = Cluster.objects.create(cluster_members=stringed)
	except:
		pass

	return Response(result_serializer)
