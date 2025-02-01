import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.
    """
    total_pages = len(corpus)
    
    # Caso a página não tenha links, consideramos links para todas as páginas
    if not corpus[page]:
        return {p: 1 / total_pages for p in corpus}
    
    # Probabilidades de transição
    probabilities = {}
    random_prob = (1 - damping_factor) / total_pages
    link_prob = damping_factor / len(corpus[page])
    
    # Calculando probabilidades de transição
    for p in corpus:
        if p in corpus[page]:
            probabilities[p] = link_prob
        else:
            probabilities[p] = random_prob
    
    return probabilities


    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    """
    # Inicializar contadores de amostras para cada página
    sample_counts = {page: 0 for page in corpus}
    
    # Escolher uma página inicial aleatória
    current_page = random.choice(list(corpus))
    
    for _ in range(n):
        sample_counts[current_page] += 1
        transition_probs = transition_model(corpus, current_page, damping_factor)
        # Escolher a próxima página com base nas probabilidades
        current_page = random.choices(list(corpus), weights=transition_probs.values())[0]
    
    # Calcular os PageRank finais
    total_samples = sum(sample_counts.values())
    return {page: count / total_samples for page, count in sample_counts.items()}


    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    total_pages = len(corpus)
    
    # Inicializar PageRank igual para todas as páginas
    pagerank = {page: 1 / total_pages for page in corpus}
    
    tolerance = 0.001
    converged = False
    
    while not converged:
        new_pagerank = {}
        converged = True
        
        for page in corpus:
            rank_sum = sum(pagerank[other_page] / len(corpus[other_page])
                           for other_page in corpus if page in corpus[other_page])
            
            # Calcular novo valor do PageRank para a página
            new_pagerank[page] = (1 - damping_factor) / total_pages + damping_factor * rank_sum
            
            # Verificar se a mudança é pequena o suficiente para considerar convergência
            if abs(new_pagerank[page] - pagerank[page]) > tolerance:
                converged = False
        
        pagerank = new_pagerank
    
    return pagerank


    raise NotImplementedError


if __name__ == "__main__":
    main()
