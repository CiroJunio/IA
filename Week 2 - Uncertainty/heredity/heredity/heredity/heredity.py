import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Calculate the joint probability of a set of genetic and trait probabilities
    for all people in the family based on their gene count and trait presence.
    """
    probability = 1

    for person in people:
        # Determine the number of genes for this person (0, 1, or 2)
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0
        
        # Calculate the probability of this gene count
        if people[person]["mother"] is None or people[person]["father"] is None:
            # If no parents, use prior probabilities
            prob_gene = PROBS["gene"][gene_count]
        else:
            mother = people[person]["mother"]
            father = people[person]["father"]
            
            # Determine the number of genes each parent has
            mother_genes = 2 if mother in two_genes else 1 if mother in one_gene else 0
            father_genes = 2 if father in two_genes else 1 if father in one_gene else 0
            
            # Calculate the probability of inheriting genes from each parent
            if gene_count == 0:
                prob_gene = (
                    (1 - PROBS["mutation"]) * (1 - PROBS["mutation"]) +
                    PROBS["mutation"] * PROBS["mutation"]
                )
            elif gene_count == 1:
                prob_gene = (
                    (1 - PROBS["mutation"]) * PROBS["mutation"] +
                    PROBS["mutation"] * (1 - PROBS["mutation"])
                )
            else:
                prob_gene = PROBS["mutation"] * PROBS["mutation"]
        
        # Calculate the probability of having the trait based on the gene count
        if person in have_trait:
            prob_trait = PROBS["trait"][gene_count][True]
        else:
            prob_trait = PROBS["trait"][gene_count][False]
        
        # Multiply the probabilities for this person
        probability *= prob_gene * prob_trait

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Update the gene and trait probabilities in the given dictionary based on the
    current probabilities (p) for each individual.
    """
    for person in probabilities:
        # Update the gene probability for this person
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        
        # Update the trait probability for this person
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Normalize the gene and trait probabilities for each person so that they sum to 1.
    """
    for person in probabilities:
        # Normalize gene probabilities
        total_gene_prob = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= total_gene_prob
        
        # Normalize trait probabilities
        total_trait_prob = sum(probabilities[person]["trait"].values())
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= total_trait_prob

if __name__ == "__main__":
    main()
