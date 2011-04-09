#include "textures/block3.inc"

// grass
#declare Block2MaterialGrass = material {
	texture{
		pigment {
			bozo
			color_map {
				[ 0.0 rgb <98 / 255, 85 / 255, 33 / 255> ]
				[ 0.05 rgb <121 / 255, 113 / 255, 51 / 255> ]
				[ 0.75 rgb <98 / 255, 142 / 255, 47 / 255> ]
				[ 1.0 rgb <50 / 255, 99 / 255, 28 / 255> ]
			}
			turbulence 1.6
			omega 0.8
			lambda 3.0
			ramp_wave
		}
	}
}

#declare Block2Object = union {
	box {
		<0, 0, 0>, <1, 0.9, 1>

		material { Block3Material }
	}

	box {
		<0, 0.9, 0>, <1, 1, 1>

		material { Block2MaterialGrass }
	}
}

#declare Block2Material = material { }
