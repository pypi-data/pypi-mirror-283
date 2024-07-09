from hyperreal import index, corpus, utilities, clustering
from hansard_corpus import HansardCorpus

if __name__ == "__main__":
    corp = HansardCorpus("tidy_hansard.db")
    idx = index.Index("tidy_hansard_index.db", corpus=corp)
    features = set()

    for cluster_id in idx.cluster_ids:
        for f in idx.cluster_features(cluster_id):
            features.add(tuple(f[1:3]))

    clusters = clustering.cluster_features(
        idx, features, 1024, 100, group_layer_sizes=[32]
    )

    idx = index.Index("tidy_hansard_index.db", corpus=corp)
    idx._update_cluster_feature(
        {
            cluster_id: {idx.lookup_feature_id(feature) for feature in features}
            for cluster_id, features in clusters.items()
        }
    )
