## How to run the assignment:

0. Dependencies
 -- Docker is required to run this assignment along with a unix/linux environment

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

4. **Bonus**:

## Deviations from the recipe

Patrick said to note down deviations that I felt were better than the instructions:

 -- I did not follow step #2 (use the 1000 most common words as feature space). We expect the word count features to be highly correlated with each other given topic/item of discussion, and this is the ideal case for PCA. It'll work better with most of these features left in. On the other hand, I did use a minimum document frequency threshold for words -- if a word didn't appear in at least 10 documents in the training set, it wasn't used as a feature. This was done for computational tractibility reasons when computing PCA. 10 was arbitrarily chosen (albeit would have been cross validated for if performance wasn't already so good...).
 -- I went to step #5 before step #3. The term-document matrix should be constructed and the PCA scheme devised without looking at the held out dataset (the instructions implied using the training and test data). These representation decisions and dimensionality reduction techniques are forms of "learning" that we don't want to pollute the objectiveness of our testing set with.
 -- I increased the propertion of the test set from 10% (approximately ~500) to 30%. I found different shuffles of the train/test split were having significant (>1-2%) differences in test error at the 10% threshold and this became insignificant (<0.25%) at the 30% threshold. 