import json
import matplotlib.pyplot as plt
from collections import Counter

def compute_and_visualize_metrics(log_file_path):
    """
    Compute execution accuracy, average similarity scores (sequence and BLEU),
    and visualize the distribution of these metrics.

    Args:
        log_file_path (str): Path to the JSON log file.
    """
    with open(log_file_path, "r", encoding="utf-8") as file:
        execution_log = json.load(file)

    total_queries = len(execution_log)
    matching_queries = 0
    total_sequence_similarity = 0
    total_bleu_similarity = 0
    valid_sequence_similarity_count = 0
    valid_bleu_similarity_count = 0
    error_types = Counter()

    sequence_similarities = []
    bleu_similarities = []

    for entry in execution_log:
        # Calculate matching queries for execution accuracy
        if entry.get("execution_accuracy", False):
            matching_queries += 1

        # Calculate sequence similarity score if available
        sequence_similarity_score = entry.get("sequence_similarity_score")
        if sequence_similarity_score is not None:
            total_sequence_similarity += sequence_similarity_score
            valid_sequence_similarity_count += 1
            sequence_similarities.append(sequence_similarity_score)

        # Calculate BLEU similarity score if available
        bleu_similarity_score = entry.get("bleu_similarity_score")
        if bleu_similarity_score is not None:
            total_bleu_similarity += bleu_similarity_score
            valid_bleu_similarity_count += 1
            bleu_similarities.append(bleu_similarity_score)

        # Record error types
        if entry.get("output_error"):
            error_types[entry["output_error"]] += 1

    # Compute metrics
    execution_accuracy = (matching_queries / total_queries) * 100 if total_queries > 0 else 0
    average_sequence_similarity_score = (
        total_sequence_similarity / valid_sequence_similarity_count
        if valid_sequence_similarity_count > 0
        else 0
    )
    average_bleu_similarity_score = (
        total_bleu_similarity / valid_bleu_similarity_count
        if valid_bleu_similarity_count > 0
        else 0
    )

    # Print results
    metrics = {
        "Total Queries": total_queries,
        "Matching Queries": matching_queries,
        "Execution Accuracy (%)": execution_accuracy,
        "Average Sequence Similarity Score": average_sequence_similarity_score,
        "Average BLEU Similarity Score": average_bleu_similarity_score,
        "Error Types": dict(error_types)
    }
    print(json.dumps(metrics, indent=4))

    # Visualize similarity score distributions
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.hist(sequence_similarities, bins=20, color='skyblue', edgecolor='black')
    plt.title('Sequence Similarity Score Distribution')
    plt.xlabel('Sequence Similarity Score')
    plt.ylabel('Frequency')

    plt.subplot(1, 2, 2)
    plt.hist(bleu_similarities, bins=20, color='salmon', edgecolor='black')
    plt.title('BLEU Similarity Score Distribution')
    plt.xlabel('BLEU Similarity Score')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.show()

log_file_path = "query_execution_comparison_log.json" 
compute_and_visualize_metrics(log_file_path)
