
from run_animation import *
import time

'''

we basically need to reimplement this loop as a class:

if __name__=="__main__":
	#turtle.fill_color('#FFFFFF')
	turtle.tracer(0,0)
	#self.view_width = 3000
	#self.view_height = 3000
	self.view_width = 1920
	self.view_height = 1080
	when_to_draw = 1000
	#sun_direction = normalise_vector(np.array([1,1,1,0]))
	point_arr = np.array([[1.1400000e-02,-1.0083000e+00,3.8222301e+01,1.0000000e+00],[2.2200000e-02,-1.0308000e+00,3.8209801e+01,1.0000000e+00],[1.5400000e-02,-9.9790000e-01,3.8223801e+01,1.0000000e+00]])
	#point_arr *= 100
	
	#triangle = Triangle(np.array([[0.0,0.0,15.0,1.0], [0.0,-20.0,15.0,1.0], [-20.0,-20.0,15.0,1.0]]))
	#triangle = Triangle(point_arr)
	#triangles = [triangle]
	
	#triangles = load_object_file("/home/cyberhacker/ball2.obj", np.array([0,0,10.0,0]))
	triangles = load_smd("/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", np.array([0.0,0.0,0.0,0.0]))

	

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
	
	
	time = 0
	#while True:
	#for count in range(how_many_cycles):
	#triangles = []
	#triangles = load_vta_frame(0, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta", add=True)
	#triangles = load_vta_initial("/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta")
	while True:
		#triangles = load_smd_frame(time, triangles, anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_anims/replaced.smd")
		triangles = load_vta_frame(24, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta", add=False)
		time += 1
		#new_third_triangle = copy.deepcopy(triangles[2])
		shit = 0
		#print(tri.point_matrix)
		


		

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
					out_triangles[i].point_matrix[j][0] = out_triangles[i].point_matrix[j][0] * (0.5 * self.view_width)
					out_triangles[i].point_matrix[j][1] = out_triangles[i].point_matrix[j][1] * (0.5 * self.view_height)

				if debug:
					print("Triangle after scaling and offset: ")
					print(out_triangles[i].point_matrix)
				triangles_to_sort.append(out_triangles[i])
				camera_transformed_points += 1












		
		




		triangles_sorted = sorted(triangles_to_sort, key=lambda x: (x.point_matrix[0][2]+x.point_matrix[1][2]+x.point_matrix[2][2])/3.0, reverse=True) # first point and the z coordinate
		

		

		#print(triangles_sorted)
		# clip each triangle and draw them:


		

		drawborder(self.view_width, self.view_height, turtleobj)
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
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,-1*(self.view_height)/2+1,0,0]), np.array([0,1,0,0]), cur_triangle)
					if p == 1:
						
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,(self.view_height/2)-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=debug)
					if p == 2:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([-self.view_width/2+1,0,0,0]), np.array([1,0,0,0]), cur_triangle)
					if p == 3:

						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([self.view_width/2-1,0,0,0]), np.array([-1,0,0,0]), cur_triangle, debug=debug)
					
					
					
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





'''

class graphicsengine:
	def __init__(self):
		self.triangles = []
		self.camera = None
		self.view_width = None
		self.view_height = None
		self.camera = Camera(np.array([0.0,0.0,0.0,1.0]), np.array([0.0,0.0,0.0,1.0]))
	def set_screen_size(self,width, height):
		self.view_width = width
		self.view_height = height
	def set_camera_pos(self, new_pos: np.array):
		self.camera.pos = new_pos
	def set_camera_rot(self, new_rot: np.array):
		self.camera.rotate_vector = new_rot
	def add_triangles_from_file(self, filename: str, time=0, animation_filename=""):
		triangles = load_smd(filename, np.array([0.0,0.0,0.0,0.0]))
		if time != 0:
			if animation_filename=="":
				print("Error. animation_filename can not be \"\" .")
				exit(-1)
			triangles = load_vta_frame(time, triangles, filename, anim_filename=animation_filename, add=False)
		self.triangles += triangles
	def render(self):
		self.set_camera_pos(np.array([0.0,-20.0,53.01,1.0]))
		self.set_camera_rot(np.array([math.pi/2,0.0,0.0,1.0]))
		self.set_screen_size(1920, 1080)
		#self.camera.rotate_vector = np.array([math.pi/2,0.0,0.0,1.0])
		#self.camera.pos = np.array([0.0,-20.0,53.01,1.0])
		triangles_to_sort = []
		camera_transformed_points = 0
		previous_thing = None
		sun_direction = normalise_vector(get_camera_forward_vector(self.camera))
		#transformed_point = camera.transform_point(triangle.point_matrix[0])
	
		turtleobj = turtle.Turtle()
		turtleobj.speed(0)
		turtle.speed(0)
		field_of_view = math.pi/2
		ratio = 1
		rotate_speed = 0.1
		forward_speed = 1
		debug = False
		when_to_draw = 1000
		print("Length of triangles: " + str(len(self.triangles)))
		for triangle in self.triangles:
			# first do the camera transform for the point:

			triangle.normal = get_surface_normal_for_triangle(triangle)
			triangle.setcolor(sun_direction)
			triangle_oof = do_camera_transform_for_triangle(triangle, self.camera)

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
					out_triangles[i].point_matrix[j][0] = out_triangles[i].point_matrix[j][0] * (0.5 * self.view_width)
					out_triangles[i].point_matrix[j][1] = out_triangles[i].point_matrix[j][1] * (0.5 * self.view_height)

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


		

		drawborder(self.view_width, self.view_height, turtleobj)
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
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,-1*(self.view_height)/2+1,0,0]), np.array([0,1,0,0]), cur_triangle)
					if p == 1:
						
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([0,(self.view_height/2)-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=debug)
					if p == 2:
						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([-self.view_width/2+1,0,0,0]), np.array([1,0,0,0]), cur_triangle)
					if p == 3:

						how_many_to_add, appended_triangles = cliptriangleagainstplane(np.array([self.view_width/2-1,0,0,0]), np.array([-1,0,0,0]), cur_triangle, debug=debug)
					
					
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
						#cliptriangleagainstplane(np.array([0,self.view_height-1,0,0]), np.array([0,-1,0,0]), cur_triangle, debug=True)
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
		time.sleep(100)
	