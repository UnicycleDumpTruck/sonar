"""Command-line interface."""

import pygame

pygame.init()


BOX = 800 # Size of bounding box
CENT = (BOX//2, BOX//2) # Center of box
RWT = 16 # Reticle line weight
RCNT = 20 # Center circle diameter
BLUE = (24, 53, 76)
WHITE = (255, 255, 255)
HRETL = pygame.Rect(RWT, BOX/2 - RWT/2, BOX-(RWT*2), RWT)
VRETL = pygame.Rect(BOX/2 - RWT/2, RWT, RWT, BOX-40)


def main() -> None:
    """Sonar."""
    
    # Set up the drawing window
    screen = pygame.display.set_mode([BOX,BOX])

    # Run until quit
    running = True
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the background with blue
        screen.fill(BLUE)

        draw_reticle(screen)

        # Flip the display
        pygame.display.flip()

    # Running false, time to quit.
    pygame.quit()

def draw_reticle(scrn):
    # Outer White Circle
    pygame.draw.circle(scrn, WHITE, CENT, BOX//2-RWT)

    # Inner Blue Circle
    pygame.draw.circle(scrn, BLUE, CENT, BOX//2-(RWT*2))

    # Reticle crossing lines
    pygame.draw.rect(scrn, WHITE, HRETL)
    pygame.draw.rect(scrn, WHITE, VRETL)

    # Central Blanking circle
    pygame.draw.circle(scrn, BLUE, CENT, RCNT+RWT)       

    # Central circle
    pygame.draw.circle(scrn, WHITE, CENT, RCNT)

def ping():
    # create generator, give main loop arc drawing object and sound player
    pass

def draw_arcs_out(scrn):
    # establish a generator of positions with angles, each call uses one until gone
    return iter_left # number of iterations left in generator

if __name__ == "__main__":
    main()
