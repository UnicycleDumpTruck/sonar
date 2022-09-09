import pygame
from os import path

pygame.mixer.pre_init(44100, -16, 1, 1024)
#pygame.mixer.pre_init(44100, -16, 1, 256)
pygame.mixer.init()

parent_dir = path.dirname(path.dirname(path.dirname(__file__)))
sound_dir = f"{parent_dir}/sounds"

sounds = {

    'ping_a': pygame.mixer.Sound(f"{sound_dir}/high_ping.wav"),
    'ping_a_echo': pygame.mixer.Sound(f"{sound_dir}/high_ping_echo.wav"),
    'ping_b': pygame.mixer.Sound(f"{sound_dir}/low_ping.wav"),
    'ping_b_echo': pygame.mixer.Sound(f"{sound_dir}/low_ping_echo.wav"),

    # "dolphin_hi": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_love": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_food": pygame.mixer.Sound("../../sounds/high_ping.wav"),
    # "dolphin_danger": pygame.mixer.Sound("../../sounds/high_ping.wav"),

    # "beluga_hi": pygame.mixer.Sound(f"{sound_dir}/beluga_hi.wav"),
    # "beluga_love": pygame.mixer.Sound(f"{sound_dir}/beluga_love.wav"),
    # "beluga_food": pygame.mixer.Sound(f"{sound_dir}/beluga_food.wav"),
    # "beluga_danger": pygame.mixer.Sound(f"{sound_dir}/beluga_danger.wav"),

    "whale_hi": pygame.mixer.Sound(f"{sound_dir}/whale_hi.wav"),
    "whale_love": pygame.mixer.Sound(f"{sound_dir}/whale_love.wav"),
    "whale_food": pygame.mixer.Sound(f"{sound_dir}/whale_food.wav"),
    "whale_danger": pygame.mixer.Sound(f"{sound_dir}/whale_danger.wav"),

    "narwhal_hi": pygame.mixer.Sound(f"{sound_dir}/narwhal_hi.wav"),
    "narwhal_love": pygame.mixer.Sound(f"{sound_dir}/narwhal_love.wav"),
    "narwhal_food": pygame.mixer.Sound(f"{sound_dir}/narwhal_food.wav"),
    "narwhal_danger": pygame.mixer.Sound(f"{sound_dir}/narwhal_danger.wav"),

    "orca_hi": pygame.mixer.Sound(f"{sound_dir}/orca_love.wav"),
    "orca_love": pygame.mixer.Sound(f"{sound_dir}/orca_love.wav"),
    "orca_food": pygame.mixer.Sound(f"{sound_dir}/orca_food.wav"),
    "orca_danger": pygame.mixer.Sound(f"{sound_dir}/orca_danger.wav"),

    "seal_hi": pygame.mixer.Sound(f"{sound_dir}/seal_love.wav"),
    "seal_love": pygame.mixer.Sound(f"{sound_dir}/seal_love.wav"),
    "seal_food": pygame.mixer.Sound(f"{sound_dir}/seal_food.wav"),
    "seal_danger": pygame.mixer.Sound(f"{sound_dir}/seal_danger.wav"),

    "shark_hi": None,
    "shark_love": None,
    "shark_food": None,
    "shark_danger": None,

    "ship_hi": pygame.mixer.Sound(f"{sound_dir}/foreign_ping.wav"),
    "ship_love": None,
    "ship_food": None,
    "ship_danger": None,

    "sub_hi": pygame.mixer.Sound(f"{sound_dir}/foreign_ping.wav"),
    "sub_love": None,
    "sub_food": None,
    "sub_danger": None,
}
