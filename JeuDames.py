# Auteur : Dylan
# Date : #enter
# Nom du projet : #enter

import pygame

# ------------ INITIALISATION ET PARAMÈTRES ------------
print("Coucou")
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
CELL_SIZE = 80  # Taille d'une case
LINE_LENGTH = 10  # Nombre de cases par ligne
NUM_ROWS = 10  # Nombre de lignes
BORDER_WIDTH = 20  # Largeur de la bordure autour du plateau
WINDOW_WIDTH = LINE_LENGTH * CELL_SIZE + BORDER_WIDTH * 2
WINDOW_HEIGHT = NUM_ROWS * CELL_SIZE + BORDER_WIDTH * 2

# Création de la fenêtre d'affichage
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de Dames - Dame avec Mouvement Libre")

# Initialisation des pions
pions_rouges = [[row, col, False] for row in range(4) for col in range(LINE_LENGTH) if
                (row + col) % 2 == 0]  # False = pas reine
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


def verifier_case_libre(case):
    """
    Vérifie si une case est libre (aucun pion rouge ou bleu).
    """
    row, col = case
    return not any(p[0] == row and p[1] == col for p in (pions_rouges + pions_bleus))


def mouvement_dame_valide(pion, case_cible):
    """
    Vérifie si un mouvement pour une dame est valide :
    - La case cible est sur la même diagonale.
    - Toutes les cases entre le point de départ et la case cible sont libres.
    """
    row, col, _ = pion
    target_row, target_col = case_cible

    # Vérifie que le mouvement est diagonal
    if abs(target_row - row) != abs(target_col - col):
        return False

    # Vérifie que toutes les cases entre la position actuelle et la cible sont libres
    step_row = 1 if target_row > row else -1
    step_col = 1 if target_col > col else -1
    for i in range(1, abs(target_row - row)):
        intermediate_row = row + i * step_row
        intermediate_col = col + i * step_col
        if not verifier_case_libre([intermediate_row, intermediate_col]):
            return False

    return True


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
                    if case_cible and est_case_noire(case_cible) and verifier_case_libre(case_cible):
                        pions, index = selected_pion
                        pion = pions[index]

                        # Vérifie mouvement normal ou mouvement dame
                        if pion[2]:  # Si c'est une dame
                            if mouvement_dame_valide(pion, case_cible):
                                pion[0], pion[1] = case_cible[0], case_cible[1]
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
