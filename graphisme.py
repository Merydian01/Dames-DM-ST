# Auteur : Dylan
# Date : #enter
# Nom du projet : #enter

# graphismes.py

import pygame
import backend


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (200, 200, 200)
QUEEN_COLOR = (255, 215, 0)

WINDOW_WIDTH = backend.LINE_LENGTH * backend.CELL_SIZE + backend.BORDER_WIDTH * 2
WINDOW_HEIGHT = backend.NUM_ROWS * backend.CELL_SIZE + backend.BORDER_WIDTH * 2


screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de Dames - Coups Multiples")

def afficher_lignes():
    for row in range(backend.NUM_ROWS):
        for col in range(backend.LINE_LENGTH):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (
                col * backend.CELL_SIZE + backend.BORDER_WIDTH,
                row * backend.CELL_SIZE + backend.BORDER_WIDTH,
                backend.CELL_SIZE, backend.CELL_SIZE
            ))

def dessiner_pion(position, color, is_queen=False):
    x = position[1] * backend.CELL_SIZE + backend.CELL_SIZE // 2 + backend.BORDER_WIDTH
    y = position[0] * backend.CELL_SIZE + backend.CELL_SIZE // 2 + backend.BORDER_WIDTH
    radius = backend.CELL_SIZE // 3
    pygame.draw.circle(screen, color, (x, y), radius)
    if is_queen:
        pygame.draw.circle(screen, QUEEN_COLOR, (x, y), radius // 2)

def main():
    pions_rouges = [[row, col, False] for row in range(4) for col in range(backend.LINE_LENGTH) if (row + col) % 2 == 0]
    pions_bleus = [[row, col, False] for row in range(6, 10) for col in range(backend.LINE_LENGTH) if (row + col) % 2 == 0]
    selected_pion = None
    tour_rouge = True  # Rouge commence

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selected_pion is None:
                        if tour_rouge:
                            index = backend.detecter_clic_pion(event.pos, pions_rouges)
                            if index is not None:
                                selected_pion = (pions_rouges, index)
                        else:
                            index = backend.detecter_clic_pion(event.pos, pions_bleus)
                            if index is not None:
                                selected_pion = (pions_bleus, index)
                    else:
                        case_cible = backend.detecter_case(event.pos)
                        if case_cible and backend.est_case_noire(case_cible):
                            pions, index = selected_pion
                            pion = pions[index]
                            couleur = RED if pions == pions_rouges else BLUE

                            if backend.verifier_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges, pions_rouges, pions_bleus):
                                backend.effectuer_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges)
                                tour_rouge = not tour_rouge
                            else:
                                selected_pion = None

        screen.fill(BG_COLOR)
        afficher_lignes()
        for pion in pions_rouges:
            dessiner_pion(pion, RED, pion[2])
        for pion in pions_bleus:
            dessiner_pion(pion, BLUE, pion[2])
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
