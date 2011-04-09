#include "colors.inc"
#include "rad_def.inc"
#include "functions.inc"

global_settings {
	radiosity {
		// http://wiki.povray.org/content/HowTo:Use_radiosity
		Rad_Settings(Radiosity_Normal,off,off)
	}
}
#default {finish{ambient 0}}

#include "textures/all.inc"
#include "block_materials.inc"
#include "objects.pov"

camera {
        location <0,95,-15>
        look_at <16,70,8>
        angle 90
}


sky_sphere {
	   pigment {
	   	   rgb <0.7,0.7,1.0>
	   }
}

light_source {
	     <0,12000,0> White * 2
}
