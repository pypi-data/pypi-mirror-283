from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


def extract_keywords(text):
    """
    Returns important keywords from a text.
    Implements TF-IDF (Term Frequency-Inverse Document Frequency) to select the top N words as keywords
    
    Args:
        text: the text from which the keywords are drawn
    
    Returns:
        extraction: the most important words in the text
    """
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word not in stopwords.words("english")]
    # Create a list of sentences
    sentences = [" ".join(filtered_words)]
    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    # Fit and transform the sentences to obtain the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(sentences)
    # Get feature names (words)
    feature_names = vectorizer.get_feature_names_out()
    # Get the TF-IDF scores
    tfidf_scores = tfidf_matrix.toarray()[0]
    # Sort words by their TF-IDF scores (highest first)
    sorted_keywords = [feature_names[i] for i in tfidf_scores.argsort()[::-1]]
    return set(sorted_keywords)


def extract_gene_features(gff_file, output_filename):
    """
    Extracts gene features from a GFF3 file and writes them to a new file.

    Args:
        gff_file (str): Path to the GFF3 file.
        output_filename (str): Path to the output file.

    Returns:
        None
    """
    gene_features = []
    with open(gff_file, "r") as gff:
        for line in gff:
            if line.startswith("#"):
                continue  # Skip comment lines
            fields = line.strip().split("\t")
            if len(fields) >= 3 and fields[2] == "gene":
                gene_features.append(line)

    # Write gene features to the output file
    with open(output_filename, "w") as output_file:
        output_file.write("".join(gene_features))


def extract_gene_info(gff_file, output_filename):
    """
    Extracts gene IDs and descriptions from a GFF3 file and writes them to a new file.

    Args:
        gff_file (str): Path to the GFF3 file.
        output_filename (str): Path to the output file.

    Returns:
        None
    """
    gene_info = []
    with open(gff_file, "r") as gff:
        for line in gff:
            if line.startswith("#"):
                continue  # Skip comment lines
            fields = line.strip().split("\t")
            if len(fields) >= 9 and fields[2] == "gene":
                gene_id = fields[8].split(";")[0].split("=")[1]
                description = fields[8].split(";")[3].split("=")[1]
                gene_info.append(f"{gene_id} - {description}")

    # Write gene info to the output file
    with open(output_filename, "w") as output_file:
        output_file.write("\n".join(gene_info))
