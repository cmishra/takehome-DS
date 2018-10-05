from pymongo import MongoClient
import os, json, numpy as np
from sklearn.feature_extraction.text import CountVectorizer


def create_connection():
    mongo_url = "mongodb://localhost:27017"
    client = MongoClient(mongo_url)
    return client


def insert_data(client, db_name, data_folder):
    db = client[db_name]
    json_files = [f for f in os.listdir(data_folder) if f[-5:] == ".json"]
    for f in json_files:
        topic = db[f[:-11]]
        with open(data_folder + "/" + f, "r") as fin:
            for d in json.load(fin):
                doc = []
                doc.append(d["title"])
                doc.append(d["body"])
                doc.extend([p["body"] for p in d["answers"]])
                topic.insert_one({"contents": " ".join(doc)})
        print("{}:\t{}".format(f[:-11], topic.count_documents({})))


def tdm(client, db_name, topics):
    corpus = {}
    labels = []
    for t in topics:
        corpus[t] = [d["contents"] for d in client[db_name][t].find({})]

    analyzer = CountVectorizer(stop_words=None).build_analyzer()

    def plurality_stemming(doc):
        return [w[:-1] if w[-1] == "s" else w for w in analyzer(doc)]

    transformer = CountVectorizer(stop_words=None, analyzer=plurality_stemming)
    flattened_docs = []
    labels = []
    for label, docs in corpus.items():
        flattened_docs.extend(docs)
        labels.extend([label for _ in range(len(docs))])
    X = transformer.fit_transform(flattened_docs)
    print(X.shape)
    labels = np.array(labels).reshape((-1, 1))
    print(labels.shape)
    return np.concatenate([np.array(X), labels], axis=1)


if __name__ == "__main__":
    client = create_connection()
    data_folder = "/workingdir/StackExchange_posts"
    db_name = "stack"
    insert_data(client, db_name, data_folder)
    print("Data uploaded to mongodb")
    topics = ["beer", "aviation", "pets", "astronomy", "outdoors"]
    feats = tdm(client, db_name, topics)
