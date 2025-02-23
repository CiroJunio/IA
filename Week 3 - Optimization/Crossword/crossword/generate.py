import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Remove palavras do domínio de uma variável que não têm o comprimento correto.
        """
        for var in self.domains:  # Itera sobre todas as variáveis
            domain = self.domains[var].copy()  # Faz uma cópia do domínio da variável
            for word in domain:  # Itera sobre todas as palavras no domínio
                if len(word) != var.length:  # Verifica se o comprimento da palavra é diferente do esperado
                    self.domains[var].remove(word)  # Remove a palavra inconsistente

    def revise(self, x, y):
        """
        Remove valores do domínio de `x` que não têm correspondência em `y`.
        Retorna True se alguma alteração foi feita, False caso contrário.
        """
        revised = False  # Flag para indicar se houve alteração
        overlap = self.crossword.overlaps[x, y]  # Obtém a sobreposição entre x e y
        if overlap:  # Se houver sobreposição
            i, j = overlap  # Índices de sobreposição
            domain_x = self.domains[x].copy()  # Cópia do domínio de x
            for word_x in domain_x:  # Itera sobre as palavras no domínio de x
                conflict = True  # Assume que há conflito inicialmente
                for word_y in self.domains[y]:  # Itera sobre as palavras no domínio de y
                    if word_x[i] == word_y[j]:  # Verifica se há correspondência
                        conflict = False  # Sem conflito
                        break
                if conflict:  # Se houver conflito
                    self.domains[x].remove(word_x)  # Remove a palavra de x
                    revised = True  # Indica que houve alteração
            return revised  # Retorna se houve alteração

    def ac3(self, arcs=None):
        """
        Aplica o algoritmo AC3 para garantir consistência de arco.
        Retorna True se a consistência foi aplicada sem esvaziar domínios, False caso contrário.
        """
        queue = arcs if arcs is not None else [(x, y) for x in self.crossword.variables for y in self.crossword.neighbors(x)]  # Inicializa a fila de arcos
        while queue:  # Enquanto houver arcos na fila
            x, y = queue.pop(0)  # Remove o primeiro arco da fila
            if self.revise(x, y):  # Se houver revisão no domínio de x
                if not self.domains[x]:  # Se o domínio de x estiver vazio
                    return False  # Retorna False (inconsistência)
                for z in self.crossword.neighbors(x) - {y}:  # Adiciona arcos vizinhos à fila
                    queue.append((z, x))
        return True  # Retorna True (consistência alcançada)

    def assignment_complete(self, assignment):
        """
        Verifica se a atribuição está completa (todas as variáveis têm valores).
        """
        return all(var in assignment for var in self.crossword.variables)  # Retorna True se todas as variáveis estão em assignment

    def consistent(self, assignment):
        """
        Verifica se a atribuição é consistente (palavras únicas, comprimento correto e sem conflitos).
        """
        words = list(assignment.values())  # Lista de palavras atribuídas
        if len(words) != len(set(words)):  # Verifica se há palavras duplicadas
            return False
        for var, word in assignment.items():  # Verifica se o comprimento da palavra está correto
            if var.length != len(word):
                return False
        for var1, var2 in self.crossword.overlaps:  # Verifica conflitos entre variáveis vizinhas
            if var1 in assignment and var2 in assignment:
                overlap = self.crossword.overlaps[var1, var2]
                if overlap:
                    i, j = overlap
                    if assignment[var1][i] != assignment[var2][j]:  # Verifica se há conflito na sobreposição
                        return False
        return True  # Retorna True se a atribuição for consistente

    def order_domain_values(self, var, assignment):
        """
        Ordena os valores do domínio de `var` pela heurística de valores menos restritivos.
        """
        def count_conflicts(value):  # Função para contar conflitos
            count = 0
            for neighbor in self.crossword.neighbors(var):  # Itera sobre os vizinhos de var
                if neighbor not in assignment:  # Se o vizinho não estiver atribuído
                    overlap = self.crossword.overlaps[var, neighbor]  # Obtém a sobreposição
                    if overlap:
                        i, j = overlap
                        for neighbor_value in self.domains[neighbor]:  # Itera sobre os valores do vizinho
                            if value[i] != neighbor_value[j]:  # Verifica conflito
                                count += 1
            return count  # Retorna o número de conflitos
        return sorted(self.domains[var], key=count_conflicts)  # Ordena os valores pelo número de conflitos

    def select_unassigned_variable(self, assignment):
        """
        Seleciona a variável não atribuída com o menor número de valores restantes no domínio.
        Em caso de empate, escolhe a variável com o maior grau (mais vizinhos).
        """
        unassigned = [var for var in self.crossword.variables if var not in assignment]  # Lista de variáveis não atribuídas
        return min(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))  # Seleciona a variável com menos valores e maior grau

    def backtrack(self, assignment):
        """
        Implementa a busca de retrocesso para encontrar uma atribuição completa.
        Retorna a atribuição se for possível, None caso contrário.
        """
        if self.assignment_complete(assignment):  # Se a atribuição estiver completa
            return assignment  # Retorna a atribuição
        var = self.select_unassigned_variable(assignment)  # Seleciona uma variável não atribuída
        for value in self.order_domain_values(var, assignment):  # Itera sobre os valores ordenados do domínio
            assignment[var] = value  # Atribui o valor à variável
            if self.consistent(assignment):  # Se a atribuição for consistente
                result = self.backtrack(assignment)  # Chama recursivamente o backtrack
                if result:  # Se encontrar uma solução
                    return result  # Retorna a solução
            del assignment[var]  # Remove a atribuição (backtrack)
        return None  # Retorna None se não encontrar solução

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
