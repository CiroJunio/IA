import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Carrega os dados de compras a partir de um arquivo CSV `filename` e os converte em
    uma lista de evidências e uma lista de rótulos. Retorna uma tupla (evidence, labels).
    """
    months = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }
    
    evidence = []  # Lista que armazenará as evidências (features) de cada entrada
    labels = []  # Lista que armazenará os rótulos (valores esperados) de cada entrada

    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignora a linha de cabeçalho do CSV

        for row in reader:
            evidence.append([
                int(row[0]),  # Número de páginas administrativas visitadas
                float(row[1]),  # Tempo gasto em páginas administrativas
                int(row[2]),  # Número de páginas informativas visitadas
                float(row[3]),  # Tempo gasto em páginas informativas
                int(row[4]),  # Número de páginas de produtos visitadas
                float(row[5]),  # Tempo gasto em páginas de produtos
                float(row[6]),  # Taxa de rejeição (Bounce Rates)
                float(row[7]),  # Taxa de saída (Exit Rates)
                float(row[8]),  # Valor das páginas visitadas
                float(row[9]),  # Indica se a visita foi próxima a uma data especial
                months[row[10]],  # Mês da visita convertido para número
                int(row[11]),  # Sistema operacional do visitante
                int(row[12]),  # Navegador utilizado pelo visitante
                int(row[13]),  # Região de origem do visitante
                int(row[14]),  # Tipo de tráfego (origem da visita)
                1 if row[15] == "Returning_Visitor" else 0,  # Tipo de visitante (1 se for recorrente, 0 se novo)
                1 if row[16] == "TRUE" else 0  # Indica se a visita ocorreu no fim de semana
            ])
            labels.append(1 if row[17] == "TRUE" else 0)  # Indica se a compra foi realizada (1) ou não (0)

    return evidence, labels

def train_model(evidence, labels):
    """
    Treina um modelo k-Nearest Neighbors (k=1) utilizando os dados fornecidos.
    Retorna o modelo treinado.
    """
    model = KNeighborsClassifier(n_neighbors=1)  # Instancia o classificador k-NN com k=1
    model.fit(evidence, labels)  # Treina o modelo com os dados fornecidos
    return model

def evaluate(labels, predictions):
    """
    Avalia o desempenho do modelo comparando os rótulos reais com as previsões feitas.
    Retorna uma tupla (sensibilidade, especificidade).
    """
    # Sensibilidade (recall para a classe positiva - compradores)
    true_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 1 and predicted == 1)
    false_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 1 and predicted == 0)
    
    # Especificidade (capacidade de identificar corretamente os não compradores)
    true_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 0 and predicted == 0)
    false_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == 0 and predicted == 1)

    sensitivity = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    specificity = true_negatives / (true_negatives + false_positives) if (true_negatives + false_positives) > 0 else 0

    return sensitivity, specificity




if __name__ == "__main__":
    main()
