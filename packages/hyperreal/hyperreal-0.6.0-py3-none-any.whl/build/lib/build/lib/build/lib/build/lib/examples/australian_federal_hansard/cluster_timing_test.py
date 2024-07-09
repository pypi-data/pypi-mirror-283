from hyperreal import index, corpus, utilities, clustering
from hansard_corpus import HansardCorpus

if __name__ == "__main__":
    corp = HansardCorpus("tidy_hansard.db")
    idx = index.Index("tidy_hansard_index.db", corpus=corp)
    idx.initialise_clusters(n_clusters=1000, include_fields=["text"], min_docs=10)
    idx.refine_clusters(iterations=20, group_test_batches=100, group_test_top_k=2)
