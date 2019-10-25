def fade_in(sprite, speed):
	# increase alpha until max is reached
	for i in range(speed):
		if sprite.alpha < 255:
			sprite.alpha += 1
		else:
			sprite.alpha = 255
			break

def fade_out(sprite, speed):
	# decrease alpha until min is reached
	for i in range(speed):
		if sprite.alpha > 0:
			sprite.alpha -= 1
		else:
			sprite.alpha = 0
			break

def slide_in(sprite, speed, finish_height):
	# increase center_y until finish_height is reached
	for i in range(speed):
		if sprite.center_y < finish_height:
			sprite.center_y += 1
		else:
			sprite.center_y = finish_height
			break