

from graphlib import *


engine = graphicsengine()
if str(input("Haluatko jättiläistissit? ;) (En/kyllä) : ")).lower() == "kyllä":
	bigtits = 24
else:
	bigtits = 0
engine.add_triangles_from_file("/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", bigtits, "/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta")
engine.render()
'''
load_vta_frame(24, triangles, "/home/cyberhacker/Asioita/Jannat/decompile/Soria_Pose_Ref3.smd", anim_filename="/home/cyberhacker/Asioita/Jannat/decompile/soria_nude_01.vta", add=False)

'''


