// sand
#declare Block12Object = BlockDefaultObject

#declare Block12_Waves = normal {
	gradient x
	slope_map {
		[0    <0.5, 1>]   // start in middle and slope up
		[0.4 <1.0, 0>]   // flat slope at top of wave
		[0.65  <0.5,-1>]   // slope down at mid point
		[0.85 <0.0, 0>]   // flat slope at bottom
		[1    <0.5, 1>]   // finish in middle and slope up
	}
	scale 0.15
	warp { turbulence 0.1 octaves 3 lambda 3.0 }
	scale 1.0/0.15
}

#declare Block12Material = material { texture {
 	pigment {colour rgb <0.808, 0.776, 0.588>}
	normal {
		average normal_map {
                       	[0.5 Block12_Waves 1.0]
                       	[0.5 wrinkles 1 scale 0.0025]
                }
        }
	finish  {
		// ambient 0.15
		diffuse 0.8
	}
} }
