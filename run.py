from pymongo import MongoClient
import os, json, numpy as np
from scipy import sparse
from sklearn.preprocessing import LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import decomposition, linear_model, metrics, pipeline, base


class DiscussionDataset:
    db_name = "stack"
    topics = set()

    def __init__(self, mongo_url, data_folder):
        self.client = MongoClient(mongo_url)

        db = self.client[self.db_name]
        json_files = [f for f in os.listdir(data_folder) if f[-5:] == ".json"]
        for f in json_files:
            topic_name = f[:-11]
            topic = db[topic_name]
            self.topics.add(topic_name)
            with open(data_folder + "/" + f, "r") as fin:
                for d in json.load(fin):
                    doc = [d["title"], d["body"]]
                    doc.extend([p["body"] for p in d["answers"]])
                    topic.insert_one({"contents": " ".join(doc)})

        corpus = {}
        labels = []
        for t in self.topics:
            corpus[t] = [
                d["contents"] for d in self.client[self.db_name][t].find({})
            ]
        flattened_docs = []
        labels = []
        for label, docs in corpus.items():
            flattened_docs.extend(docs)
            labels.extend([label for _ in range(len(docs))])
        self.data = np.array(flattened_docs)
        self.target = np.array(labels)


def plurality_stemming(doc):
    analyzer = CountVectorizer(stop_words=None).build_analyzer()
    return [w[:-1] if w[-1] == "s" else w for w in analyzer(doc)]


class DenseTransformer(base.TransformerMixin):
    def transform(self, X, y=None, **fit_params):
        return X.todense()

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y, **fit_params)
        return self.transform(X)

    def fit(self, X, y=None, **fit_params):
        return self


class PipelineWithShapes(pipeline.Pipeline):
    shapes = []

    def predict(self, X, **predict_params):
        Xt = X
        for name, transform in self.steps[:-1]:
            if transform is not None:
                Xt = transform.transform(Xt)
                self.shapes.append((name, Xt.shape))
        return self.steps[-1][-1].predict(Xt, **predict_params)


if __name__ == "__main__":
    data_folder = "/workingdir/StackExchange_posts"
    mongo_url = "mongodb://localhost:27017"
    dataset = DiscussionDataset(mongo_url, data_folder)
    print("Data uploaded to mongodb\n")

    steps = [("vectorizer",
              CountVectorizer(
                  stop_words=None, min_df=10, analyzer=plurality_stemming)),
             ("todense", DenseTransformer()),
             ("reduce_dims",
              decomposition.PCA(
                  n_components=800,
                  whiten=True,
                  svd_solver="randomized",
                  random_state=40)),
             ("classifier",
              linear_model.LogisticRegressionCV(
                  n_jobs=4,
                  random_state=40,
                  solver="lbfgs",
                  multi_class="ovr",
                  cv=10))]

    process = PipelineWithShapes(steps)

    train_feats, test_feats, train_labels, test_labels = train_test_split(
        dataset.data,
        dataset.target,
        stratify=dataset.target,
        test_size=0.3,
        random_state=40)

    process.fit(train_feats, train_labels)

    print("Validation set confusion matrix:")
    print(
        metrics.confusion_matrix(
            process.predict(dataset.data), dataset.target))
    print("Term-document matrix constructed with shape {}\n".format(
        process.shapes[1][1]))
    print("PCA used to reduce dimensionality to {} retaining {} variance\n".
          format(process.shapes[2][1],
                 process.steps[2][1].explained_variance_ratio_.sum()))
    print("Model trained with train error {} test error {}\n".format(
        process.score(train_feats, train_labels),
        process.score(test_feats, test_labels)))

    dataset.client.drop_database(dataset.db_name)
