// glass
#declare Block20Object = BlockDefaultObject

#declare Block20Material = material {
	texture {
		pigment { rgbf <0.97, 0.99, 0.98, 0.9> }

		finish {
			specular 0.6
			roughness 0.002
			ambient 0
			diffuse 0.1
			reflection {
				0.05, 1.0
			}
			conserve_energy
		}
	}

	interior {
		ior 1.5
		// fade_distance 2.0
		// fade_power 2
	}

}
