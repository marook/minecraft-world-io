// ice
#declare Block79Object = BlockDefaultObject

#declare Block79Material = material {
	texture {
		pigment {
			color rgbt <1, 1, 1, 1>
		}

		finish {
			ambient 0.0
			diffuse 0.1

			reflection {
				0.0, 0.6
				fresnel on
			}

			specular 0.2
			roughness 0.003
		}

		normal {
			function {
				f_ridged_mf(x, y, z, 0.1, 3.0, 7, 0.7, 0.7, 2)
			} 0.2
			scale 0.13
		}
	}

	interior {
		ior 1.31
	}
}
