

import numpy as np

import math
from mpmath import cot
import turtle
import copy
import keyboard
import io
from PIL import Image

# define a triangle:


'''

[[  2  19   1   1]
 [499  13   1   1]
 [499  12   1   1]]
 
[[  2  19   1   1]
 [  0  15   1   1]
 [499  12   1   1]]

[[  0  15   1   1]
 [499  12   1   1]
 [499  10   1   1]]

[[  0  15   1   1]
 [  0   0   1   1]
 [499  10   1   1]]

[[  0   0   1   1]
 [499  10   1   1]
 [499   0   1   1]]

'''

class Triangle:
	def __init__(self,point_matrix: np.array):
		#print(type(point_matrix.shape))
		#print(point_matrix.shape)
		self.normal = None
		self.color = None
		self.id = -1
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

	def setcolor(self, sun_direction_vector):
		normal = get_surface_normal_for_triangle(self)
		#print("Normal: " + str(normal))
		#print(normal)
		coloof = np.dot(normal, sun_direction_vector)
		coloof = max(0, coloof)

		#print(coloof)
		coloof *= 255
		coloof = round(coloof)
		hex_shit = hex(coloof)
		hex_shit = hex_shit[2:]
		#if hex_shit != "93" and hex_shit != "00":
		#	print("Quite shit")
		#	exit()
		if len(hex_shit) == 1:
			hex_shit = "0"+hex_shit

		color = "#"+hex_shit*3
		self.color = color

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
	'''
	return np.array([[w,0,0,0],
		[0,h,0,0],
		[0,0,far/(near-far), -1],
		[0,0,(near*far)/(near-far),0]])
	'''
	'''
	return np.array([[w,0,0,0],
		[0,h,0,0],
		[0,0,-1*far/(far-near), -1],
		[0,0,-1*(near*far)/(far-near),0]])
	'''
	return np.array([[w,0,0,0],
		[0,h,0,0],
		[0,0,far/(far-near), 1],
		[0,0,(-1*near*far)/(far-near),0]])





def do_camera_transform_for_triangle(triangle: Triangle, camera: Camera):
	triangle_shit = copy.deepcopy(triangle)
	for i in range(3):
		triangle_shit.point_matrix[i] = camera.transform_point(triangle.point_matrix[i])
	return triangle_shit

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





def cliptriangleagainstplane(point_on_plane, plane_normal, triangle_to_clip, debug=False):
	plane_normal = normalise_vector(plane_normal)
	if debug:
		print("Point on plane: " + str(point_on_plane))
		print("plane_normal: " + str(plane_normal))
		print("Triangle to clip:")
		print(triangle_to_clip.point_matrix)
	
	if np.array_equal(triangle_to_clip.point_matrix[0], triangle_to_clip.point_matrix[1]) and np.array_equal(triangle_to_clip.point_matrix[1], triangle_to_clip.point_matrix[2]):
		print("Very shit.")
		print(triangle_to_clip.point_matrix)
		return 0, []
		#exit()


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
		out_triangle = Triangle(np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1]]))
		out_triangle.point_matrix[0] = inside_points[0]
		out_triangle.point_matrix[1] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[0])
		out_triangle.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[0], outside_points[1])
		if debug:
			print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOFFFFFFFFFF")
			print(out_triangle.point_matrix)
		out_triangle.color = triangle_to_clip.color
		return 1, [out_triangle]
	if debug:
		print("Shitooooofff")
		print("Outside point at shitoooff: " + str(outside_points[0]))
	if len(inside_points) == 2 and len(outside_points) == 1:
		if debug:
			print("Thing")
			print("Outside point at loop: " + str(outside_points[0]))

		bullshit = copy.deepcopy(outside_points[0])
		bullshit_before = copy.deepcopy(bullshit)
		out_triangle1 = Triangle(np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1]]))
		if debug:
			print("after triangle thing: " + str(outside_points[0]))
		# first triangle is composed of the two points inside and the point outside:

		out_triangle1.point_matrix[0] = inside_points[0]
		out_triangle1.point_matrix[1] = inside_points[1]

		# here we calculate the intersection between out_triangle1.point_matrix[1] and the outside point
		print("before debug thing: " + str(outside_points[0]))
		if debug:
			print("Shittt")
			print("Outside point: " + str(outside_points[0]))
		shitthing = copy.deepcopy(inside_points[0])
		out_triangle1.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, shitthing, bullshit)
		if debug:
			print("ooooooooofffffffffff")

		# the second points consists of one of the inside points and the point outside and the previously calculated intersection between the other point and plane:



		#out_triangle2 = Triangle(triangle_to_clip.point_matrix)
		out_triangle2 = Triangle(np.array([[0,0,0,1],[0,0,0,1],[0,0,0,1]]))
		#out_triangle2.point_matrix[]
		if debug:
			print("!!!!!!!!!!!!!!!!!\n\n\n")
			print("inside_points[1] = " + str(inside_points[1]))
			print("out_triangle1.point_matrix[2] = " + str(out_triangle1.point_matrix[2]))
			print("intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[1], bullshit, debug=True) =" + str(intersection_between_plane_and_line(point_on_plane, plane_normal, inside_points[1], bullshit, debug=True)))
			print("All of inside points: ")
			print(inside_points)
			print("Outside points: ")
			print(outside_points)
			print("out_triangle1:")
			print(out_triangle1.point_matrix)
			print("!!!!!!!!!!\n\n\n")
		out_triangle2.point_matrix[0] = inside_points[1]
		out_triangle2.point_matrix[1] = out_triangle1.point_matrix[2]
		paskaperse = copy.deepcopy(inside_points[1])
		out_triangle2.point_matrix[2] = intersection_between_plane_and_line(point_on_plane, plane_normal, paskaperse, bullshit, debug=True)
		
		bullshit_after = bullshit

		if not np.array_equal(bullshit_before, bullshit_after):
			print("FEFUEOFG")
			exit()
		if debug:
			if np.array_equal(bullshit_before, bullshit_after):
				print("VERY GOOD!")
		if debug:
			print("First output triangle:")
			print(out_triangle1.point_matrix)
			print("Second output triangle: ")
			print(out_triangle2.point_matrix)
			print("Original input triangle: ")
			print(triangle_to_clip.point_matrix)

		out_triangle1.color = triangle_to_clip.color
		out_triangle2.color = triangle_to_clip.color

		return 2, [out_triangle1,out_triangle2]
	print("Bullshit: ")
	return 0

