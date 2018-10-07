## How to run the assignment:

0. Dependencies

* Docker is required to run this assignment

1. Clone the repo

```
git clone https://github.com/cmishra/takehome-DS.git
cd takehome-DS
```

2. Start mongodb 

```
. .env.sh
buildImage && launchServer
```

3. Run and save model

```
. .env.sh
runScript
```

4. **Bonus**: Inference with sentences/documents sent as command line arguments:

```
runScript --inference conversations about my dog are the best! I love my dog :D
```

Here's what the output looks like:

```
chetan@chetan-pc:~/projects/spine_takehome$ . .env.sh
chetan@chetan-pc:~/projects/spine_takehome$ runScript
Data uploaded to mongodb

Validation set confusion matrix:
[[1113    7    0    7    4]
[   3 1516    0    6    4]
[   0    0  293    0    0]
[   5   15    6 1472    7]
[   0    0    2   12 1354]]
Term-document matrix constructed with shape (5826, 7025)

PCA used to reduce dimensionality to (5826, 800) retaining 0.953451105423 variance

Model trained with train error 0.998773908779 test error 0.95823798627

Model saved
chetan@chetan-pc:~/projects/spine_takehome$ runScript --inference conversations about my dog are the best! I love my dog :D.
[('astronomy', 0.13620319598074593),
 ('aviation', 0.13899892928976595),
 ('beer', 0.010969681972934619),
 ('outdoors', 0.19123399468548538),
 ('pets', 0.5225941980710681)]

```

## Deviations from the recipe

Patrick said to note down deviations that I felt were better than the instructions:


* I did not follow step #2 (use the 1000 most common words as feature space).
 * We expect the word count features to be highly correlated with each other given topic/item of discussion, and this is the ideal case for PCA. It'll work better with most of these features left in.
* On the other hand, I did use a minimum document frequency threshold for words -- if a word didn't appear in at least 10 documents in the training set, it wasn't used as a feature. This was done for computational tractibility reasons when computing PCA.
 * 10 was arbitrarily chosen (albeit would have been cross validated for if performance wasn't already so good...).

* I went to step #5 before step #3. The term-document matrix should be constructed and the PCA scheme devised without looking at the held out dataset (the instructions implied using the training and test data for PCA). These representation decisions and dimensionality reduction techniques are forms of "learning" that we don't want to pollute the objectiveness of our testing set with.

* I increased the propertion of the test set from 10% (approximately ~500) to 30%. I found different shuffles of the train/test split were having significant (>1-2%) differences in test error at the 10% threshold and this became insignificant (<0.25%) at the 30% threshold.

* The test data was not created entirely randomly but with stratified sampling given the discussion label so that the test set was representative of the target distribution in the overall data