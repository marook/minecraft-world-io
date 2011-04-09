// snow
//
// http://povray.tashcorp.net/tutorials/irtc_2006_0102/

#declare Block78Object = box {
	<0, 0, 0>, <1, 1 / 16, 1>
}

#declare Block78Material = material {
	texture {
		pigment { rgb White }


		finish {
			ambient 0
			diffuse 0.9
			brilliance 1.75
			specular 1.5
			roughness 0.0001
			reflection 0.025
		}

		normal{
			average
			normal_map {
				[ 1 granite 0.5 scale 0.002 turbulence 1 omega 0.4 lambda 1.2 ]
				[ 1 wrinkles 0.75 scale 0.15 ]
			}
		}
	}
}