def load_object_file(filename: str, offset: np.array) -> list:
	fh = open(filename, "r")
	lines = fh.readlines()
	fh.close()

	vertices = []
	return_triangles = []
	for line in lines:
		list_thing = line.split(" ")
		if list_thing[0] == "v":
			# vertice
			vertices.append(np.array([float(list_thing[1]), float(list_thing[2]), float(list_thing[3])]))
			
		if list_thing[0] == "f":
			appendable_thing = Triangle(np.array([vertices[int(list_thing[1]) - 1], vertices[int(list_thing[2]) - 1], vertices[int(list_thing[3]) - 1]]))
			for i in range(3):
				appendable_thing.point_matrix[i] += offset
			return_triangles.append(appendable_thing)
	return return_triangles

def drawtriangle(turtleobj, triangle_obj, color):
	#turtle.penup()
	turtle.goto(triangle_obj.point_matrix[0][0], triangle_obj.point_matrix[0][1])
	turtle.pendown()
	# calculate color

	turtle.fillcolor(color)
	turtle.color(color)
	turtle.begin_fill()
	turtle.goto(triangle_obj.point_matrix[1][0], triangle_obj.point_matrix[1][1])
	turtle.goto(triangle_obj.point_matrix[2][0], triangle_obj.point_matrix[2][1])
	turtle.goto(triangle_obj.point_matrix[0][0], triangle_obj.point_matrix[0][1])
	turtle.end_fill()
	turtle.penup()
	#print("SHIIITT")
	return

def normalise_vector(vector: np.array):
	if float(np.linalg.norm(vector)) == 0.0:
		print("Sum squared shit: " + str(np.sum(vector**2)))

		return vector
	return vector/np.linalg.norm(vector)


def project_triangle_from_2d_to_3d(triangle: Triangle, projection_matrix: np.array):
	for i in range(3):
		triangle.point_matrix[i] = np.dot(triangle.point_matrix[i], projection_matrix)
	return triangle
'''
def drawborder(screenwidth, screenheight, turtleobj):
	turtleobj.penup()
	turtleobj.goto(-1*screenwidth/2, -1*screenheight/2)
	turtleobj.setheading(0)
	turtleobj.pendown()
	turtleobj.forward(screenwidth)
	turtleobj.left(90)
	turtleobj.forward(screenheight)
	turtleobj.left(90)
	turtleobj.forward(screenwidth)
	turtleobj.left(90)
	turtleobj.forward(screenheight)
	turtleobj.penup()
'''

'''

def drawborder(screenwidth, screenheight, turtleobj):
	turtle.penup()
	turtle.goto(-1*screenwidth/2, -1*screenheight/2)
	turtle.setheading(0)
	turtle.pendown()
	turtle.forward(screenwidth)
	turtle.left(90)
	turtle.forward(screenheight)
	turtle.left(90)
	turtle.forward(screenwidth)
	turtle.left(90)
	turtle.forward(screenheight)
	turtle.penup()

'''

def drawborder(screenwidth, screenheight, turtleobj):
	turtle.speed(0)
	turtle.penup()
	turtle.goto(-1*screenwidth, -1*screenheight)
	turtle.setheading(0)
	turtle.pendown()
	turtle.forward(screenwidth*2)
	turtle.left(90)
	turtle.forward(screenheight*2)
	turtle.left(90)
	turtle.forward(screenwidth*2)
	turtle.left(90)
	turtle.forward(screenheight*2)
	turtle.penup()




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
			#print(point_strings)
			point1_str = point_strings[0]
			point2_str = point_strings[1]
			point3_str = point_strings[2]

			shit = point1_str.split(" ")
			#print("shit:")
			#print(shit)
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
			#print("Final triangle: ")
			#print(np.array([first_point, second_point, third_point]))
			point_strings = []
		else:
			point_strings.append(line)
	#print("Length of all_triangles: " + str(len(all_triangles)))
	#print(len(new_lines)/4)
	#print(actual_lines)
	return all_triangles



'''

def get_surface_normal_for_triangle(triangle_obj):
	U = triangle_obj.point_matrix[1] - triangle_obj.point_matrix[0]
	V = triangle_obj.point_matrix[2] - triangle_obj.point_matrix[0]

	normal = np.array([0,0,0,0])

	normal[0] = (U[1]*V[2]) - (U[2]*V[1])
	normal[1] = (U[2]*V[0]) - (U[0]*V[2])
	normal[2] = (U[0]*V[1]) - (U[1]*V[0])
	#print("Normal: " + str(normal))
	print("Normalised normal: " + str(normalise_vector(normal)))

	print("Triangle matrix:")
	print(triangle_obj.point_matrix)
	return normalise_vector(normal)

'''

def get_surface_normal_for_triangle(triangle_obj):
	line1 = triangle_obj.point_matrix[1] - triangle_obj.point_matrix[0]
	line2 = triangle_obj.point_matrix[2] - triangle_obj.point_matrix[0]
	normal = np.cross(line1[0:3],line2[0:3])
	#print(normal)
	#normal[3] = 0
	normal = normalise_vector(normal)
	normal = np.append(normal, [0])
	return normal













