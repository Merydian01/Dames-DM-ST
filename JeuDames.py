import pygame

# ------------ INITIALISATION ET PARAMÈTRES ------------

# Initialisation de Pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (200, 200, 200)
QUEEN_COLOR = (255, 215, 0)  # Or pour les reines

# Paramètres du plateau et de la fenêtre
CELL_SIZE = 80          # Taille d'une case
LINE_LENGTH = 10        # Nombre de cases par ligne
NUM_ROWS = 10           # Nombre de lignes
BORDER_WIDTH = 20       # Largeur de la bordure autour du plateau
WINDOW_WIDTH = LINE_LENGTH * CELL_SIZE + BORDER_WIDTH * 2
WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE + BORDER_WIDTH * 2

# Création de la fenêtre d'affichage
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de Dames - Captures Valides")

# Initialisation des pions
pions_rouges = [[row, col, False] for row in range(4) for col in range(LINE_LENGTH) if (row + col) % 2 == 0]  # False = pas reine
pions_bleus = [[row, col, False] for row in range(6, 10) for col in range(LINE_LENGTH) if (row + col) % 2 == 0]
selected_pion = None  # Aucun pion n'est sélectionné au départ

# ------------ FONCTIONS ------------

def afficher_lignes():
    """
    Affiche un plateau de damier noir et blanc.
    """
    for row in range(NUM_ROWS):
        for col in range(LINE_LENGTH):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (
                col * CELL_SIZE + BORDER_WIDTH,
                row * CELL_SIZE + BORDER_WIDTH,
                CELL_SIZE, CELL_SIZE
            ))

def dessiner_pion(position, color, is_queen=False):
    """
    Dessine un pion de la couleur spécifiée à la position donnée.
    """
    x = position[1] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
    y = position[0] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
    radius = CELL_SIZE // 3
    pygame.draw.circle(screen, color, (x, y), radius)
    if is_queen:
        pygame.draw.circle(screen, QUEEN_COLOR, (x, y), radius // 2)

def detecter_case(mouse_pos):
    """
    Détecte sur quelle case l'utilisateur a cliqué.
    """
    x, y = mouse_pos
    col = (x - BORDER_WIDTH) // CELL_SIZE
    row = (y - BORDER_WIDTH) // CELL_SIZE
    if 0 <= row < NUM_ROWS and 0 <= col < LINE_LENGTH:
        return [row, col]
    return None

def detecter_clic_pion(mouse_pos, pions):
    """
    Vérifie si la souris clique sur un pion donné.
    """
    for i, pion in enumerate(pions):
        x = pion[1] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
        y = pion[0] * CELL_SIZE + CELL_SIZE // 2 + BORDER_WIDTH
        distance = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
        if distance <= CELL_SIZE // 3:
            return i  # Retourne l'indice du pion sélectionné
    return None

def est_case_noire(case):
    """
    Vérifie si une case est noire.
    """
    row, col = case
    return (row + col) % 2 == 0

def est_case_vide(case, pions_rouges, pions_bleus):
    """
    Vérifie si une case est vide (aucun pion rouge ou bleu).
    """
    return not any(p[0] == case[0] and p[1] == case[1] for p in (pions_rouges + pions_bleus))

def verifier_capture(pion, case_cible, pions_ennemis):
    """
    Vérifie si une capture est possible :
    - Pion saute par-dessus un ennemi.
    - Une case vide se trouve après l'ennemi.
    """
    row, col, _ = pion
    target_row, target_col = case_cible

    # Vérifie si la case cible est à deux cases en diagonale
    if abs(target_row - row) == 2 and abs(target_col - col) == 2:
        middle_row = (row + target_row) // 2
        middle_col = (col + target_col) // 2

        # Vérifie si un pion ennemi est à capturer et la case cible est vide
        if any(p[0] == middle_row and p[1] == middle_col for p in pions_ennemis) and \
                est_case_vide(case_cible, pions_rouges, pions_bleus):
            return True

    return False

def effectuer_capture(pion, case_cible, pions_ennemis):
    """
    Effectue la capture :
    - Déplace le pion sur la case cible.
    - Supprime le pion ennemi capturé.
    """
    row, col, _ = pion
    target_row, target_col = case_cible
    middle_row = (row + target_row) // 2
    middle_col = (col + target_col) // 2

    # Supprime le pion ennemi capturé
    for p in pions_ennemis:
        if p[0] == middle_row and p[1] == middle_col:
            pions_ennemis.remove(p)
            break

    # Met à jour la position du pion
    pion[0] = target_row
    pion[1] = target_col

def promotion_en_reine(pion, couleur):
    """
    Vérifie si le pion doit être promu en reine.
    """
    if couleur == RED and pion[0] == NUM_ROWS - 1:
        pion[2] = True  # Promu en reine
    elif couleur == BLUE and pion[0] == 0:
        pion[2] = True  # Promu en reine

# ------------ BOUCLE PRINCIPALE ------------

running = True
case_cible = None  # Case cible pour déplacer le pion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if selected_pion is None:
                    # Vérifie si un pion rouge ou bleu est sélectionné
                    index = detecter_clic_pion(event.pos, pions_rouges)
                    if index is not None:
                        selected_pion = (pions_rouges, index)  # Sélectionner un pion rouge
                    else:
                        index = detecter_clic_pion(event.pos, pions_bleus)
                        if index is not None:
                            selected_pion = (pions_bleus, index)  # Sélectionner un pion bleu
                else:
                    # Si un pion est déjà sélectionné, détecte la case cible
                    case_cible = detecter_case(event.pos)
                    if case_cible and est_case_noire(case_cible) and est_case_vide(case_cible, pions_rouges, pions_bleus):
                        pions, index = selected_pion
                        pion = pions[index]

                        # Vérifie capture ou mouvement
                        if verifier_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges):
                            effectuer_capture(pion, case_cible, pions_bleus if pions == pions_rouges else pions_rouges)
                        elif abs(case_cible[0] - pion[0]) == 1 and abs(case_cible[1] - pion[1]) == 1:
                            # Mouvement normal
                            pion[0], pion[1] = case_cible[0], case_cible[1]

                        # Vérifie promotion
                        promotion_en_reine(pion, RED if pions == pions_rouges else BLUE)

                        selected_pion = None
                        case_cible = None

    # Remplir le fond de la fenêtre
    screen.fill(BG_COLOR)

    # Affichage des cases et des pions
    afficher_lignes()
    for pion in pions_rouges:
        dessiner_pion(pion, RED, pion[2])
    for pion in pions_bleus:
        dessiner_pion(pion, BLUE, pion[2])

    # Mise à jour de l'affichage
    pygame.display.flip()

pygame.quit()
