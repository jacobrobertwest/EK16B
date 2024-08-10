import pygame
pygame.init()


def debug(info,y = 10, x = 10, font_size = 30,bg='Black'):
	font = pygame.font.Font(None,font_size)
	display_surface = pygame.display.get_surface()
	debug_surf = font.render(str(info),True,'White')
	debug_rect = debug_surf.get_rect(topleft = (x,y))
	if bg is not None:
		pygame.draw.rect(display_surface,bg,debug_rect)
	display_surface.blit(debug_surf,debug_rect)
