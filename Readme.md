## How to run the assignment:

0. Dependencies

* Docker is required to run this assignment

1. Clone the repo

```
git clone https://github.com/cmishra/takehome-DS.git
cd takehome-DS
```

2. Add data to folder StackExchange_posts

3. Start mongodb 

```
. .env.sh
buildImage && launchServer
```

4. Run and save model

```
. .env.sh
runScript
```

5. **Bonus**: Inference with sentences/documents sent as command line arguments:

```
runScript --inference conversations about my dog are the best! I love my dog :D
```

Here's what the output looks like:
1. Starting Mongodb

```
chetan@chetan-pc:~/projects/spine_takehome$ . .env.sh
chetan@chetan-pc:~/projects/spine_takehome$ buildImage && launchServer 
Sending build context to Docker daemon  25.12MB
Step 1/6 : FROM mongo:xenial
 ---> aff56fde18bf
Step 2/6 : RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates     libglib2.0-0 libxext6 libsm6 libxrender1     git mercurial subversion
 ---> Using cache
 ---> 264542982555
Step 3/6 : ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
 ---> Using cache
 ---> b87eb43416f4
Step 4/6 : ENV PATH /opt/conda/bin:$PATH
 ---> Using cache
 ---> a6f1b7063f1c
Step 5/6 : RUN wget --quiet https://repo.anaconda.com/archive/Anaconda2-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh &&     /bin/bash ~/anaconda.sh -b -p /opt/conda &&     rm ~/anaconda.sh &&     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh &&     echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc &&     echo "conda activate base" >> ~/.bashrc
 ---> Using cache
 ---> 53f83f00ef18
Step 6/6 : RUN conda upgrade pandas numpy seaborn && conda install pymongo
 ---> Using cache
 ---> 55c9acc8813b
Successfully built 55c9acc8813b
Successfully tagged jupyterlab:chetan
2018-10-07T23:47:31.071+0000 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols 'none'
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] MongoDB starting : pid=1 port=27017 dbpath=/data/db 64-bit host=1c21f2eda126
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] db version v4.0.2
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] git version: fc1573ba18aee42f97a3bb13b67af7d837826b47
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] OpenSSL version: OpenSSL 1.0.2g  1 Mar 2016
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] allocator: tcmalloc
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] modules: none
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] build environment:
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten]     distmod: ubuntu1604
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten]     distarch: x86_64
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten]     target_arch: x86_64
2018-10-07T23:47:31.075+0000 I CONTROL  [initandlisten] options: { net: { bindIpAll: true } }
2018-10-07T23:47:31.076+0000 I STORAGE  [initandlisten] 
2018-10-07T23:47:31.076+0000 I STORAGE  [initandlisten] ** WARNING: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine
2018-10-07T23:47:31.076+0000 I STORAGE  [initandlisten] **          See http://dochub.mongodb.org/core/prodnotes-filesystem
2018-10-07T23:47:31.076+0000 I STORAGE  [initandlisten] wiredtiger_open config: create,cache_size=15502M,session_max=20000,eviction=(threads_min=4,threads_max=4),config_base=false,statistics=(fast),log=(enabled=true,archive=true,path=journal,compressor=snappy),file_manager=(close_idle_time=100000),statistics_log=(wait=0),verbose=(recovery_progress),
2018-10-07T23:47:31.535+0000 I STORAGE  [initandlisten] WiredTiger message [1538956051:535821][1:0x7ffa9ad4aa00], txn-recover: Set global recovery timestamp: 0
2018-10-07T23:47:31.572+0000 I RECOVERY [initandlisten] WiredTiger recoveryTimestamp. Ts: Timestamp(0, 0)
2018-10-07T23:47:31.625+0000 I CONTROL  [initandlisten] 
2018-10-07T23:47:31.625+0000 I CONTROL  [initandlisten] ** WARNING: Access control is not enabled for the database.
2018-10-07T23:47:31.625+0000 I CONTROL  [initandlisten] **          Read and write access to data and configuration is unrestricted.
2018-10-07T23:47:31.625+0000 I CONTROL  [initandlisten] 
2018-10-07T23:47:31.626+0000 I STORAGE  [initandlisten] createCollection: admin.system.version with provided UUID: 0c5d4e0d-ffe5-4e81-8949-f06c7de58b67
2018-10-07T23:47:31.675+0000 I COMMAND  [initandlisten] setting featureCompatibilityVersion to 4.0
2018-10-07T23:47:31.684+0000 I STORAGE  [initandlisten] createCollection: local.startup_log with generated UUID: 2cbf08d3-3f70-450b-939c-a612e71bc5a7
2018-10-07T23:47:31.733+0000 I FTDC     [initandlisten] Initializing full-time diagnostic data capture with directory '/data/db/diagnostic.data'
2018-10-07T23:47:31.735+0000 I NETWORK  [initandlisten] waiting for connections on port 27017
2018-10-07T23:47:31.736+0000 I STORAGE  [LogicalSessionCacheRefresh] createCollection: config.system.sessions with generated UUID: d91a6331-9b6c-4691-a5e3-c95a36f9cc10
2018-10-07T23:47:31.811+0000 I INDEX    [LogicalSessionCacheRefresh] build index on: config.system.sessions properties: { v: 2, key: { lastUse: 1 }, name: "lsidTTLIndex", ns: "config.system.sessions", expireAfterSeconds: 1800 }
2018-10-07T23:47:31.811+0000 I INDEX    [LogicalSessionCacheRefresh]     building index using bulk method; build may temporarily use up to 500 megabytes of RAM
2018-10-07T23:47:31.813+0000 I INDEX    [LogicalSessionCacheRefresh] build index done.  scanned 0 total records. 0 secs

```


2. Running my code

```
chetan@chetan-pc:~/projects/spine_takehome$ . .env.sh
chetan@chetan-pc:~/projects/spine_takehome$ runScript 
Data uploaded to mongodb

Validation set confusion matrix:
[[328   7   0   7   4]
 [  3 442   0   6   4]
 [  0   0  84   0   0]
 [  5  13   4 424   6]
 [  0   0   2  12 397]]
Term-document matrix constructed with 7025 features

PCA used to reduce dimensionality to 800 retaining 0.953451105423 variance

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


* I did not follow step #2 (use the 1000 most common words as feature space):
 
(a) We expect the word count features to be highly correlated with each other given topic/item of discussion, and this is the ideal case for PCA. It'll work better with most of these features left in.

(b) On the other hand, I did use a minimum document frequency threshold for words -- if a word didn't appear in at least 10 documents in the training set, it wasn't used as a feature. This was done for computational tractibility reasons when computing PCA. 10 was arbitrarily chosen (albeit would have been cross validated for if performance wasn't already so good...).

* I went to step #5 before step #3. The term-document matrix should be constructed and the PCA scheme devised without looking at the held out dataset (the instructions implied using the training and test data for PCA). These representation decisions and dimensionality reduction techniques are forms of "learning" that we don't want to pollute the objectiveness of our testing set with.

* I increased the propertion of the test set from 10% (approximately ~500) to 30%. I found different shuffles of the train/test split were having significant (>1-2%) differences in test error at the 10% threshold and this became insignificant (<0.25%) at the 30% threshold.

* The test data was not created entirely randomly but with stratified sampling given the discussion label so that the test set was representative of the target distribution in the overall data 
