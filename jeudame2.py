import pygame

# ------------ INITIALISATION ET PARAMÈTRES ------------

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (200, 200, 200)
QUEEN_COLOR = (255, 215, 0)

CELL_SIZE = 80
LINE_LENGTH = 10
NUM_ROWS = 10
BORDER_WIDTH = 20
WINDOW_WIDTH = LINE_LENGTH * CELL_SIZE + BORDER_WIDTH * 2
WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE + BORDER_WIDTH * 2

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de Dames - Coups Multiples")

pions_rouges = [[row, col, False] for row in range(4) for col in range(LINE_LENGTH) if (row + col) % 2 == 0]
pions_bleus = [[row, col, False] for row in range(6, 10) for col in range(LINE_LENGTH) if (row + col) % 2 == 0]
selected_pion = None
tour_rouge = True  # Rouge commence

# ------------ FONCTIONS ------------

def afficher_lignes():
    for row in range(NUM_ROWS):
        for col in range(LINE_LENGTH):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (
                col * CELL_SIZE + BORDER_WIDTH,
                row * CELL_SIZE + BORDER_WIDTH,
                CELL_SIZE, CELL_SIZE
            ))

def dessiner_pion(position, color, is_queen=False):
    x = position[1] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
    y = position[0] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
    radius = CELL_SIZE // 3
    pygame.draw.circle(screen, color, (x, y), radius)
    if is_queen:
        pygame.draw.circle(screen, QUEEN_COLOR, (x, y), radius // 2)

def detecter_case(mouse_pos):
    x = mouse_pos[0] - BORDER_WIDTH
    y = mouse_pos[1] - BORDER_WIDTH
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    if 0 <= row < NUM_ROWS and 0 <= col < LINE_LENGTH:
        return [row, col]
    return None

def detecter_clic_pion(mouse_pos, pions):
    for i, pion in enumerate(pions):
        x = pion[1] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
        y = pion[0] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
        distance = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
        if distance <= CELL_SIZE // 3:
            return i
    return None

def est_case_noire(case):
    row, col = case
    return (row + col) % 2 == 0

def est_case_vide(case, pions_rouges, pions_bleus):
    return not any(p[0] == case[0] and p[1] == case[1] for p in (pions_rouges + pions_bleus))

def deplacement_valide(pion, case_cible, couleur):
    """Vérifie si le déplacement est valide."""
    row, col, is_queen = pion
    target_row, target_col = case_cible
    if is_queen:
        # Vérifie le déplacement en diagonale
        delta_row = target_row - row
        delta_col = target_col - col
        if abs(delta_row) == abs(delta_col):
            step_row = delta_row // abs(delta_row)
            step_col = delta_col // abs(delta_col)
            ennemis_trouves = 0
            for i in range(1, abs(delta_row)):
                intermediate_row = row + i * step_row
                intermediate_col = col + i * step_col
                if any(p[0] == intermediate_row and p[1] == intermediate_col for p in pions_rouges + pions_bleus):
                    if any(p[0] == intermediate_row and p[1] == intermediate_col for p in (pions_bleus if couleur == RED else pions_rouges)):
                        ennemis_trouves += 1
                    else:
                        return False  # Bloqué par un pion allié
            return ennemis_trouves <= 1 and est_case_vide(case_cible, pions_rouges, pions_bleus)
    else:
        # Déplacement standard pour un pion
        if couleur == RED and target_row < row:
            return False
        if couleur == BLUE and target_row > row:
            return False
        return abs(target_row - row) == 1 and abs(target_col - col) == 1 and \
               est_case_vide(case_cible, pions_rouges, pions_bleus)

    return False

def verifier_capture(pion, case_cible, pions_ennemis):
    """Vérifie si une capture est possible."""
    row, col, is_queen = pion
    target_row, target_col = case_cible

    if is_queen:
        delta_row = target_row - row
        delta_col = target_col - col
        if abs(delta_row) == abs(delta_col):
            step_row = delta_row // abs(delta_row)
            step_col = delta_col // abs(delta_col)
            ennemis_trouves = []
            for i in range(1, abs(delta_row)):
                intermediate_row = row + i * step_row
                intermediate_col = col + i * step_col
                if any(p[0] == intermediate_row and p[1] == intermediate_col for p in pions_ennemis):
                    ennemis_trouves.append((intermediate_row, intermediate_col))
                elif not est_case_vide([intermediate_row, intermediate_col], pions_rouges, pions_bleus):
                    return False
            return len(ennemis_trouves) == 1 and est_case_vide(case_cible, pions_rouges, pions_bleus)
    else:
        if abs(target_row - row) == 2 and abs(target_col - col) == 2:
            middle_row = (row + target_row) // 2
            middle_col = (col + target_col) // 2
            if any(p[0] == middle_row and p[1] == middle_col for p in pions_ennemis) and \
                    est_case_vide(case_cible, pions_rouges, pions_bleus):
                return True

    return False
def effectuer_capture(pion, case_cible, pions_ennemis):
    """Effectue la capture d'un pion ennemi."""
    row, col, is_queen = pion
    target_row, target_col = case_cible

    if is_queen:
        delta_row = target_row - row
        delta_col = target_col - col
        step_row = delta_row // abs(delta_row)
        step_col = delta_col // abs(delta_col)
        for i in range(1, abs(delta_row)):
            intermediate_row = row + i * step_row
            intermediate_col = col + i * step_col
            for p in pions_ennemis:
                if p[0] == intermediate_row and p[1] == intermediate_col:
                    pions_ennemis.remove(p)
                    break
    else:
        middle_row = (row + target_row) // 2
        middle_col = (col + target_col) // 2
        for p in pions_ennemis:
            if p[0] == middle_row and p[1] == middle_col:
                pions_ennemis.remove(p)
                break

    pion[0], pion[1] = target_row, target_col

def mouvements_possibles_apres_capture(pion, pions_ennemis):
    """Retourne les mouvements possibles après une capture."""
    row, col, is_queen = pion
    mouvements = []

    for delta_row, delta_col in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        target_row = row + delta_row
        target_col = col + delta_col
        if 0 <= target_row < NUM_ROWS and 0 <= target_col < LINE_LENGTH:
            if verifier_capture(pion, [target_row, target_col], pions_ennemis):
                mouvements.append([target_row, target_col])

    return mouvements

def promotion_en_reine(pion, couleur):
    """Promut un pion en reine s'il atteint l'extrémité du plateau."""
    if couleur == RED and pion[0] == NUM_ROWS - 1:
        pion[2] = True
    elif couleur == BLUE and pion[0] == 0:
        pion[2] = True

# ------------ BOUCLE PRINCIPALE ------------

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if selected_pion is None:
                    if tour_rouge:
                        index = detecter_clic_pion(event.pos, pions_rouges)
                        if index is not None:
                            selected_pion = (pions_rouges, index)
                    else:
                        index = detecter_clic_pion(event.pos, pions_bleus)
                        if index is not None:
                            selected_pion = (pions_bleus, index)
                else:
                    case_cible = detecter_case(event.pos)
                    if case_cible and est_case_noire(case_cible):
                        pions, index = selected_pion
                        pion = pions[index]
                        couleur = RED if pions == pions_rouges else BLUE

                        if verifier_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges):
                            effectuer_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges)
                            new_moves = mouvements_possibles_apres_capture(pion, pions_bleus if pions == pions_rouges else pions_rouges)
                            if not new_moves:
                                tour_rouge = not tour_rouge
                        elif deplacement_valide(pion, case_cible, couleur) and \
                                est_case_vide(case_cible, pions_rouges, pions_bleus):
                            pion[0], pion[1] = case_cible[0], case_cible[1]
                            tour_rouge = not tour_rouge
                        promotion_en_reine(pion, couleur)
                        selected_pion = None

    screen.fill(BG_COLOR)
    afficher_lignes()
    for pion in pions_rouges:
        dessiner_pion(pion, RED, pion[2])
    for pion in pions_bleus:
        dessiner_pion(pion, BLUE, pion[2])
    pygame.display.flip()

pygame.quit()