'''


def getcolor(triangle_obj, sun_dir):
	normal = get_surface_normal_for_triangle(triangle_obj)
	print("Normal: " + str(normal))

	coloof = abs(np.dot(normal, sun_dir))
	coloof *= 255
	coloof = round(coloof)
	hex_shit = hex(coloof)
	hex_shit = hex_shit[2:]

	color = "#"+hex_shit*3
	return color


'''

def getcolor(triangle_obj, sun_dir):
	normal = get_surface_normal_for_triangle(triangle_obj)
	#print("Normal: " + str(normal))
	#print(normal)
	coloof = abs(np.dot(normal, sun_dir))
	coloof = max(0, coloof)

	#print(coloof)
	coloof *= 255
	coloof = round(coloof)
	hex_shit = hex(coloof)
	hex_shit = hex_shit[2:]
	#if hex_shit != "93" and hex_shit != "00":
	#	print("Quite shit")
	#	exit()
	if len(hex_shit) == 1:
		hex_shit = "0"+hex_shit

	color = "#"+hex_shit*3
	return color


def get_camera_forward_vector(camera: Camera):
	forward = np.array([0,0,1,0])
	forward = np.dot(forward, camera.get_x_rotation_matrix())
	forward = np.dot(forward, camera.get_y_rotation_matrix())
	forward = np.dot(forward, camera.get_z_rotation_matrix())
	return forward

'''
def load_smd_frame(time, triangles, anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0])):
	
	if anim_filename == None:
		return triangles
	else:
		# at this point the triangles are in triangles and we need to modify the list:
		fh = open(anim_filename, "r")
		lines = fh.readlines()
		fh.close()
		counter = 0
		while "time "+str(time) not in lines[counter]:
			counter += 1
		counter+=1
		anim_lines = []
		while "time" not in lines[counter]:
			anim_lines.append(lines[counter].split(" "))
			print(lines[counter].split(" "))
			counter += 1
	return triangles
'''


'''
def load_smd_frame(time, triangles, anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0])):
	

	# at this point the triangles are in triangles and we need to modify the list:
	fh = open(anim_filename, "r")
	lines = fh.readlines()
	fh.close()
	counter = 0
	while "time "+str(time) not in lines[counter]:
		counter += 1
	counter+=1
	anim_lines = []
	while "time" not in lines[counter]:
		appendable_thing = lines[counter].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		anim_lines.append(appendable_thing)
		#print(lines[counter].split(" "))
		counter += 1
	thing = 0
	for animated_triangle in anim_lines:
		point_in_triangle = thing % 3

		triangle = int(math.floor(thing/3))


		#new_triangle = Triangle()
		
		triangles[triangle].point_matrix[point_in_triangle] = np.array([float(animated_triangle[1]), float(animated_triangle[2]), float(animated_triangle[3]), triangles[triangle].point_matrix[point_in_triangle, 3]])
		thing += 1


	return triangles

'''
'''

def load_vta_frame(time, triangles, base_filename, anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0]), add=False):
	

	# at this point the triangles are in triangles and we need to modify the list:
	fh = open(anim_filename, "r")
	lines = fh.readlines()
	fh.close()
	print("Triangle number 150 in the original triangles: ")
	print(triangles[149].point_matrix)

	counter = 0
	while "vertexanimation" not in lines[counter]:
		counter += 1
	while "time "+str(time) not in lines[counter]:
		counter += 1
	counter+=1
	anim_lines = []
	vertices = load_smd_vertices(base_filename, offset)
	print("Vertices for triangles number 150 from load_smd_vertices: ")
	print(vertices[149*3:150*3])
	shit = 0
	while "time" not in lines[counter]:
		appendable_thing = lines[counter].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#anim_lines.append(appendable_thing)
		#print(lines[counter].split(" "))
		# we need to generate the new vector:
		print("Vertices before modifying: ")
		
		print(vertices[int(appendable_thing[0])])
		print("Appendable thing:")
		print(appendable_thing)
		print(appendable_thing[1:4])
		# ['4.208581', '-7.113604', '54.759979']
		if appendable_thing[1:4] == ["4.208581", "-7.113604", "54.759979"]:
			print("ok so now is the important thing:")
			print("Current line: ")
			print(appendable_thing)
			print("The vertex which we are replacing: ")
			print(vertices[int(appendable_thing[0])])
		if add:

			vertices[int(appendable_thing[0])][0] += float(appendable_thing[1])
			vertices[int(appendable_thing[0])][1] += float(appendable_thing[2])
			vertices[int(appendable_thing[0])][2] += float(appendable_thing[3])
		else:
			vertices[int(appendable_thing[0])][0] = float(appendable_thing[1])
			vertices[int(appendable_thing[0])][1] = float(appendable_thing[2])
			vertices[int(appendable_thing[0])][2] = float(appendable_thing[3])
		print("Modified vertex: " + str(int(appendable_thing[0])))
		print(lines[counter])

		counter += 1
		shit += 1
	print("Modified triangles: " + str(shit))
	print("Vertices for triangles[149]: " + str(vertices[149*3:149*3++3]))
	returned_triangles = triangles_from_vertices(vertices)
	print("Triangle number 150 in the resulting triangles: ")
	print(returned_triangles[149].point_matrix)
	return returned_triangles
'''


'''

import pickle 
object = Object() 
filehandler = open(filename, 'w') 
pickle.dump(object, filehandler)

'''

import pickle




