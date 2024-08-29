# game setup
WIDTH    = 640
HEIGTH   = 360
FPS      = 60
TILESIZE = 64

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
STAMINA_BAR_WIDTH = 140
STAMINA_BAR_HEIGHT = 10
ITEM_BOX_SIZE = 80
UI_FONT = 'font/AncientModernTales.ttf'
DESERET_FONT = 'font/AdamicBee.ttf'
FUTURA_FONT = 'font/Futura.ttf'
FUTURA_CONDENSED = 'font/FuturaCondensed.ttf'
FUTURA_CONDENSED_BOLD = 'font/FuturaCEB.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
STAMINA_COLOR = 'green'
STAMINA_COLOR_OVERSPRINT = 'red'
UI_BORDER_COLOR_ACTIVE = 'gold'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15,'graphic':'graphics/weapons/sword/full.png'}
}

monster_data = {
	'them': {'health': 400,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 3, 'resistance': 3, 'attack_radius': 40, 'notice_radius': 500},
    'monkey': {'health': 100,'exp':100,'damage':5,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 30, 'notice_radius': 250},
    'snail': {'health': 200,'exp':100,'damage':30,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 1, 'resistance': 3, 'attack_radius': 30, 'notice_radius': 250},
    'okto': {'health': 150,'exp':100,'damage':20,'attack_type': 'slash', 'attack_sound':'audio/attack/slash.wav', 'speed': 2, 'resistance': 3, 'attack_radius': 350, 'notice_radius': 450}
}