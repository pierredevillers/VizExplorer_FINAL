import plotly.express as px
import plotly.graph_objects as go

def plot_similarity_distribution(similarity_scores):
    fig = px.histogram(
        x=similarity_scores,
        nbins=10,
        title="Distribution of Similarity Scores",
        labels={'x': 'Similarity Score'},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title="Similarity Score",
        yaxis_title="Frequency",
    )
    fig.show()

def plot_jaccard_similarity_distribution(jaccard_scores):
    """Plot the distribution of Jaccard Similarity scores."""
    fig = px.histogram(
        x=jaccard_scores,
        nbins=10,
        title="Jaccard Similarity Distribution",
        labels={"x": "Jaccard Similarity"},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title="Jaccard Similarity",
        yaxis_title="Frequency",
        bargap=0.2
    )
    fig.show()

def plot_bleu_distribution(bleu_scores):
    fig = px.histogram(
        x=bleu_scores,
        nbins=10,
        title="Distribution of BLEU Scores",
        labels={'x': 'BLEU Score'},
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title="BLEU Score",
        yaxis_title="Frequency",
    )
    fig.show()


def plot_processing_time_comparison(ref_stats, gen_stats):
    categories = ["Reference", "Generated"]
    average_times = [ref_stats["average"], gen_stats["average"]]
    min_times = [ref_stats["min"], gen_stats["min"]]
    max_times = [ref_stats["max"], gen_stats["max"]]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=average_times,
        name="Average",
        marker_color='blue'
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=max_times,
        name="Max",
        marker_color='red'
    ))

    fig.update_layout(
        title="Processing Time Comparison",
        xaxis_title="Categories",
        yaxis_title="Time (seconds)",
        barmode='group',
        template="plotly_white"
    )
    fig.show()   


def plot_queries_validation_breakdown(valid_generated, invalid_generated, non_sql):
    labels = ['Valid Generated Queries', 'Invalid Generated Queries', 'Non-SQL Responses']
    values = [valid_generated, invalid_generated, non_sql]
    colors = ['green', 'red', 'grey']
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors)
    )])


    fig.update_layout(
        title="Queries Validity Breakdown",
        template="plotly_white"
    )
    fig.show()   