def construct_vertices_dict(vertices): # Generates a search dictionary.

	out = {}

	for i, vert in enumerate(vertices):
		x, y, z = copy.deepcopy(vert[0]), copy.deepcopy(vert[1]), copy.deepcopy(vert[2])
		if vert[0] == float("-0.120362"):
			print("FUUCCCK")
			exit(0)

		if x == -0.120362:
			print("qqqq")
			exit(0)

		if x not in out:
			out[x] = {} # Create new thing.
		
		if y not in out[x]:
			out[x][y] = {}
		if z not in out[x][y]:
			out[x][y][z] = [i]
		else:
			#assert False
			assert isinstance(out[x][y][z], list)
			out[x][y][z].append(i) # Just add the thing.

	return out # Return the thing.


def load_vta_frame(time, triangles, base_filename, anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0]), add=False):
	

	# at this point the triangles are in triangles and we need to modify the list:
	fh = open(anim_filename, "r")
	lines = fh.readlines()
	fh.close()
	print("Triangle number 150 in the original triangles: ")
	print(triangles[149].point_matrix)

	counter = 0
	while "vertexanimation" not in lines[counter]:
		counter += 1
	

	while "time 0" not in lines[counter]:
		counter += 1

	counter += 1

	vertices = load_smd_vertices(base_filename, offset)
	oof = counter

	vertice_shit = {}

	print("lines == "+str(lines))

	filehandler = open("lines.pickle", 'bw') 
	pickle.dump(lines, filehandler)
	filehandler.close()

	filehandler = open("vertices.pickle", 'bw') 
	pickle.dump(vertices, filehandler)
	filehandler.close()

	vertices_dict = construct_vertices_dict(vertices)

	while "time 1" not in lines[oof]:

		another = 0
		appendable_thing = lines[oof].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#print(appendable_thing)

		'''
		
		found = False
		for vertice in vertices:
			#print("bullshit")
			#print(appendable_thing)
			
			if vertice[0] == float(appendable_thing[1]) and vertice[1] == float(appendable_thing[2]) and vertice[2] == float(appendable_thing[3]):
				if int(appendable_thing[0]) not in vertice_shit.keys():
					vertice_shit[int(appendable_thing[0])] = [another]
					found = True
					#break
				else:
					found = True
					vertice_shit[int(appendable_thing[0])].append(another)
					#break
				# 
			another += 1
		assert found # We should always find atleast one corresponding thing.


		'''


		
		'''


while "time 1" not in lines[oof]:

	another = 0
	appendable_thing = lines[oof].split(" ")
	appendable_thing = remove_values_from_list(appendable_thing, "")
	#print(appendable_thing)
	for vertice in vertices:
		#print("bullshit")
		#print(appendable_thing)
		if vertice[0] == float(appendable_thing[1]) and vertice[1] == float(appendable_thing[2]) and vertice[2] == float(appendable_thing[3]):
			if int(appendable_thing[0]) not in vertice_shit.keys():
				vertice_shit[int(appendable_thing[0])] = [another]

			else:
				vertice_shit[int(appendable_thing[0])].append(another)

			#
		another += 1
	oof += 1

	if oof % 1000 == 0:
		print(oof)
print("Done")

'''

		
		found = True

		if float(appendable_thing[1]) not in vertices_dict or float(appendable_thing[2]) not in vertices_dict[float(appendable_thing[1])] or float(appendable_thing[3]) not in vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])]:
			another = len(vertices) - 1 # Just a handy shortcut. This is to handle the things.
			found = False
		else:

			assert float(appendable_thing[1]) in vertices_dict
			assert float(appendable_thing[2]) in vertices_dict[float(appendable_thing[1])]
			assert float(appendable_thing[3]) in vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])]
			orig_len = len(vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])])
			assert vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])] != [] # Should have something
			another = vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])][0] # Just use the first index


			# Remove the first index.

			vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])].pop(0)

			# vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])].pop(0)
			# print("vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])] == "+str(vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])]))
			# new_len = len(vertices_dict[float(appendable_thing[1])][float(appendable_thing[2])][float(appendable_thing[3])])
			# assert new_len == orig_len - 1 # Sanity

		# Now another is the correct index into the vertices list.

		# if int(appendable_thing[0]) not in vertice_shit.keys():

		



		if found:

			if int(appendable_thing[0]) not in vertice_shit.keys():
				vertice_shit[int(appendable_thing[0])] = [another]
				print("int(appendable_thing[0]) == "+str(int(appendable_thing[0])))
				print("vertice_shit[int(appendable_thing[0])] == "+str(vertice_shit[int(appendable_thing[0])]))
			else:
				assert False
				vertice_shit[int(appendable_thing[0])].append(another)
				print("int(appendable_thing[0]) == "+str(int(appendable_thing[0])))
				print("vertice_shit[int(appendable_thing[0])] == "+str(vertice_shit[int(appendable_thing[0])]))



		oof += 1

		if oof % 1000 == 0:
			print(oof)
	print("Done")



	while "time "+str(time) not in lines[counter]:
		counter += 1
	counter+=1
	anim_lines = []
	
	print("Vertices for triangles number 150 from load_smd_vertices: ")
	print(vertices[149*3:150*3])
	shit = 0




	while "time" not in lines[counter]:
		appendable_thing = lines[counter].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#anim_lines.append(appendable_thing)
		#print(lines[counter].split(" "))
		# we need to generate the new vector:
		print("Vertices before modifying: ")
		
		print(vertices[int(appendable_thing[0])])
		print("Appendable thing:")
		print(appendable_thing)
		print(appendable_thing[1:4])
		# ['4.208581', '-7.113604', '54.759979']
		if appendable_thing[1:4] == ["4.208581", "-7.113604", "54.759979"]:
			print("ok so now is the important thing:")
			print("Current line: ")
			print(appendable_thing)
			print("The vertex which we are replacing (index): ")
			print(vertice_shit[int(appendable_thing[0])])
			print("Actual:")
			#print(vertices[vertice_shit[int(appendable_thing[0])]])

		for poopoo in vertice_shit[int(appendable_thing[0])]:
			if add:

				vertices[poopoo][0] += float(appendable_thing[1])
				vertices[poopoo][1] += float(appendable_thing[2])
				vertices[poopoo][2] += float(appendable_thing[3])
			else:
				vertices[poopoo][0] = float(appendable_thing[1])
				vertices[poopoo][1] = float(appendable_thing[2])
				vertices[poopoo][2] = float(appendable_thing[3])
		#print("Modified vertex: " + str(int(appendable_thing[0])))
		#print(lines[counter])

		counter += 1
		shit += 1
	#print("Modified triangles: " + str(shit))
	#print("Vertices for triangles[149]: " + str(vertices[149*3:149*3++3]))
	returned_triangles = triangles_from_vertices(vertices)
	#print("Triangle number 150 in the resulting triangles: ")
	#print(returned_triangles[149].point_matrix)
	return returned_triangles

