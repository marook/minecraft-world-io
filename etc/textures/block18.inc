// leaves
#declare Block18Radius = 0.3;

#declare Block18Object = union {
	cylinder { <0.0, 0.5, 0.5>, <1.0, 0.5, 0.5>, Block18Radius }
	cylinder { <0.5, 0.5, 0.0>, <0.5, 0.5, 1.0>, Block18Radius }
	cylinder { <0.5, 0.0, 0.5>, <0.5, 1.0, 0.5>, Block18Radius }
}

#declare Block18Material = material {
	texture {
		pigment { color Green }
	}
}
