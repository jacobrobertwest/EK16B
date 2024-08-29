import pygame
pygame.init()

def debug(info, x=10, y=10, font_size= 30,bg='Black',mult=0):
	font = pygame.font.Font(None,font_size)
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	x = x
	y = y + (20*mult)
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	if bg is not None:
		pygame.draw.rect(display_surface,bg,debug_rect)
	display_surface.blit(debug_surf,debug_rect)
