import pygame

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set up screen
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("🎹 Mini Piano")

# Define sounds (you can replace these with actual .wav piano notes)
notes = {
    pygame.K_a: 'C.wav',
    pygame.K_s: 'D.wav',
    pygame.K_d: 'E.wav',
    pygame.K_f: 'F.wav',
    pygame.K_g: 'G.wav',
    pygame.K_h: 'A.wav',
    pygame.K_j: 'B.wav',
}

# Load and store sound files (use your own .wav files in same folder)
sounds = {}
for key, filename in notes.items():
    try:
        sounds[key] = pygame.mixer.Sound(filename)
    except:
        print(f"Missing sound: {filename}. Please place a .wav file named {filename} in the same folder.")

# Game loop
running = True
while running:
    screen.fill((200, 220, 255))
    font = pygame.font.SysFont(None, 40)
    label = font.render("Press A, S, D, F, G, H, J to play notes", True, (10, 10, 10))
    screen.blit(label, (20, 130))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key in sounds:
            sounds[event.key].play()

pygame.quit()