def load_smd_initial(triangles, base_filename, anim_filename=None,  offset=np.array([0.0,0.0,0.0,0.0])):
	fh = open(anim_filename, "r")
	lines = fh.readlines()
	fh.close()
	print("Triangle number 150 in the original triangles: ")
	print(triangles[149].point_matrix)

	counter = 0
	while "skeleton" not in lines[counter]:
		counter += 1
	

	while "time 0" not in lines[counter]:
		counter += 1

	counter += 1

	vertices = load_smd_vertices(base_filename, offset)
	oof = counter
	vertice_shit = {}

	thing_thing = 0
	print("SHIT")
	for vertice in vertices:
		print(vertice)
	while "time 1" not in lines[oof]:
		print("loop")
		another = 0
		appendable_thing = lines[oof].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#print(appendable_thing)
		thing_counter = 0
		for vertice in vertices:
			#print("bullshit")
			#print(appendable_thing)
			#print("appendable_thing[0]" + str(appendable_thing[0]))
			if '-0.410169' in appendable_thing:
				print("Appendable thing:")
				print(appendable_thing)
				print("Vertice: " + str(vertice))
				if float('-0.410169') in vertice:
					print("KKKKKK")
			if vertice[0] == float(appendable_thing[1]) and vertice[1] == float(appendable_thing[2]) and vertice[2] == float(appendable_thing[3]):
				if int(appendable_thing[0]) not in vertice_shit.keys():
					vertice_shit[int(appendable_thing[0])] = [another]

				else:
					vertice_shit[int(appendable_thing[0])].append(another)

				# 
			another += 1
			thing_counter += 1
		oof += 1

		if oof % 1000 == 0:
			print(oof)
	print("Vertice_shit in the initial: ")
	print(vertice_shit)
	print("Done")
	return vertices, vertice_shit, counter




def load_smd_frame(time, triangles, base_filename, vertices, vertice_shit, counter,anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0]), add=False):
	

	# at this point the triangles are in triangles and we need to modify the list:
	'''
	oof = counter
	vertice_shit = {}

	while "time 1" not in lines[oof]:

		another = 0
		appendable_thing = lines[oof].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#print(appendable_thing)
		for vertice in vertices:
			#print("bullshit")
			#print(appendable_thing)
			if vertice[0] == float(appendable_thing[1]) and vertice[1] == float(appendable_thing[2]) and vertice[2] == float(appendable_thing[3]):
				if int(appendable_thing[0]) not in vertice_shit.keys():
					vertice_shit[int(appendable_thing[0])] = [another]

				else:
					vertice_shit[int(appendable_thing[0])].append(another)

				# 
			another += 1
		oof += 1

		if oof % 1000 == 0:
			print(oof)
	print("Done")
	'''

	fh = open(anim_filename, "r")
	lines = fh.readlines()
	fh.close()

	while "time "+str(time) not in lines[counter]:
		counter += 1
	counter+=1
	anim_lines = []
	
	print("Vertices for triangles number 150 from load_smd_vertices: ")
	print(vertices[149*3:150*3])
	shit = 0




	while "time" not in lines[counter]:
		appendable_thing = lines[counter].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#anim_lines.append(appendable_thing)
		#print(lines[counter].split(" "))
		# we need to generate the new vector:
		print("Vertices before modifying: ")
		
		print(vertices[int(appendable_thing[0])])
		print("Appendable thing:")
		print(appendable_thing)
		print(appendable_thing[1:4])
		# ['4.208581', '-7.113604', '54.759979']
		if appendable_thing[1:4] == ["4.208581", "-7.113604", "54.759979"]:
			print("ok so now is the important thing:")
			print("Current line: ")
			print(appendable_thing)
			print("The vertex which we are replacing (index): ")
			print(vertice_shit[int(appendable_thing[0])])
			print("Actual:")
			#print(vertices[vertice_shit[int(appendable_thing[0])]])
		print("vertice_shit: ")
		print(vertice_shit)

		for poopoo in vertice_shit[int(appendable_thing[0])]:
			if add:

				vertices[poopoo][0] += float(appendable_thing[1])
				vertices[poopoo][1] += float(appendable_thing[2])
				vertices[poopoo][2] += float(appendable_thing[3])
			else:
				vertices[poopoo][0] = float(appendable_thing[1])
				vertices[poopoo][1] = float(appendable_thing[2])
				vertices[poopoo][2] = float(appendable_thing[3])
		#print("Modified vertex: " + str(int(appendable_thing[0])))
		#print(lines[counter])

		counter += 1
		shit += 1
	#print("Modified triangles: " + str(shit))
	#print("Vertices for triangles[149]: " + str(vertices[149*3:149*3++3]))
	returned_triangles = triangles_from_vertices(vertices)
	#print("Triangle number 150 in the resulting triangles: ")
	#print(returned_triangles[149].point_matrix)
	return returned_triangles

