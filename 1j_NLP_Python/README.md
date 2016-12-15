## Live Training - Natural Language Processing in Python

Notebooks, source data, and other materials for
[Get Started with Natural Language Processing in Python](https://www.safaribooksonline.com/live-training/courses/get-started-with-natural-language-processing-in-python/0636920065517/).

See the Docker container defined in https://github.com/montyz/nlp-12-14-2016
courtesy of @montyz, @ashapochka

Practical techniques for preparing text for cutom search, content recommenders, AI applications, and more.

Course code can be found [here](https://github.com/ceteri/a41124835ed0) - this repo is based on the courses sourece code!

Python provides a number of awesome packages for natural language processing (NLP), along with great ways to leverage the results. This course is a great practical jump-start to NLP and will explore Deep Learning with the following topics:
    - prep text for parsing
    - extract key phrases
    - prepare text for indexing in search
    - calculate similarity between documents
    - natural language generation
    - chatbots
    - ...and more

This is a great start for developing custom search, content recommenders, and even AI applications.


#### Links After Class Discussion
[NLP With Python](http://www.one-tab.com/page/hfnDmR4uTWWqpxXeqMtNCw)



#### The approaches to use today
    - Keyword analyis, n-grams, co-occurence, stemming, and other techniques from a previous generation of NLP tools are no longer the best approaches to use. 
    - Whether NLP request Big Data tooling and use of clusters; instead, the course will show practical applications on a laptop. 
    - That NLP work leading into AI applications is either fully automated or something which requires a huge amount of manual work; instead the course will demonstrate "human-in-the-loop" practices that make the best of both people skills and automation

####Benefits of using Python for NLP applications
    - How statistical parsing works
    - How resources such as [WordNet](https://wordnet.princeton.edu/) enhance text mining
    - How to extract more than just a list of keywords from a text
    - How to summarize and compare a set of documents
    - How deep learning gets used with natural language

#### The course helped participants to
    - Prepare texts for parsing - how to handle difficult Unicode
    - Parse sentences into annotated lists, structured as JSON output
    - Perform keyword randing using TF-IDF, while filtering stop words
    - Calculate a Jaccard similarity measure to compare texts
    - Leverage probabilistic data structures to perform the above more efficiently
    - Use Jupyter notebooks for sharing all of the above within their teams

#### PIP Installs
    - Python 3
    - Jupyter
    - BeautifulSoup4
    - TextBlob
    - polygot - replaced by spaCy
    - datasketch

####Course Notes
    - Text vs. Data Instead of Unicode vs. 8bit - article
    - Ligatures (F5 sequence and consolidate into 1 character) - python code we are using here will handle it
    - codecs - encoding/decoding -> saving an encoded string to a text file will also require identifying which encoding to use - this might be tricky
    - Character encoding - Character Filtering by Daniel Tunkelang; Query Understanding also by Daniel. 
    - Custom searches, recommenders, chatbots will require careful handling
    - Build functions and then use them in lambdas
    - Transformational grammars, link grammars, statistical parsing, NIST, Stanford Parser
    - Probabalistic methods split texts into sentences, annotate words with part-of-speech, chunk noun phrases, resolve named entities, estimate sentiment scores, etc.
    - TextBlog vs. NLTK - natural language processes in python
    - WordNet - large data source structures as database, binding with Python - lookup words and chase down their meaning and relation to other words

When working with words from sentences, they might have inflactions:
    - plular, verb -> normalize words by getting to root words
    - stemming - get to the root of the word by chopping the ends ("s", "ed") - computationally efficient, but distroys the data
    - lemmatize - look up a word in WordNet and get the actual root, which will generate the actual root - more presice

Noun phrase chunking
    - pull out the entire noun phrase that might pull out more than just simply keywords -> example 4
    - proper nouns: names of people, places - name entity resolution helps to extract these types of information; polyglot has the name entity rosolution; there is another example with spaCy for these more complicated issues for example 5

```bash
$ pip install textblob-aptagger
```

Once the text has been extracted and parsed, we need to reuse the result - there needs to be a good way to store the data on the disk
    - one of the good way is to store annotation in JSON
    - use pynlp.py -> ``` pynlp.full_parse() ```

Q/A:
    - does TextBlob support many languages -> yes
    - count various words -> to classify words and languages

    - TextBlog works well on production code; a lot of people like cpaSy; 
    - You can train your own nlp - but it is more advanced

    Fun things to do with the text:
    - TF-IDF - once the document is parsed count frequency of key fraces - weights of how important each keyword is
    - TF - term frequency - how often is a term appears
    - DF - document frequency - 

    Once we have a lot of annotated text (parsed documents, serialized to disk) how do we use it:
    - a common practice is to get rid of stop words: now, of, a, by, come, it
    - sometimes i might decide to add my stop words if I see that the results are skewed

Semantic Similarity:
    - compare two different documents and tell how close or far apart they are
    - Jaccard measure - how related terms/keyphrases/keywords are; how are documents compared to each other
    - Probabilistic data structures - use MinHash to calculate set intersectins for huge sets of data:
        - what is the distance between certain documents
        - set up a threshold
        - use this for building recommender systems

TextRank to extract key phrases
    - construct a graph from a paragraph of text - graph analytics - then run the pagerank algorithm on it
    - run PageRank on that graph
    - extract the highly ranked noun phrases
    - for a pure-Python implementation take a look at **pytextrank** for running a ranking algorithm
        - pytextrant - GitHub repo - use TextRank to extract key phrases from an article; it will also do summarization
    - symantic similarity - summary of the document
    - Use numbers to represent words to optimize NLP
    - Run through the parsed sentenses and rank the repeats, word annotation
    - TextRank also gives scores for the keyphrases
    - Take results from the textrank and now run symentic similarity (what are the most similar sentences) - this provides a nice summary - Auto-Summarization

Use the Docker Container - Meso and Kubernetes support for running the Docker containers
- go to DockerHub - lunch.bio

Q/A:
    - pull text -> parse -> get noun phrases, keyphrases, how can we start to relate what we have parsed to a larger database (let's say a database)
    - NLP - getting meaning out of the text - use WordNet to find definition/synonims for a word
        - for specific domains we need more specific databases
        - use Cycorp/OpenCyc - large dataset of words
            - this is what was used for Watson/Jeopardy
            - translate terms/phrases into meaning
        - RDF/Symantic Web -> AI

    - Use Spark for NLP at scale
    - pytextrank - TextRank - using the tutorial


- TextRank also gives scores for the keyphrases
- Take results from the textrank and now run symentic similarity (what are the most similar sentences) - this provides a nice summary - Auto-Summarization

Vector embedding:
    - once we come up with feature vector
    - use methods to map words, phrases, sentences, ... to numerical vectors - generally trained using deep learning
    - once words are put into phrases - to be able to go from 10 000 of phrases into a vector that is 1000 long
    - one of the ways to do it is using Word2Vec with the **gensim** library. The we'll query to find related terms
    - this approach can be used to enhance search - take a look at GPU Accelerated Natural Language Processing - Guillermo Molini, who describes the Happening platform for semantic search

Fun things to do with the text:
    - TF-IDF - once the document is parsed count frequency of key fraces - weights of how important each keyword is
    - TF - term frequency - how often is a term appears
    - DF - document frequency

Once we have a lot of annotated text (parsed documents, serialized to disk) how do we use it:
- a common practice is to get rid of stop words: now, of, a, by, come, it
- sometimes i might decide to add my stop words if I see that the results are skewed

Use the Docker Container - Meso and Kubernetes support for running the Docker containers
- go to DockerHub - lunch.bio
Fun things to do with the text:
- TF-IDF - once the document is parsed count frequency of key fraces - weights of how important each keyword is
- TF - term frequency - how often is a term appears
- DF - document frequency -

Once we have a lot of annotated text (parsed documents, serialized to disk) how do we use it:
- a common practice is to get rid of stop words: now, of, a, by, come, it
- sometimes i might decide to add my stop words if I see that the results are skewed

Vector embedding:
- once we come up with feature vector
- use methods to map words, phrases, sentences, ... to numerical vectors - generally trained using deep learning
- once words are put into phrases - to be able to go from 10 000 of phrases into a vector that is 1000 long
- one of the ways to do it is using Word2Vec with the **gensim** library. The we'll query to find related terms
- construct a graph from a paragraph of text - graph analytics - then run the pagerank algorithm on it
- run PageRank on that graph
- extract the highly ranked noun phrases
- for a pure-Python implementation take a look at **pytextrank** for running a ranking algorithm
    - pytextrant - GitHub repo - use TextRank to extract key phrases from an article; it will also do summarization
- symantic similarity - summary of the document
- Use numbers to represent words to optimize NLP
- Run through the parsed sentenses and rank the repeats, word annotation
- TextRank also gives scores for the keyphrases
- Take results from the textrank and now run symentic similarity (what are the most similar sentences) - this provides a nice summary - Auto-Summarization

A preview of advanced features:
- parse text to create a feature vector
- ...
