from pymongo import MongoClient
import os, json, numpy as np
from scipy import sparse
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import decomposition, linear_model, metrics


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


def tdm(client, db_name, topics):
    corpus = {}
    labels = []
    for t in topics:
        corpus[t] = [d["contents"] for d in client[db_name][t].find({})]

    analyzer = CountVectorizer(stop_words=None).build_analyzer()

    def plurality_stemming(doc):
        return [w[:-1] if w[-1] == "s" else w for w in analyzer(doc)]

    transformer = CountVectorizer(
        stop_words=None, min_df=10, analyzer=plurality_stemming)
    flattened_docs = []
    labels = []
    for label, docs in corpus.items():
        flattened_docs.extend(docs)
        labels.extend([label for _ in range(len(docs))])
    labels = np.array(labels)
    train_feats, test_feats, train_labels, test_labels = train_test_split(
        flattened_docs,
        labels,
        stratify=labels,
        test_size=0.3,
        random_state=40)
    train_feats = transformer.fit_transform(train_feats)
    test_feats = transformer.transform(test_feats)
    return [
        train_feats.toarray(),
        test_feats.toarray(), train_labels, test_labels
    ]


def reduce_dims(train_feats, test_feats):
    n_components = 800
    decomposer = decomposition.PCA(
        n_components=n_components,
        whiten=True,
        svd_solver="randomized",
        random_state=41)
    train_feats = decomposer.fit_transform(train_feats)
    print("{} components contain {} amount of variance".format(
        n_components, decomposer.explained_variance_ratio_.sum()))
    test_feats = decomposer.transform(test_feats)
    return train_feats, test_feats


def fit_model(train_feats, train_labels):
    model = linear_model.LogisticRegressionCV(
        n_jobs=4, random_state=40, solver="lbfgs", multi_class="ovr", cv=10)
    model.fit(train_feats, train_labels)
    return model


if __name__ == "__main__":
    client = create_connection()
    data_folder = "/workingdir/StackExchange_posts"
    db_name = "stack"
    insert_data(client, db_name, data_folder)
    print("data uploaded to mongodb\n")

    topics = ["beer", "aviation", "pets", "astronomy", "outdoors"]
    datasets = tdm(client, db_name, topics)
    print("term-document matrix constructed")
    print("data set split with n={} for training and n={} for test\n".format(
        datasets[0].shape[0], datasets[1].shape[0]))

    old_feat_size = datasets[0].shape[1]
    datasets[0], datasets[1] = reduce_dims(datasets[0], datasets[1])
    print("dimensionality reduced from {} to {}\n".format(
        old_feat_size, datasets[0].shape[1]))

    model = fit_model(datasets[0], datasets[2])
    print("model trained with train error {} test error {}\n".format(
        model.score(datasets[0], datasets[2]),
        model.score(datasets[1], datasets[3])))

    print("validation set confusion matrix:")
    print(metrics.confusion_matrix(model.predict(datasets[1]), datasets[3]))

    client.drop_database(db_name)
