// yellow flower
#declare Block37Object = union {
	cylinder {
		<0.5, 0, 0.5>, <0.5, 0.4, 0.5> 0.02

		pigment { color Green }
	}
	sphere {
		<0.5, 0.4, 0.5>, 0.07

		pigment { color Yellow }
	}
}

#declare Block37Material = material {}
