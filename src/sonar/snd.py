import pygame

pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.mixer.init()

ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
r_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
g_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")
b_ping = pygame.mixer.Sound("../../sounds/high_ping.wav")

sounds = {

    'ping_a': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    'ping_a_echo': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    'ping_b': pygame.mixer.Sound("../../sounds/high_ping.wav"),
    'ping_b_echo': pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "dolphin_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "dolphin_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "dolphin_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "dolphin_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "whale_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "whale_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "whale_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "whale_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "narwhal_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "narwhal_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "narwhal_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "narwhal_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "orca_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "orca_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "orca_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "orca_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    "seal_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "seal_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "seal_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    "seal_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),
}
