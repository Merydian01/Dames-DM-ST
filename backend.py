# Auteur : Dylan
# Date : #enter
# Nom du projet : #enter

# backend
import pygame

NUM_ROWS = 10
LINE_LENGTH = 10
CELL_SIZE = 80
BORDER_WIDTH = 20

def totaux():
    print("totaux")

def est_case_noire(case):
    row, col = case
    return (row + col) % 2 == 0

def est_case_vide(case, pions_rouges, pions_bleus):
    return not any(p[0] == case[0] and p[1] == case[1] for p in (pions_rouges + pions_bleus))

def verifier_capture(pion, case_cible, pions_ennemis, pions_rouges, pions_bleus):
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

def promotion_en_reine(pion, couleur):
    if couleur == (255, 0, 0) and pion[0] == NUM_ROWS - 1:
        pion[2] = True
    elif couleur == (0, 0, 255) and pion[0] == 0:
        pion[2] = True

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
