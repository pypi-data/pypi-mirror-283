def read_descriptions(fp, kwords):
    """
    :param fp: the filepath
    :param kwords: the keywords
    :return: matching gene ids and descriptions
    """
    # Read gene descriptions from the specified text file
    file_path = fp
    with open(file_path, "r") as file:
        gene_lines = [line.strip() for line in file]

    # Extract gene IDs and descriptions
    gene_descriptions = []
    for line in gene_lines:
        gene_id, description = line.split(" - ", 1)
        gene_descriptions.append((gene_id, description.strip()))

    # Find matching descriptions for each keyword
    matching_descriptions = []
    for keyword in kwords:
        for gene_id, desc in gene_descriptions:
            if keyword.lower() in desc.lower():
                matching_descriptions.append((gene_id, desc, keyword))

    md = set(matching_descriptions)
    return md
