// dirt
#declare Block3Object = BlockDefaultObject

#declare Block3Material = material {
	texture {
		pigment {
			bozo
			color_map {
				[ 0.0 rgb <1 / 255, 10 / 255, 2 / 255> ]
				[ 0.2 rgb <85 / 255, 59 / 255, 21 / 255> ]
				[ 0.95 rgb <137 / 255, 107 / 255, 68 / 255> ]
				[ 1.0 rgb <199 / 255, 163 / 255, 49 / 255> ]
			}
			turbulence 0.6
			omega 0.8
			lambda 3.0
			ramp_wave
		 }
		 normal {
			bumps , 1.0
			scale  <0.75, 0.75, 1.0>
			turbulence 0.6
			octaves 5
			omega 0.65
			lambda 3.0
			frequency 0.0
			ramp_wave
		 }
		 finish {
			ambient 0.0
			diffuse 0.4
			specular 0.0002
			roughness 1.0
		 }
	}
}