def triangles_from_vertices(verts):
	tris = []
	debug = False
	for k in range(int(len(verts)/3)):
		if k == 149:
			debug = True
		#mat = np.array([[0,0,0],[0,0,0],[0,0,0]])
		'''
		for i in range(3):
			if debug:
				print("Here is the buggy shit: ")
				print(verts[k*3+i:k*3+i+3])
				debug=False
			mat[i] = verts[k*3+i]
			print("Current matrix: ")
			print(mat[i])
			print("verts[k*3+i]: ")
			print(verts[k*3+i])
		'''

		point1 = verts[k*3]
		point2 = verts[k*3+1]
		point3 = verts[k*3+2]
		tris.append(Triangle(np.array([point1, point2, point3])))
	return tris



def load_smd_vertices(filename: str, offset: np.array):


	filehandle = open(filename, "r")

	lines = filehandle.readlines()

	filehandle.close()
	count = 0
	while "triangles" not in lines[count]:
		print(lines[count])

		count += 1
	new_lines = lines[count:]

	actual_lines = []
	all_triangles = []
	count = 0
	point_strings = []
	offset = offset[0:3]
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
			#print(point_strings)
			point1_str = point_strings[0]
			point2_str = point_strings[1]
			point3_str = point_strings[2]

			shit = point1_str.split(" ")
			#print("shit:")
			#print(shit)
			shit = remove_values_from_list(shit, "")
			# shit[0] = parent bone
			# shit[1:4] = {x,y,z}

			first_point = np.array([float(shit[1]), float(shit[2]), float(shit[3])])
			first_point += offset
			shit = point2_str.split(" ")
			shit = remove_values_from_list(shit, "")
			second_point = np.array([float(shit[1]), float(shit[2]), float(shit[3])])
			second_point += offset

			shit = point3_str.split(" ")
			shit = remove_values_from_list(shit, "")
			third_point = np.array([float(shit[1]), float(shit[2]), float(shit[3])])
			third_point += offset

			all_triangles.append(first_point)
			all_triangles.append(second_point)
			all_triangles.append(third_point)
			#print("Final triangle: ")
			#print(np.array([first_point, second_point, third_point]))
			point_strings = []
		else:
			point_strings.append(line)
	#print("Length of all_triangles: " + str(len(all_triangles)))
	#print(len(new_lines)/4)
	#print(actual_lines)
	return all_triangles

def save_layout(filename="Unnamed_Layout"):
	ps = turtle.getscreen().getcanvas().postscript(colormode="color")
	im = Image.open(io.BytesIO(ps.encode("utf-8")))
	im.save(filename, format="PNG")

def load_vta_initial(vta_filename, add=False):

	# at this point the triangles are in triangles and we need to modify the list:
	fh = open(vta_filename, "r")
	lines = fh.readlines()
	fh.close()
	

	counter = 0
	while "vertexanimation" not in lines[counter]:
		counter += 1
	while "time 0" not in lines[counter]:
		counter += 1
	counter+=1
	anim_lines = []
	#vertices = load_smd_vertices(base_filename, offset)
	print("Vertices for triangles number 150 from load_smd_vertices: ")
	#print(vertices[149*3:150*3])
	shit = 0
	vertices = []
	while "time" not in lines[counter]:
		addable_vert = np.array([0,0,0])
		appendable_thing = lines[counter].split(" ")
		appendable_thing = remove_values_from_list(appendable_thing, "")
		#anim_lines.append(appendable_thing)
		#print(lines[counter].split(" "))
		# we need to generate the new vector:
		print("appendable_thing:")
		print(appendable_thing)
		print("Vertices before modifying: ")
		
		#print(vertices[int(appendable_thing[0])])
		if add:

			addable_vert[0] += float(appendable_thing[1])
			addable_vert[1] += float(appendable_thing[2])
			addable_vert[2] += float(appendable_thing[3])
		else:
			addable_vert[0] = float(appendable_thing[1])
			addable_vert[1] = float(appendable_thing[2])
			addable_vert[2] = float(appendable_thing[3])
		
		vertices.append(addable_vert)
		counter += 1
		shit += 1
	
	returned_triangles = triangles_from_vertices(vertices)
	
	return returned_triangles

