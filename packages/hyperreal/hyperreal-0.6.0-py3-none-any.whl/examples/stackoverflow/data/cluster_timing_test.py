from hyperreal import index, corpus, utilities, clustering

if __name__ == "__main__":
    corp = corpus.StackExchangeCorpus("stackoverflow.db")
    idx = index.Index("stackoverflow_index.db", corpus=corp)
    idx.initialise_clusters(n_clusters=1024, include_fields=["Post"], min_docs=10)
    idx.refine_clusters(iterations=1, group_test_batches=32, group_test_top_k=1)
