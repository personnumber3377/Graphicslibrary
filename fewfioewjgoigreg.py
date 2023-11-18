

import numpy as np

import math
from mpmath import cot
import turtle
import copy

# define a triangle:



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

class Camera:
	def __init__(self, cameraPos: np.array, rotate_vector: np.array):

		self.pos = cameraPos

		self.rotate_vector = rotate_vector

	def get_z_rotation_matrix(self):

		# self.rotate_vector[2] is theta_z

		theta_z = self.rotate_vector[2]

		return np.array([[math.cos(theta_z), math.sin(theta_z), 0, 0],
			[-1*math.sin(theta_z), math.cos(theta_z), 0, 0],
			[0,0,1,0],
			[0,0,0,1]])
	def get_y_rotation_matrix(self):
		theta_y = self.rotate_vector[1]

		return np.array([[math.cos(theta_y),0,-1*math.sin(theta_y),0],
			[0,1,0,0],
			[math.sin(theta_y), 0, math.cos(theta_y), 0],
			[0,0,0,1]])
	def get_x_rotation_matrix(self):
		theta_x = self.rotate_vector[0]

		return np.array([[1,0,0,0],
			[0,math.cos(theta_x), math.sin(theta_x), 0],
			[0,-1*math.sin(theta_x), math.cos(theta_x), 0],
			[0,0,0,1]])
	def transform_point(self,point):
		
		# offset 

		point = -1*self.pos+point

		# rotate

		point = np.dot(point, self.get_z_rotation_matrix())
		point = np.dot(point, self.get_y_rotation_matrix())
		point = np.dot(point, self.get_x_rotation_matrix())

		# return transformed_point

		return point

def cotangent(angle):
	return (math.cos(angle)/(math.sin(angle)))


def get_perspective_projection_matrix(field_of_view: float, aspect_ratio: float, near: float, far: float):
	h = cotangent(field_of_view/2.0)
	w = h/(aspect_ratio)

	return np.array([[w,0,0,0],
		[0,h,0,0],
		[0,0,far/(near-far), -1],
		[0,0,(near*far)/(near-far),0]])



def do_camera_transform_for_triangle(triangle: Triangle, camera: Camera):
	triangle_shit = copy.deepcopy(triangle)
	for i in range(3):
		triangle_shit.point_matrix[i] = camera.transform_point(triangle.point_matrix[i])
	return triangle_shit

def distance_from_point_to_plane(point_on_plane, plane_normal, point):
	n = normalise_vector(point)

	return (plane_normal[0] * point[0] + plane_normal[1] * point[1] + plane_normal[2] * point[2] - np.dot(plane_normal, point_on_plane))

def intersection_between_plane_and_line(point_on_plane, plane_normal, point1, point2):
	print("Point1:" + str(point1))
	print("Point2: " + str(point2))
	plane_normal = normalise_vector(plane_normal)
	plane_d = -1*np.dot(plane_normal, point_on_plane)
	ad = np.dot(point1, plane_normal)
	bd = np.dot(point2, plane_normal)
	print(plane_d)
	print(ad)
	print(bd)
	print(ad)
	t = (-1*plane_d - ad)/(bd - ad)
	linestarttoend = -1*point1+point2
	linetointersect = linestarttoend*t
	return point1 + linetointersect





def cliptriangleagainstplane(point_on_plane, plane_normal, triangle_to_clip, debug=False):
	plane_normal = normalise_vector(plane_normal)
	if debug:
		print("Point on plane: " + str(point_on_plane))
		print("plane_normal: " + str(plane_normal))
		print("Triangle to clip:")
		print(triangle_to_clip.point_matrix)
	

	inside_points = []
	outside_points = []

	d0 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[0])
	d1 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[1])
	d2 = distance_from_point_to_plane(point_on_plane, plane_normal, triangle_to_clip.point_matrix[2])

	if d0 >= 0:
		inside_points.append(triangle_to_clip.point_matrix[0])
	else:
		outside_points.append(triangle_to_clip.point_matrix[0])

	if d0 >= 1:
		inside_points.append(triangle_to_clip.point_matrix[1])
	else:
		outside_points.append(triangle_to_clip.point_matrix[1])

	if d0 >= 2:
		inside_points.append(triangle_to_clip.point_matrix[2])
	else:
		outside_points.append(triangle_to_clip.point_matrix[2])


	print("Amount of inside points: " + str(inside_points))

	if len(inside_points) == 0:
		return 0, []
	if len(inside_points) == 3:
		print("Everything is inside")
		return 1, [triangle_to_clip]
	if len(inside_points) == 1:
		# here one point is inside the plane and two are outside so we need to make the new triangle use the intersection points between the old triangle and new triangles as points 2 and 3 and use the inside point as point1
		out_triangle = Triangle(triangle_to_clip.point_matrix)
		out_triangle.point_matrix[1] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[0])
		out_triangle.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[1])


		return 1, [out_triangle]
	if len(inside_points) == 2 and len(outside_points) == 1:

		out_triangle1 = Triangle(inside_points[0].point_matrix)
		

		# first triangle is composed of the two points inside and the point outside:

		out_triangle1.point_matrix[0] = inside_points[0]
		out_triangle1.point_matrix[1] = inside_points[1]

		# here we calculate the intersection between out_triangle1.point_matrix[1] and the outside point
		out_triangle1.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[0])


		# the second points consists of one of the inside points and the point outside and the previously calculated intersection between the other point and plane:


		out_triangle2 = Triangle(inside_points[1].point_matrix)

		out_triangle2.point_matrix[0] = inside_points[1]
		out_triangle2.point_matrix[1] = out_triangle1.point_matrix[2]
		out_triangle2.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[1], outside_points[0])

		return 2, [out_triangle1,out_triangle2]
	print("Bullshit: ")
	return 0