if __name__=="__main__":
	#turtle.fill_color('#FFFFFF')
	turtle.tracer(0,0)
	#screenwidth = 3000
	#screenheight = 3000
	screenwidth = 1920
	screenheight = 1080
	when_to_draw = 1000
	#sun_direction = normalise_vector(np.array([1,1,1,0]))
	point_arr = np.array([[1.1400000e-02,-1.0083000e+00,3.8222301e+01,1.0000000e+00],[2.2200000e-02,-1.0308000e+00,3.8209801e+01,1.0000000e+00],[1.5400000e-02,-9.9790000e-01,3.8223801e+01,1.0000000e+00]])
	#point_arr *= 100
	
	#triangle = Triangle(np.array([[0.0,0.0,15.0,1.0], [0.0,-20.0,15.0,1.0], [-20.0,-20.0,15.0,1.0]]))
	#triangle = Triangle(point_arr)
	#triangles = [triangle]
	
	#triangles = load_object_file("/home/cyberhacker/ball2.obj", np.array([0,0,10.0,0]))
	triangles = load_smd("/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", np.array([0.0,0.0,0.0,0.0]))
	vertices, vertice_shit, counter = load_smd_initial(triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_anims/idle_bouncetest.smd")
	# def load_smd_initial(triangles, base_filename, anim_filename=None):
	'''
	old_third_triangle = copy.deepcopy(triangles[2])
	old_triangles = copy.deepcopy(triangles)
	print("Amount of vertices: " + str(len(triangles)*3))
	'''

	#triangles = load_object_file("./axis.obj", np.array([0,0,5.0,0]))
	# we need to rotate the first element aka camera_rotation[0] = pi/2
	#cameraPos = np.array([0.0,-70.0,38.01,1.0])
	#cameraPos = np.array([0.0,-15.0,53.01,1.0])
	cameraPos = np.array([0.0,-20.0,53.01,1.0])
	#cameraPos = np.array([0.0,0.0,0.0,1.0])
	camera_rotation = np.array([math.pi/2,0.0,0.0,1.0])
	#camera_rotation = np.array([0.0,0.0,0.0,1.0])
	camera = Camera(cameraPos, camera_rotation)
	sun_direction = normalise_vector(get_camera_forward_vector(camera))
	#transformed_point = camera.transform_point(triangle.point_matrix[0])
	
	turtleobj = turtle.Turtle()
	turtleobj.speed(0)
	turtle.speed(0)

	field_of_view = math.pi/2
	ratio = 1

	# first make camera transform for each triangle in triangles
	
	how_many_cycles = 1
	debug = False
	forward_speed = 1
	#for count in range(how_many_cycles):
	rotate_speed = 0.1
	#while True:
	
	
	time = 1
	#while True:
	#for count in range(how_many_cycles):
	#triangles = []
	#triangles = load_vta_frame(0, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta", add=True)
	#triangles = load_vta_initial("/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta")
	while True:
		#triangles = load_smd_frame(time, triangles, anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_anims/replaced.smd")
		#triangles = load_vta_frame(24, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta", add=False)
		triangles = load_smd_frame(time, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", vertices,vertice_shit, counter,anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_anims/idle_bouncetest.smd", add=False)
		# (time, triangles, base_filename, vertices, vertice_shit,anim_filename=None, offset=np.array([0.0,0.0,0.0,0.0]), add=False):
		time += 1
		#new_third_triangle = copy.deepcopy(triangles[2])
		shit = 0
		#print(tri.point_matrix)
		'''
		for tri in triangles:

			if np.array_equal(tri.point_matrix, old_triangles[shit].point_matrix):
				print("FUCK")
				exit()
			shit += 1
		'''


		

		triangles_to_sort = []
		

		# get user input



		if keyboard.is_pressed("w"):
			camera.pos += np.array([0.0,0,1,0])*forward_speed
		if keyboard.is_pressed("a"):
			camera.pos += np.array([-1.0,0,0,0])*forward_speed
		if keyboard.is_pressed("s"):
			camera.pos += np.array([0.0,0,-1,0])*forward_speed

		if keyboard.is_pressed("d"):
			camera.pos += np.array([1.0,0,0,0])*forward_speed

		if keyboard.is_pressed("f"):
			camera.pos += np.array([0,1.0,0,0])*forward_speed

		if keyboard.is_pressed("g"):
			camera.pos += np.array([0,-1.0,0,0])*forward_speed



		if keyboard.is_pressed("p"):
			camera.rotate_vector += np.array([1.0,0.0,0.0,0.0])*rotate_speed
		if keyboard.is_pressed("o"):
			camera.rotate_vector += np.array([-1.0,0.0,0.0,0.0])*rotate_speed
		if keyboard.is_pressed("k"):
			camera.rotate_vector += np.array([0.0,-1.0,0.0,0.0])*rotate_speed
		if keyboard.is_pressed("l"):
			camera.rotate_vector += np.array([0.0,1.0,0.0,0.0])*rotate_speed
		if keyboard.is_pressed("n"):
			camera.rotate_vector += np.array([0.0,0.0,-1.0,0.0])*rotate_speed
		if keyboard.is_pressed("m"):
			camera.rotate_vector += np.array([0.0,0.0,1.0,0.0])*rotate_speed

		camera_transformed_points = 0
		previous_thing = None
		for triangle in triangles:
			# first do the camera transform for the point:

			triangle.normal = get_surface_normal_for_triangle(triangle)
			triangle.setcolor(sun_direction)
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

			thing_thing = copy.deepcopy(triangle_oof.point_matrix[0,2])

			number_of_clipped_triangles, out_triangles = cliptriangleagainstplane(np.array([0,0,1,1]), np.array([0,0,1,0]), triangle_oof, debug=debug)
			#if number_of_clipped_triangles != 0:
			#	oof_oof = copy.deepcopy(out_triangles[0].point_matrix[0,2])
			#	print("Thingthing: " + str(out_triangles[0].point_matrix[0][2]))
			#	if thing_thing != oof_oof:
			#		print("qqq")
			#		exit()

			if debug:
				print("-------------\n\n")
				print(out_triangles[0].point_matrix)
			for i in range(number_of_clipped_triangles):

				projection_matrix = get_perspective_projection_matrix(field_of_view, ratio, 0.1, 100)
				#print("Projection matrix:")
				#print(projection_matrix)
				#print("\n\n")
				if debug:
					print("----------------\n\n\n\nPerspective projection matrix: ")
					print(projection_matrix)
					print("--------------------\n\n\n")

				if debug:
					print("-----------------------\n\n\nProjection phase:\n\n")
					print("Original triangle:")
					print(out_triangles[i].point_matrix)
				
				for k in range(3):
					out_triangles[i].point_matrix[k,3] = 1.0
				#print("POOPOO: ")
				#print(out_triangles[i].point_matrix)
				out_triangles[i] = project_triangle_from_2d_to_3d(out_triangles[i], projection_matrix)

				#print("aaaaaaaaa: " + str(out_triangles[i].point_matrix[0][2]))
				#print("aaaaaaaaa: " + str(out_triangles[i].point_matrix[1][2]))
				#print("aaaaaaaaa: " + str(out_triangles[i].point_matrix[2][2]))
				
				# divide each point vector by the value of w to convert back to cartesian coordinates

				out_triangles[i].point_matrix = out_triangles[i].point_matrix.astype(float)
				#print("PEEPEE: ")
				#print(out_triangles[i].point_matrix)
				for q in range(3):
					#print(out_triangles[i].point_matrix)
					out_triangles[i].point_matrix[q] /= float(out_triangles[i].point_matrix[q][3])
					out_triangles[i].point_matrix[q, 0] *= -1
					out_triangles[i].point_matrix[q, 1] *= -1
				#print("FARDFARD: ")
				#print(out_triangles[i].point_matrix)
				if previous_thing != None:

					if abs(out_triangles[i].point_matrix[0][3] - 1.0010010010010009) != previous_thing:
						print("Paska")
						print(abs(out_triangles[i].point_matrix[0][3] - 1.0010010010010009))
						exit()
				else:
					previous_thing = abs(out_triangles[i].point_matrix[0][3] - 1.0010010010010009)
				

				#print("bbbbbbbbb: " + str(out_triangles[i].point_matrix[0][2]))
				#print("bbbbbbbbb: " + str(out_triangles[i].point_matrix[1][2]))
				#print("bbbbbbbbb: " + str(out_triangles[i].point_matrix[2][2]))

				if debug:
					print("Resulting triangle: ")
					print(out_triangles[i].point_matrix)
					print("----------------------\n\n\n")


				# offset into normalised space
				#if camera_transformed_points % 1000 == 0:
				#	print(camera_transformed_points)
				#voffset = np.array([1,1,0,0])
				voffset = np.array([0.01,0.01,0,0])
				for k in range(3):
					out_triangles[i].point_matrix[k] = out_triangles[i].point_matrix[k] + voffset
					

				for j in range(3):
					out_triangles[i].point_matrix[j][0] = out_triangles[i].point_matrix[j][0] * (0.5 * screenwidth)
					out_triangles[i].point_matrix[j][1] = out_triangles[i].point_matrix[j][1] * (0.5 * screenheight)

				if debug:
					print("Triangle after scaling and offset: ")
					print(out_triangles[i].point_matrix)
				triangles_to_sort.append(out_triangles[i])
				camera_transformed_points += 1












		
		'''
		for triangle_thing in triangles_to_sort:
			print("Bullshit: eee")
			print(triangle_thing.point_matrix)
		'''





		triangles_sorted = sorted(triangles_to_sort, key=lambda x: (x.point_matrix[0][2]+x.point_matrix[1][2]+x.point_matrix[2][2])/3.0, reverse=True) # first point and the z coordinate
		

		'''

		for triangle_thing in triangles_sorted:
			#x = triangle_thing
			print("Thing: ")
			print((triangle_thing.point_matrix[0][2]+triangle_thing.point_matrix[1][2]+triangle_thing.point_matrix[2][2])/3.0)

		'''

		#print(triangles_sorted)
		# clip each triangle and draw them:


		

		drawborder(screenwidth, screenheight, turtleobj)
		triangle_count = 0
		all_triangles = []
		oofcount = 0
		turtle.clearscreen()
		prev_z = 0
		turtle.tracer(0,0)
		for triangle in triangles_sorted:
			#if (triangle.point_matrix[0][2]+triangle.point_matrix[1][2]+triangle.point_matrix[2][2])/3.0<prev_z:
			#	print("FUCK")
			#	exit()

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
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,-1*(screenheight)/2+1,0,0]), np.array([0,1,0,0]), cur_triangle)
					if p == 1:
						
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,(screenheight/2)-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=debug)
					if p == 2:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([-screenwidth/2+1,0,0,0]), np.array([1,0,0,0]), cur_triangle)
					if p == 3:

						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([screenwidth/2-1,0,0,0]), np.array([-1,0,0,0]), cur_triangle, debug=debug)
					
					
					'''
					if debug:
						print("Current triangle in clipping: ")
						print(cur_triangle.point_matrix)
						print("Amount of triangles: " + str(how_many_to_add))
						print("List of all the triangles: ")
						for q in range(how_many_to_add):
							print(appended_triangles[q].point_matrix)
					'''
					'''
					
					if how_many_to_add == 0:
						print("----------------------")
						print(p)
						#cliptriangleagainstplane(np.array([0,screenheight-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=True)
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,0,0,0]), np.array([1,0,0,0]), cur_triangle, debug=True)
						exit()
					'''
					
					if oofcount % 100 == 0:
						print("Drawn " + str(oofcount) + " triangles.")
					counter = 0
					for triangle_oof in appended_triangles:
						oofcount += 1
						counter += 1
						current_triangle_list.append(triangle_oof)
				amount_of_new_triangles = len(current_triangle_list)
			#print("Amount of drawn triangles: " + str(len(current_triangle_list)))
			#print(len(current_triangle_list))
			
			for triangle_shit in current_triangle_list:
				triangle_count += 1
				if triangle_count % when_to_draw == 0:
					turtle.update()
				#color = getcolor(triangle_shit, sun_direction)
				#print(color)
				drawtriangle(turtleobj, triangle_shit, triangle_shit.color)
				all_triangles.append(triangle_shit)

		print("Amount of drawn triangles: " + str(triangle_count))
		#print("All triangles: ")
		turtle.update()
		save_layout(filename=str("./frames/frame_"+str(time)+".png"))

		#for triangle_obj in all_triangles:

		#	print(triangle_obj.point_matrix)










