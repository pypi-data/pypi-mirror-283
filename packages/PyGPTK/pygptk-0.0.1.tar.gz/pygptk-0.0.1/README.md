# Gene Feature Extraction and Keyword Analysis

This repository contains Python functions for extracting gene features from a GFF3 file and performing keyword analysis using TF-IDF (Term Frequency-Inverse Document Frequency).

## Functions
<br>

### Extraction.py:
This file contains methods required to extract information from the genome and descriptions of organisms.
<hr>

### `extract_keywords(text: str) -> set`
Returns important keywords from a given text using TF-IDF. The function tokenizes the text, removes stopwords, and computes the TF-IDF scores. It then selects the top N words as keywords.

#### Args:
- `text` (str): The input text from which keywords are drawn.

#### Returns:
- `extraction` (set): A set of important keywords.

<hr>

### `extract_gene_features(gff_file: str, output_filename: str) -> None`
Extracts gene features from a GFF3 file and writes them to a new file.

#### Args:
- `gff_file` (str): Path to the GFF3 file.
- `output_filename` (str): Path to the output file.

<hr>

### `extract_gene_info(gff_file: str, output_filename: str) -> None`
Extracts gene IDs and descriptions from a GFF3 file and writes them to a new file.

#### Args:
- `gff_file` (str): Path to the GFF3 file.
- `output_filename` (str): Path to the output file.

<hr><br>

### Read.py
This file contains a method to read descriptions of genes and return ones that match to generated keywords.
<hr>

### `read_descriptions(fp: str, kwords: set) -> set`
Finds matching gene IDs and descriptions based on provided keywords.

#### Args:
- `fp` (str): The filepath to the gene descriptions text file.
- `kwords` (set): A set of keywords to search for.

#### Returns:
- `matching_descriptions` (set): A set of tuples containing matching gene IDs, descriptions, and keywords.