def drawtriangle(turtleobj, triangle_obj):
	turtle.penup()
	turtle.goto(triangle_obj.point1[0], triangle_obj.point1[1])
	turtle.pendown()
	turtle.goto(triangle_obj.point2[0], triangle_obj.point2[1])
	turtle.goto(triangle_obj.point3[0], triangle_obj.point3[1])
	turtle.goto(triangle_obj.point1[0], triangle_obj.point1[1])
	turtle.penup()
	print("SHIIITT")
	return

def normalise_vector(vector: np.array):
	return vector/(np.sum(vector**2))


def project_triangle_from_2d_to_3d(triangle: Triangle, projection_matrix: np.array):
	for i in range(3):
		triangle.point_matrix[i] = np.dot(triangle.point_matrix[i], projection_matrix)
	return triangle

if __name__=="__main__":
	screenwidth = 500
	screenheight = 500
	triangle = Triangle(np.array([[0.0,0.0,15.0,1.0], [10.0,0.0,15.0,1.0], [0.0,10.0,15.0,1.0]]))
	triangles = [triangle]
	cameraPos = np.array([0.0,0.0,0.0,1.0])
	camera_rotation = np.array([0.0,0.0,0.0,1.0])
	camera = Camera(cameraPos, camera_rotation)
	transformed_point = camera.transform_point(triangle.point_matrix[0])
	print(transformed_point)

	field_of_view = math.pi/2
	ratio = 1

	# first make camera transform for each triangle in triangles
	triangles_to_sort = []
	how_many_cycles = 3
	debug = True
	#for count in range(how_many_cycles):
	while True:
		print("Triangles:")
		print(triangles[0].point_matrix)
		for triangle in triangles:
			# first do the camera transform for the point:
			triangle_oof = do_camera_transform_for_triangle(triangle, camera)

			if debug:
				print("---------------------\n\nCamera transform:\n\n")
				print("Original triangle: ")
				print(triangle.point_matrix)
				print("Camera transformed triangle: ")
				print(triangle_oof.point_matrix)
				print("-------------\n\n")

		
			# Clip against near plane:
			# here the near plane is assumed to be at distance 1 from the camera
			if debug:
				print("----------------------\n\nNear clipping phase\n\n\n")


			number_of_clipped_triangles, out_triangles = cliptriangleagainstplane(np.array([0,0,1,1]), np.array([0,0,1,0]), triangle_oof, debug=debug)
			if debug:
				print("-------------\n\n")
			for i in range(number_of_clipped_triangles):

				projection_matrix = get_perspective_projection_matrix(field_of_view, ratio, 0.1, 100)

				if debug:
					print("----------------\n\n\n\nPerspective projection matrix: ")
					print(projection_matrix)
					print("--------------------\n\n\n")

				if debug:
					print("-----------------------\n\n\nProjection phase:\n\n")
					print("Original triangle:")
					print(out_triangles[i].point_matrix)
				out_triangles[i] = project_triangle_from_2d_to_3d(out_triangles[i], projection_matrix)
				if debug:
					print("Resulting triangle: ")
					print(out_triangles[i].point_matrix)
					print("----------------------\n\n\n")


				# offset into normalised space

				voffset = np.array([1,1,0,0])

				for k in range(3):
					out_triangles[i].point_matrix[0] = out_triangles[i].point_matrix[0] + voffset
					

				for j in range(3):
					out_triangles[i].point_matrix[j][0] = out_triangles[i].point_matrix[j][0] * (0.5 * screenwidth)
					out_triangles[i].point_matrix[j][1] = out_triangles[i].point_matrix[j][1] * (0.5 * screenheight)


				triangles_to_sort.append(out_triangles[i])












		







		triangles_sorted = sorted(triangles_to_sort, key=lambda x: (x.point_matrix[0][2]+x.point_matrix[1][2]+x.point_matrix[2][2])/3.0) # first point and the z coordinate

		#print(triangles_sorted)
		# clip each triangle and draw them:


		turtle.clearscreen()

		for triangle in triangles_sorted:
			

			clipped_triangles = []

			current_triangle_list = [triangle]

			amount_of_new_triangles = 1

			for p in range(4):
				how_many_to_add = 0

				while amount_of_new_triangles > 0:




					cur_triangle = current_triangle_list.pop(0)
					amount_of_new_triangles -= 1

					# def cliptriangleagainstplane(point_on_plane, plane_normal, triangle_to_clip):
					# return num_of_triangles_triangles
					if p == 0:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,0,0,0]), np.array([0,1,0,0]), cur_triangle)
					if p == 1:
						
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,screenheight-1,0,0]), np.array([0,-1,0,0]), cur_triangle)
					if p == 2:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,0,0,0]), np.array([1,0,0,0]), cur_triangle)
					if p == 3:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([screenwidth-1,0,0,0]), np.array([-1,0,0,0]), cur_triangle)
					
					print("Appended triangles: ")
					print(appended_triangles)
					if how_many_to_add == 0:
						print("----------------------")
						print(p)
						cliptriangleagainstplane(np.array([0,screenheight-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=True)
						exit()

					for triangle_oof in appended_triangles:
						current_triangle_list.append(triangle_oof)
				amount_of_new_triangles = len(current_triangle_list)

			for triangle in current_triangle_list:
				print("ooofff")
				print("Thing")
				drawtriangle(turtleobj, triangle)

			












