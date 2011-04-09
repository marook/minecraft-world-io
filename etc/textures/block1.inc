// stone
#declare Block1Object = BlockDefaultObject

#declare Block1Material = material { texture {
 	pigment {rgb 0.68 }
	normal {
		average normal_map {
				[1.0  granite scale 0.25]
				[1.0  agate 0.5 scale 0.005]
		}
	}
	 	
	finish {
		specular 0.1 roughness 0.3
	}

	scale 3
}
}
