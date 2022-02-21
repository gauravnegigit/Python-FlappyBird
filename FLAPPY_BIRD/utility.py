import pygame

def scale_image(img, factor):
	size = round(img.get_width() * factor) , round(img.get_height() * factor)
	return pygame.transform.scale(img,size)

def blit_rotate_centre(win,image,top_left, angle):
	rotated_image = pygame.transform.rotate(image , angle)
	new_rect = rotated_image.get_rect(center = image.get_rect(topleft = top_left).center)
	win.blit(rotated_image , new_rect.topleft)

def blit_text_center(win,font, text):
	text_blit = font.render(text , 1, (0,0,0) )
	win.blit(text_blit , (win.get_width()//2  - text_blit.get_width()//2 , win.get_height()//2 - text_blit.get_height()//2))
	pygame.display.update()