#include "colors.inc"
#include "rad_def.inc"
#include "functions.inc"

#include "textures/default.inc"

global_settings {
	radiosity {
		// http://wiki.povray.org/content/HowTo:Use_radiosity
		Rad_Settings(Radiosity_Normal,off,off)
	}
}

#default {finish{ambient 0}}

camera {
        location <-0.4, 1.3, -1.6>
        look_at <0.5, 0.5, 0.5>
        angle 60
}


light_source {
	     <0, 300, 0> White
}

sky_sphere {
	   pigment {
	   	   rgb White
	   }
}

plane {
	<0, 1, 0>, -0.001

	pigment {
		checker color rgb 0.8, color rgb 0.2
		scale 0.5
	}
}
