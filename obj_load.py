
import numpy as np

class Triangle:
	def __init__(self,point_matrix: np.array):
		#print(type(point_matrix.shape))
		#print(point_matrix.shape)
		self.normal = None
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

def load_object_file(filename: str) -> list:
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
			return_triangles.append(Triangle(np.array([vertices[int(list_thing[1]) - 1], vertices[int(list_thing[2]) - 1], vertices[int(list_thing[3]) - 1]])))			
	return return_triangles


if __name__=="__main__":
	filename = "/home/cyberhacker/ball2.obj"
	triangle_list = load_object_file(filename)
	for triangle in triangle_list:
		print(triangle.point_matrix)
