
import numpy as np

import math
from mpmath import cot
import turtle
import copy




class Triangle:
	def __init__(self,point_matrix: np.array):
		#print(type(point_matrix.shape))
		#print(point_matrix.shape)
		if point_matrix.shape != tuple((3,3)) and point_matrix.shape != tuple((3,4)):
			print("Error: Tried to construct triangle from a matrix which is not 3x3 or 3x4.")
			print("Current matrix: ")
			print(point_matrix)
			print("Matrix shape: " + str(point_matrix.shape))
			exit(1)
		if point_matrix.shape == (3,4):
			self.point_matrix = point_matrix # just do it as is
		else:


			# we need to also generate the fourth element for each matrix and also the fourth :

			self.point_matrix = np.zeros((3,4))

			for i in range(3):
				self.point_matrix[i] = np.append(point_matrix[i], 1)

def remove_values_from_list(the_list, val):
	return [value for value in the_list if value != val]

def load_smd(filename: str, offset: np.array):


	filehandle = open(filename, "r")

	lines = filehandle.readlines()

	filehandle.close()
	count = 0
	while "triangles" not in lines[count]:

		count += 1
	new_lines = lines[count:]

	actual_lines = []
	all_triangles = []
	count = 0
	point_strings = []
	for line in new_lines:
		if len(line) < 20:
			
			if len(point_strings) != 3 and len(point_strings) != 0:
				print("Error: Invalid number of points in triangle!")
				print("Point list:")
				print(point_strings)
				print("Length of point_strings: ")
				print(len(point_strings))
				exit(-1)
			
			if len(point_strings) == 0:
				print("First pass so continue.")
				continue
			# generate the triangle:
			print(point_strings)
			point1_str = point_strings[0]
			point2_str = point_strings[1]
			point3_str = point_strings[2]

			shit = point1_str.split(" ")
			print("shit:")
			print(shit)
			shit = remove_values_from_list(shit, "")
			# shit[0] = parent bone
			# shit[1:4] = {x,y,z}

			first_point = np.array([float(shit[1]), float(shit[2]), float(shit[3]), 1.0])
			first_point += offset
			shit = point2_str.split(" ")
			shit = remove_values_from_list(shit, "")
			second_point = np.array([float(shit[1]), float(shit[2]), float(shit[3]), 1.0])
			second_point += offset

			shit = point3_str.split(" ")
			shit = remove_values_from_list(shit, "")
			third_point = np.array([float(shit[1]), float(shit[2]), float(shit[3]), 1.0])
			third_point += offset

			all_triangles.append(Triangle(np.array([first_point, second_point, third_point])))
			print("Final triangle: ")
			print(np.array([first_point, second_point, third_point]))
			point_strings = []
		else:
			point_strings.append(line)
	print("Length of all_triangles: " + str(len(all_triangles)))
	print(len(new_lines)/4)
	#print(actual_lines)
	return all_triangles

if __name__=="__main__":
	load_smd("/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", np.array([0.0,0.0,100.0,0.0]))