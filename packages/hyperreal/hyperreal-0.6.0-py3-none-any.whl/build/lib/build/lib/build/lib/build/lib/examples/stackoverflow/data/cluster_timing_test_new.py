from hyperreal import index, corpus, utilities, clustering

if __name__ == "__main__":
    corp = corpus.StackExchangeCorpus("stackoverflow.db")
    idx = index.Index("stackoverflow_index.db", corpus=corp)
    features = set()

    for cluster_id in idx.cluster_ids:
        for f in idx.cluster_features(cluster_id):
            features.add(tuple(f[1:3]))

    clusters = clustering.cluster_features(
        idx, features, 1000, 10, group_layer_sizes=[100, 10]
    )

    idx = index.Index("stackoverflow_index.db", corpus=corp)
    idx._update_cluster_feature(
        {
            cluster_id: {idx.lookup_feature_id(feature) for feature in features}
            for cluster_id, features in clusters.items()
        }
    )
