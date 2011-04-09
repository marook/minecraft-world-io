// red rose
#declare Block38Object = union {
	cylinder {
		<0.5, 0, 0.5>, <0.5, 0.4, 0.5> 0.02

		pigment { color Green }
	}
	sphere {
		<0.5, 0.4, 0.5>, 0.07

		pigment { color Red }
	}
}

#declare Block38Material = material {}
