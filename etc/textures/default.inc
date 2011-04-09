#declare BlockOverlap = 0.001;

#declare BlockDefaultObject = box {
	<0 - BlockOverlap, 0 - BlockOverlap, 0 - BlockOverlap>,
	<1 + BlockOverlap, 1 + BlockOverlap, 1 + BlockOverlap>
}

#declare BlockDefaultMaterial = material {
	texture {
		pigment {
			rgb <1, 0, 1>
		}
	}
}
