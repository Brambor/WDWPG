"""
name_AI = {
	"cause": sss, #cause
	"behavior": (
		(ticks, speed, locked direction),
		...
	),
	"recharge": sss, #ammount of ticks to recharge after behavior ended
}
"""

Smurph_AI = {
	"distance": 600,
	"behavior": (
		{"ticks": 240, "speed": 0.05, "locked_direction": False},

		{"ticks": 1, "speed": 0, "locked_direction": False},	#point
		{"ticks": 20, "speed": 5, "locked_direction": True},	#charge
		{"ticks": 102, "speed": 0, "locked_direction": True},	#re-charge

		{"ticks": 1, "speed": 0, "locked_direction": False},
		{"ticks": 20, "speed": 5, "locked_direction": True},
		{"ticks": 84, "speed": 0, "locked_direction": True},

		{"ticks": 1, "speed": 0, "locked_direction": False},
		{"ticks": 20, "speed": 5, "locked_direction": True},
		{"ticks": 66, "speed": 0, "locked_direction": True},

		{"ticks": 1, "speed": 0, "locked_direction": False},
		{"ticks": 20, "speed": 5, "locked_direction": True},
		{"ticks": 48, "speed": 0, "locked_direction": True},

		{"ticks": 1, "speed": 0, "locked_direction": False},
		{"ticks": 20, "speed": 5, "locked_direction": True},
		{"ticks": 30, "speed": 0, "locked_direction": True},

		{"ticks": 1, "speed": 0, "locked_direction": False},
		{"ticks": 60, "speed": 5, "locked_direction": True},

		{"ticks": 150, "speed": 0, "locked_direction": False},
	),
	"recharge": 600,
}