// water
//
// Povray water tutorial:
// http://www.imagico.de/pov/water/index.html

#declare Block8Object = BlockDefaultObject

#declare Block8Material = material {
	texture {
		pigment {
			color rgbt <1, 1, 1, 1>
		}

		finish {
			ambient 0.0
			diffuse 0.0

			reflection {
				0.0, 1.0
				fresnel on
			}

			specular 0.4
			roughness 0.003
		}

		normal {
			function {
				f_ridged_mf(x, y, z, 0.1, 3.0, 7, 0.7, 0.7, 2)
			} 0.8
			scale 0.13
		}
	}

	interior {
		ior 1.333
	}
}
