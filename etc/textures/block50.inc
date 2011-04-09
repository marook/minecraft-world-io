// torch
#declare Block50Object = union {
	light_source {
		<0.5, 1, 0.5>
		color rgb <0.8, 0.5, 0.2> * 3
		adaptive 3
		jitter
		fade_distance 3
		fade_power 2
	}

	box {
		<0.45, 0. 0.45>, <0.55, 0.5, 0.55>
		material {
			texture {
				pigment { rgb <102 / 255, 69 / 255, 41 / 255> }
			}
		}
	}

	merge{
		intersection{
			sphere{<0, 0, 0>, 1}
			box{<-1, -0.00001, -1>, <1, 1, 1>}

			scale <1, 2.5, 1>
		}
		intersection{
			sphere{<0,0,0>, 1}
			box{<-1, -1, -1>, <1, 0+0.01, 1>}
		}

		scale 0.1
		translate <0.5, 0.5, 0.5>

		hollow

		pigment{ color rgbf 1}
		finish { ambient 0 diffuse 0 }
		interior {
			media {
				emission
				color rgb <1.0, 0.75, 0.1> * 10
				intervals 9
				samples 1, 20
				confidence 0.9999
				variance 1/100
				density{
					spherical
					ramp_wave
					turbulence 0.15
					color_map {
						[0.0 color rgb <0.0, 0.0, 0.0>]
						[0.6 color rgb <0.8, 0.3, 0.0>]
						[0.9 color rgb <1.0, 0.8, 0.3>]
						[1.0 color rgb <1.0, 1.0, 0.1>]
					}
					scale <1, 2.5, 1>
				}
			}
		}

	}
}

#declare Block50Material = material {}
