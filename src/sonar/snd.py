import pygame

pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.mixer.init()

# ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
# r_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
# g_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
# b_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")

sounds = {

    'ping_a': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # TODO: Replace
    'ping_a_echo': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # TODO: Replace
    'ping_b': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # TODO: Replace
    'ping_b_echo': pygame.mixer.Sound("../../sounds/high_ping.wav"),

    # "dolphin_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "beluga_hi": pygame.mixer.Sound("../../sounds/beluga_hi.wav"),
    "beluga_love": pygame.mixer.Sound("../../sounds/beluga_love.wav"),
    "beluga_food": pygame.mixer.Sound("../../sounds/beluga_food.wav"),
    "beluga_danger": pygame.mixer.Sound("../../sounds/beluga_danger.wav"),

    "whale_hi": pygame.mixer.Sound("../../sounds/whale_hi.wav"),
    "whale_love": pygame.mixer.Sound("../../sounds/whale_love.wav"),
    "whale_food": pygame.mixer.Sound("../../sounds/whale_food.wav"),
    "whale_danger": pygame.mixer.Sound("../../sounds/whale_danger.wav"),

    "narwhal_hi": pygame.mixer.Sound("../../sounds/narwhal_hi.wav"),
    "narwhal_love": pygame.mixer.Sound("../../sounds/narwhal_love.wav"),
    "narwhal_food": pygame.mixer.Sound("../../sounds/narwhal_food.wav"),
    "narwhal_danger": pygame.mixer.Sound("../../sounds/narwhal_danger.wav"),

    "orca_hi": pygame.mixer.Sound("../../sounds/orca_hi.wav"),
    "orca_love": pygame.mixer.Sound("../../sounds/orca_love.wav"),
    "orca_food": pygame.mixer.Sound("../../sounds/orca_food.wav"),
    "orca_danger": pygame.mixer.Sound("../../sounds/orca_danger.wav"),

    "seal_hi": pygame.mixer.Sound("../../sounds/seal_hi.mp3"),
    "seal_love": pygame.mixer.Sound("../../sounds/seal_love.wav"),
    "seal_food": pygame.mixer.Sound("../../sounds/seal_food.wav"),
    "seal_danger": pygame.mixer.Sound("../../sounds/seal_danger.wav"),

    "shark_hi": None,
    "shark_love": None,
    "shark_food": None,
    "shark_danger": None,

    "ship_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "ship_love": None,
    "ship_food": None,
    "ship_danger": None,

    "sub_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "sub_love": None,
    "sub_food": None,
    "sub_danger": None,
}
