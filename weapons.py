"""
SPS: shoots per second
damage: damage per bullet
speed: how fast does bullet travel
bullet_lifespawn: how many ticks will bullet exist
zoom: how much will it affect view; line is divided into parts, center is one part from the weapon and 'zoom' parts from the player; for melee very high; for telescope less than 0
img: name of the image it is with
"""
"""
TODO:
Magazine size
reload time
"""
pistol = {
	"SPS" : 2,
	"damage" : 5,
	"speed" : 3,
	"bullet_lifespawn": 70,
	"zoom" : 5,
	"img": "pistol",
}

m4 = {
	"SPS": 10,
	"damage" : 2,
	"speed": 4,
	"bullet_lifespawn": 50,
	"zoom": 4,
	"img": "m4",
}

sniper_rifle = {
	"SPS": 0.5,
	"damage" : 30,
	"speed": 6,
	"bullet_lifespawn": 100,
	"zoom": 1,
	"img": "pistol",
}