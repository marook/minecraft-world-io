#include "colors.inc"
#include "functions.inc"
#include "textures/default.inc"
#include "textures/block8.inc"

merge {
	merge {
		object { BlockDefaultObject translate <0, 0, 0> }
		object { BlockDefaultObject translate <1, 0, 0> }
		object { BlockDefaultObject translate <0, -1, 0> }
		object { BlockDefaultObject translate <1, -1, 0> }
	}
	
	merge {
		object { BlockDefaultObject translate <0, 0, 1> }
		object { BlockDefaultObject translate <1, 0, 1> }
		object { BlockDefaultObject translate <0, -1, 1> }
		object { BlockDefaultObject translate <1, -1, 1> }
	}

	material { Block8Material }
}

camera {
        location <-0.4, 1.3, -1.6>
        look_at <1.0, 0.5, 0.5>
        angle 60
}


light_source {
	     <-3, 3, -3> White
}

sky_sphere {
	   pigment {
	   	   gradient y
		   color_map {
		   	[0 color Red]
			[1 color Blue]
		   }
		   scale 2
		   translate -1
	   }
}
