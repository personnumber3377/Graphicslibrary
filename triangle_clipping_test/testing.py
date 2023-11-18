


import numpy as np

import math
from mpmath import cot
import turtle
import copy
import keyboard






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




def distance_from_point_to_plane(point_on_plane, plane_normal, point):
	n = normalise_vector(point)

	return (plane_normal[0] * point[0] + plane_normal[1] * point[1] + plane_normal[2] * point[2] - np.dot(plane_normal, point_on_plane))

def intersection_between_plane_and_line(point_on_plane, plane_normal, point1, point2, debug=False):
	
	plane_normal = normalise_vector(plane_normal)
	plane_d = -1*np.dot(plane_normal, point_on_plane)
	ad = np.dot(point1, plane_normal)
	bd = np.dot(point2, plane_normal)
	
	t = (-1*plane_d - ad)/(bd - ad)
	linestarttoend = -1*point1+point2
	linetointersect = linestarttoend*t
	return point1 + linetointersect





def cliptriangleagainstplane(point_on_plane, plane_normal, triangle_to_clip, debug=True):
	plane_normal = normalise_vector(plane_normal)
	if debug:
		print("Point on plane: " + str(point_on_plane))
		print("plane_normal: " + str(plane_normal))
		print("Triangle to clip:")
		print(triangle_to_clip.point_matrix)

	if np.array_equal(triangle_to_clip.point_matrix[0], triangle_to_clip.point_matrix[1]) and np.array_equal(triangle_to_clip.point_matrix[1], triangle_to_clip.point_matrix[2]):
		print("Very shit.")
		exit()
	

	inside_points = []
	outside_points = []

	d0 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[0])
	d1 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[1])
	d2 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[2])

	if d0 >= 0:
		inside_points.append(triangle_to_clip.point_matrix[0])
	else:
		outside_points.append(triangle_to_clip.point_matrix[0])

	if d1 >= 0:
		inside_points.append(triangle_to_clip.point_matrix[1])
	else:
		outside_points.append(triangle_to_clip.point_matrix[1])

	if d2 >= 0:
		inside_points.append(triangle_to_clip.point_matrix[2])
	else:
		outside_points.append(triangle_to_clip.point_matrix[2])


	if debug:
		print("d0: " + str(d0))
		print("Point0: " + str(triangle_to_clip.point_matrix[0]))
		print("d1: " + str(d1))
		print("Point1: " + str(triangle_to_clip.point_matrix[1]))
		print("d2: " + str(d2))
		print("Point2: " + str(triangle_to_clip.point_matrix[2]))
		print("Length of inside_points: " + str(len(inside_points)))
		print("Length of outside_points: " + str(len(outside_points)))
		if len(inside_points) == 2:
			print("Outside point: " + str(outside_points[0]))




	if len(inside_points) == 0:
		return 0, []
	if len(inside_points) == 3:
		
		return 1, [triangle_to_clip]
	if len(inside_points) == 1 and len(outside_points) == 2:
		# here one point is inside the plane and two are outside so we need to make the new triangle use the intersection points between the old triangle and new triangles as points 2 and 3 and use the inside point as point1
		out_triangle = Triangle(triangle_to_clip.point_matrix)
		out_triangle.point_matrix[1] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[0])
		out_triangle.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[1])


		return 1, [out_triangle]
	print("Shitooooofff")
	print("Outside point at shitoooff: " + str(outside_points[0]))

	print("Input triangle at this point: ")
	print(triangle_to_clip.point_matrix)

	if len(inside_points) == 2 and len(outside_points) == 1:
		print("Thing")
		print("Outside point at loop: " + str(outside_points[0]))

		bullshit = copy.deepcopy(outside_points[0])
		bullshit_before = copy.deepcopy(bullshit)
		out_triangle1 = Triangle(np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1]]))
		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
		print(triangle_to_clip.point_matrix)
		
		# first triangle is composed of the two points inside and the point outside:

		out_triangle1.point_matrix[0] = inside_points[0]
		out_triangle1.point_matrix[1] = inside_points[1]

		print("BBBBBBBBBBBBBBBBBBB")
		print(triangle_to_clip.point_matrix)
		# here we calculate the intersection between out_triangle1.point_matrix[1] and the outside point
	
		shitthing = copy.deepcopy(inside_points[0])
		out_triangle1.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, shitthing, bullshit)
		

		# the second points consists of one of the inside points and the point outside and the previously calculated intersection between the other point and plane:

		print("The original input triangle is at before the out_triangle2 this: ")
		print(triangle_to_clip.point_matrix)

		#out_triangle2 = Triangle(triangle_to_clip.point_matrix)
		out_triangle2 = Triangle(np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1]]))
		#out_triangle2.point_matrix[]
		
		out_triangle2.point_matrix[0] = inside_points[1]
		out_triangle2.point_matrix[1] = out_triangle1.point_matrix[2]
		paskaperse = copy.deepcopy(inside_points[1])
		out_triangle2.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, paskaperse, bullshit, debug=True)
		
		print("The original input triangle is now: ")
		print(triangle_to_clip.point_matrix)
		return 2, [out_triangle1,out_triangle2]
	print("Bullshit: ")
	return 0



def drawtriangle(turtleobj, triangle_obj):
	turtle.penup()
	turtle.goto(triangle_obj.point_matrix[0][0], triangle_obj.point_matrix[0][1])
	turtle.pendown()
	turtle.goto(triangle_obj.point_matrix[1][0], triangle_obj.point_matrix[1][1])
	turtle.goto(triangle_obj.point_matrix[2][0], triangle_obj.point_matrix[2][1])
	turtle.goto(triangle_obj.point_matrix[0][0], triangle_obj.point_matrix[0][1])
	turtle.penup()
	#print("SHIIITT")
	return

def normalise_vector(vector: np.array):
	return vector/(np.sum(vector**2))



'''

Original input triangle: 
[[ 1.66916667e+03  2.50000000e+00  1.00100100e+00  1.00000000e+00]
 [ 2.50000000e+00  1.91666667e+01  1.00100100e+00  1.00000000e+00]
 [-1.02777778e+01  0.00000000e+00  1.00100100e+00  1.00000000e+00]]

'''


if __name__=="__main__":
	triangle = Triangle(np.array([[1.66916667e+03,  2.50000000e+00,  1.00100100e+00,  1.00000000e+00], [ 2.50000000e+00,  1.91666667e+01,  1.00100100e+00,  1.00000000e+00], [-1.02777778e+01,  0.00000000e+00,  1.00100100e+00,  1.00000000e+00]]))

	# cliptriangleagainstplane(point_on_plane, plane_normal, triangle_to_clip, debug=True)
	screenwidth = 500
	#num_of_out_triangles, out_triangles = cliptriangleagainstplane()

	how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([screenwidth-1,0,0,0]), np.array([-1,0,0,0]), triangle, debug=True)



