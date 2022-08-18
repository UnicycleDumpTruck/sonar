import pygame

pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.mixer.init()

ping = pygame.mixer.Sound("high_ping.wav")
r_ping = pygame.mixer.Sound("high_ping.wav")
g_ping = pygame.mixer.Sound("high_ping.wav")
b_ping = pygame.mixer.Sound("high_ping.wav")

ping_sounds = {
    'ping_a': pygame.mixer.Sound("high_ping.wav"),
    'ping_a_echo': pygame.mixer.Sound("high_ping.wav"),
    'ping_b': pygame.mixer.Sound("high_ping.wav"),
    'ping_b_echo': pygame.mixer.Sound("high_ping.wav"),
}

dolphin_sounds = {
    "hi": pygame.mixer.Sound("high_ping.wav"),
    "love": pygame.mixer.Sound("high_ping.wav"),
    "food": pygame.mixer.Sound("high_ping.wav"),
}

whale_sounds = {
    "hi": pygame.mixer.Sound("high_ping.wav"),
    "love": pygame.mixer.Sound("high_ping.wav"),
    "food": pygame.mixer.Sound("high_ping.wav"),
}

animal_sounds = {
    "dolphin": dolphin_sounds,
    "whale": whale_sounds,
}
