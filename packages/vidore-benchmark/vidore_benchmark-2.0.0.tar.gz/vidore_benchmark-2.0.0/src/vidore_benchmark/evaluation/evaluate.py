from __future__ import annotations

from typing import Dict, List

from datasets import Dataset
import torch

from vidore_benchmark.retrievers.vision_retriever import VisionRetriever


def evaluate_dataset(
    vision_retriever: VisionRetriever,
    ds: Dataset,
    batch_query: int,
    batch_doc: int,
) -> Dict[str, float]:
    """
    Evaluate the model on a given dataset using the MTEB metrics.

    NOTE: The dataset should contain the following columns:
    - query: the query text
    - image_filename: the filename of the image
    - image: the image (PIL.Image) if `use_visual_embedding` is True
    - text_description: the text description (i.e. the page caption or the text chunks) if `use_visual_embedding` is False
    """

    # Dataset: sanity check
    col_documents = "image" if vision_retriever.use_visual_embedding else "text_description"
    required_columns = ["query", col_documents, "image_filename"]

    if not all(col in ds.column_names for col in required_columns):
        raise ValueError(f"Dataset should contain the following columns: {required_columns}")

    # Remove None queries and duplicates
    queries = list(set(ds["query"]))
    if None in queries:
        queries.remove(None)
        if len(queries) == 0:
            raise ValueError("All queries are None")

    documents = ds[col_documents]
    # Get the embeddings for the queries and documents - size (n_queries, emb_dim_query) and (n_documents, emb_dim_doc)
    emb_queries = vision_retriever.forward_queries(queries, batch_size=batch_query)
    emb_documents = vision_retriever.forward_documents(documents, batch_size=batch_doc)

    # Get the scores - size (n_queries, n_documents)
    scores = vision_retriever.get_scores(emb_queries, emb_documents)

    # Get the relevant documents and results
    relevant_docs, results = vision_retriever.get_relevant_docs_results(ds, queries, scores)

    # compute MTEB metrics
    metrics = vision_retriever.compute_metrics(relevant_docs, results)

    return metrics


def get_top_k(
    vision_retriever: VisionRetriever,
    queries: List[str],
    emb_queries: List[torch.Tensor],
    emb_documents: List[torch.Tensor],
    file_names: List[str],
    k: int,
) -> Dict[str, Dict[str, float]]:
    """
    Get the top-k documents for a given query.

    Output:
    {
        query_1: {
            document_1: score_1,
            ...
        },
        ...
    }
    """
    scores = vision_retriever.get_scores(emb_queries, emb_documents)

    passages2filename = {doc_idx: image_filename for doc_idx, image_filename in enumerate(file_names)}

    results = {}
    for query, score_per_query in zip(queries, scores):
        for docidx, score in enumerate(score_per_query):
            filename = passages2filename[docidx]
            score_passage = float(score.item())

            if query in results:
                results[query][filename] = max(results[query].get(filename, 0), score_passage)
            else:
                results[query] = {filename: score_passage}

        # Sort the results by score for each query
        results[query] = dict(sorted(results[query].items(), key=lambda item: item[1], reverse=True))

        # Get the top-k documents
        results[query] = dict(list(results[query].items())[:k])

    return results
