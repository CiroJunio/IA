"""
Tic Tac Toe Player
"""

import math
import random
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Verifica se o tabuleiro está vazio (início do jogo)
    if all(cell is None for row in board for cell in row):
        return X

    # Conta os valores de X e O no tabuleiro
    count_X = sum(row.count(X) for row in board)
    count_O = sum(row.count(O) for row in board)

    # Determinar o proximo jogador
    if (count_X == count_O):
        return X    # X joga se as jogadas estão equilibradas
    else:
        return O    # O joga caso contrario

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    positions = set()
    for i, row in enumerate(board):  
        for j, cell in enumerate(row): 
            if cell is None: 
                positions.add((i, j))  # Adiciona a posição (i, j) à lista
    return positions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not (0 <= action[0] < 3 and 0 <= action[1] < 3):
        raise ValueError("Ação inválida! Posição fora dos limites do tabuleiro.")

    i, j = action  # Desempacota a ação (posição onde o jogador quer jogar)

    if board[i][j] is not None:
        raise ValueError("Ação inválida! A posição está ocupada!")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Verificar as linhas
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]  # Retorna o vencedor ('X' ou 'O')

    # Verificar as colunas
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col] # Retorna o vencedor ('X' ou 'O')

    # Verifica a primeira diagonal
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0] # Retorna o vencedor ('X' ou 'O')

    # Verifica a segunda diagonal
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2] # Retorna o vencedor ('X' ou 'O')

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    # Verifica se ainda há células vazias
    for row in board:
        for cell in row:
            if cell is None:
                return False  # O jogo pode continuar, pois há células vazias

    # Se não houver vencedor e não houver células vazias, o jogo terminou em empate
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_value = winner(board)
    if winner_value == X:
        return 1  # X venceu
    elif winner_value == O:
        return -1  # O venceu
    return 0  # Empate


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            if v >= beta:  # Poda
                return v
            alpha = max(alpha, v)
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            if v <= alpha:  # Poda
                return v
            beta = min(beta, v)
        return v

    current_player = player(board)
    if current_player == "X":  # Maximizador
        best_action = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in actions(board):
            score = min_value(result(board, action), alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, score)
        return best_action
    else:  # Minimizador
        best_action = None
        best_score = float('inf')
        alpha = float('-inf')
        beta = float('inf')
        for action in actions(board):
            score = max_value(result(board, action), alpha, beta)
            if score < best_score:
                best_score = score
                best_action = action
            beta = min(beta, score)
        return best_action


