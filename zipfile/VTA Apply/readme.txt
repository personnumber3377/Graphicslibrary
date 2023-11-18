This application allows you to apply VTA animations to SMD
model files.

The idea is to recover lost original files. The generated
SMD files are compatible to the original ones. So if you use
3ds max for example the generated SMD files can be used as
valid morph targets to their original SMD file - this way
you could for example recover lost original model data
files.

Once you open vtaapply.exe it will ask you which SMD file to
open. The SMD file you open now is the original SMD file to
apply a VTA file to. You do not require to make a safety
copy of it (although I recommend you to do anyway) the app
should never actually write to it, it will only read it.
Once you have selected it, it will request you to select the
VTA file to apply! Again, this VTA file will not be
modified. As VTA files are made of multiple frames, in the
next dialog it will ask you which of the frames to apply.
Please note that frame is not frame - it totally depends on
the VTA exporter you used! I will name two common example:

3ds max VTA export (we're working with 10 frames for the VTA
export):
-first of all the VTA contains a list of base verticles
which are to be changed in the file
-frame  1: vertex animation applied by 10%
-frame  2: by 20%
...
-frame 10: by 100%

So if your VTA file was created by 3ds Max you'll always
want to select the last frame of a file. However
mdldecompiler for example does something totally else:

Mdldecompiler_expressions.vta structure:
-first of all the VTA contains a list of base verticles
which are to be changed in the file
-frame  1: 1 finalized 100% expression
-frame  2: another 100% finalized expression
-frame  3: and another 100% finalized
....

For Max users: It seems to me the Source engine ignores all
frames between the base data and the final frame so most of
your frames are completely useless.. using 1 frame should be
100% sufficient, Source seems to auto-create transitions.

So as you can see mdldecompiler works completely different,
the easiest way to check which frame matches which animation
is to check the qc file:

flexfile "mdldecompiler_expressions.vta" {
          flex "l_blink" frame 1
		  flex "r_blink" frame 2
		  ....
}

This tells us: frame 1 is the l_blink - so most likely
blinking left eye!


Okay back to business: you selected your frame now.. it will
now apply the frame to the SMD file it has in memory (again
the source file will not be touched). After it has applied
the animation (may take some seconds) it will ask you for
the saving place of the new to be created SMD file. Now it
will store the SMD file from memory to your harddisk! And
well.. now you should be able to import that SMD file into
your favorite modelling application!