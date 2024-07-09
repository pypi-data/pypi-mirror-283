import csv
import io
import zipfile
from hyperreal import corpus, index
from hyperreal.utilities import social_media_tokens


def iterate_file_tweets(*filenames):
    for fname in filenames:
        with zipfile.ZipFile(f"{fname}.zip", "r") as zfile:
            with zfile.open(f"{fname}.csv", mode="r") as data:
                textdata = io.TextIOWrapper(data)
                tweets = csv.reader(textdata)

                yield from tweets


if __name__ == "__main__":
    corp = corpus.PlainTextSqliteCorpus("tweets.db", tokeniser=social_media_tokens)
    tweets = (row[1] for row in iterate_file_tweets("tweets_2020") if not int(row[2]))
    corp.replace_docs(tweets)

    idx = index.Index("tweets_index.db", corpus=corp)
    idx.index(doc_batch_size=100000, index_positions=True)
    idx.initialise_clusters(512, min_docs=78, include_fields=["text"])
    idx.refine_clusters(iterations=100)
