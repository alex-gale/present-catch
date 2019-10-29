def fade_in(sprite, speed):
    # increase alpha until max is reached
    sprite.alpha += speed
    if sprite.alpha > 255:
        sprite.alpha = 255

def fade_out(sprite, speed):
    # decrease alpha until min is reached
    sprite.alpha -= speed
    if sprite.alpha < 0:
        sprite.alpha = 0

def slide_in(sprite, speed, finish_height):
    # increase center_y until finish_height is reached
        sprite.center_y += speed
        if sprite.center_y > finish_height:
        	sprite.center_y = finish_height

def turn_animation(sprite, speed=1, increase = True):
    sprite.height += speed if increase else -speed

    if sprite.height < 0:
        sprite.height = 0
    elif sprite.height > sprite.texture.height:
        sprite.height = sprite.texture.height