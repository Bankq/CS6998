		   CS 6998 Search Engine Technology
		 =====================================

          HW 1 Building a basic information retrieval system

                     Instructor: Dragomir Radev
                    TA: Hongzhi Li and Siyang Dai
               Contact: set_ta@lists.cs.columbia.edu
	           Due:   Oct. 10, 2012    11:55PM


	

In this project, you will build a basic information retrieval
system. Given a local corpus, your code will process the documents in
the corpus, and build an inverted index from them. After building the
index, your code will take a query, process it, find and rank
documents matching that query, and return a ranked list of results
with document snippets containing the query. Your code will also
handle several other requests to get statistics from the index. The
code should be as efficient as possible, so you will report the amount
of time spent indexing and handling queries, as well as the amount of
disk space used for the index. 
	Finally, you will have to find out the words similar in context to
the input word in all the documents. For this, you'll have to compute the 
list of similar words for all words.
	Extensions are possible for extra credit.


Before you start
================

Getting an account

You will need a CS account for this project. If you do not have a CS
account already, follow the instructions here: 

  https://www1.cs.columbia.edu/~crf/accounts/cs.html



Programming languages
=====================

This assignment could be implemented in c, c++, c#, Java, Python and Perl.


For the students who choose to use Perl, you can use the existing 
libraries (a) CPAN and (b) clairlib. Both resources will help you with
the assignment significantly. (Please refer to HW0.)
(Hint : Make use of Clairlib as much as possible. Particularly, these modules
 1.Clair::Utils::CorpusDownload;
 2.Clair::Utils::Idf;
 3.Clair::Utils::Tf;
and some others. )


For the students who want to use c/c++, you should submit a Makefile
to help TAs complie your code.

For the students who choose to use c#, your code should run on Mono runtime.
Please visit http://www.mono-project.com/Main_Page for more details. 

If you want to use other existing libraries, you have to contact with TAs to 
get permission before you can use them. 

Your code should run on a standard linux machine. If any external
libraries are needed, they should be included in your code submission
along with an installation script. The TAs will only be allowed to do
the following:

% cd tas-test-dir-for-df2141  (where df2141 stands for your login ID)
% gunzip df2141-install.tar.gz
% tar xf df2141-install.tar
% ./install
--> your system's output here
% ./index /path/to/raw/cranfield/data
--> your system's output here
% ./query
query1
--> your system's output here
query2
--> your system's output here
request1
--> your system's output here
request2
--> your system's output here

Grading
=======

Working code: 40%
 -- You should implement all following requirements. 

Efficiency and accuracy: 40%
 -- We will use some queries to test your program. 
 -- You should make your index file as small as possible.

Documentation: 20%

(up to 10% bonus will be given for particularly innovative extensions)


Requirements
============

1. Standardized input document representation

This assignment uses the Cranfield collection
(/home/cs6998/data/Cranfield_Collection/cranfieldDocs).  Cranfield
collection is a well-known IR test collection containing 1,400
aerodynamics' documents. Your code, however, should in principle work
with arbitrary textual documents. Cranfield documents follows the
following generic XML representation:

<DOC>
<DOCNO>
...
</DOCNO>
<TITLE>
...
</TITLE>
<AUTHOR>
...
</AUTHOR>
<BIBLIO>
...
</BIBLIO>
<TEXT>
...
</TEXT>
</DOC>


In the future, if you need to index another type of input documents, all you
should have to do is write a converter to the generic representation and the
rest of the code should remain the same.  


2. Queries

You should handle at least the following query types:

cat             : returns any document that has the word "cat" in it
cat dog         : any document that has one or more of these words
                 ("fuzzy or" is assumed by default)
cat dog rat     : up to 10 words in a query
"tabby cat"     : phrases of up to 5 words in length
"small tabby cat" "shaggy dog" : multiple phrases in a query
!cat
!"tabby cat"    : negations of single words or phrases
!cat !dog       : multiple negations per query

You don't need to worry about nested queries in parentheses. Note that
the default Boolean operator ("fuzzy or") above is an extension to
"AND" and "OR" and supersedes both.

3. Ranking

If multiple documents match, you should order them by decreasing score. The
score is defined as the number of query terms (or phrases) that match in the
"fuzzy or", including repetitions and counting phrases as the number of words
that are included in them. Negated terms are not included in the score.

For example, if the query is

cat dog "pack rat"

and you have three documents D1, D2, and D3 that contain at least one
of the query terms as follows:

D1: cat cat dog cat mouse
D2: pack rat cat rat rat
D3: rabbit elephant dog dog cat pack rat cat

their scores should be as follows:

D1: 4
D2: 3  ("pack rat" counts as two terms, but "rat" alone doesn't count)
D3: 6

4. Similarity

You have to find words similar in context. An example of this can be found on
http://nltk.googlecode.com/svn/trunk/doc/book/ch01.html
Read the section on concordance and similarity. You have to construct a list of 
similar words and when an input query such as "similar cat" is entered, all the 
words which are similar in context should be returned in the decreasing order of similarity.
For this section, your code won't be evaluated by the TAs. We will give you a list of words
and you have to return the list of similar words for each of them (i.e., just the output).

5. Extensibility

Your code should be extensible. In a future assignment, if you need to add
hyperlink functionality (e.g., indexing anchor text or running pagerank), it
should be easy to do so.  


Components
==========

Your system should consist of an API and a runtime part (a set of command-line
based programs that use the API).

API: You need to have the following classes (or modules). I have listed some
typical methods that each class should implement. Not all items below
correspond to specific methods. At the same time, you will probably need more
methods in addition to the ones on the list. Items in parentheses are not
required for this assignment but would in general be part of a practical
system. Furthermore, the list of modules is only shown as a guide. You can
deviate from it if needed.  
 
Note that this assignment is not web-specific. We will have a separate
web-specific assignment later.

Document
 - html parsing
 - stemming
 - lowercasing
 - tokenization
 - document segmentation
 - convert to common representation
 - summarization (pick snippets that contain the query terms)
 
Statistics
 - number of documents
 - word distributions (stemmed or not)
 - size of index

Index
 - build an inverted index
 - storing metadata

 Not required:
 - (add to an index)
 - (delete from index)
 - (optimizing the index)

Query
 - preprocess

Retrieval
 - document matching
 - document ranking

Evaluation
 - timing the indexing part
 - timing a retrieval

Error
 - print appropriate error messages if incorrect commands are typed

RUNTIME: You should provide the following runtime programs:

- install
- index
- query

Here is what each of them should do:

install

 - install your code in the "current" directory
 - your install script should not include the Cranfield data set
   but should instead allow the user to give a path to it (the
   standard path under /home/cs6998/data/Cranfield_Collection/cranfieldDocs)

index

 - build an index
 - give some basic statistics about the indexing, including time
   elapsed for index, amount of disk space used, number of words,
   number of documents, etc.

query
document snippets
containing the query

 - reads queries from standard input and prints a list of matching 
   documents ids and short summaries of matching documents. Each 
   line should contain a document id followed by a "tab" followed by 
   a document snippets containing the query.
 - see above for the required support for query types
 - reads requests from standard input and prints back statistics
 - the following request types should be supported:
   df "pack rat"     - shows the number of documents in which "pack
                       rat" appears in the index
   df rat            - shows the number of documents in which rat
                       appears in the index
   freq "pack rat"   - shows how many times the phrase "pack rat"
                       appears in the index
   doc 4562          - shows the full text of document 4562 (ideally
                       through a pager)
   tf 4562 rat       - shows the term frequency of rat in document 4562
   title 4562        - show the title of document 4562


Documentation
=============

Your code should be well commented. Write a brief document that describes
the architecture of your program and how to use your program.



Hints
=====

If you use Perl, try to stay within the clairlib paradigm as much as 
possible. Try to write your code in such a way that it can potentially 
be added to clairlib.

Sample additional features (for bonus points: maximum 10 bonus points)
======================================================================

- handle sophisticated queries
- perform vector retrieval
- web interface
- improve clairlib
- consistent use of XML throughout the system
- proximity-based reranking
- score normalization by document length
- score determined by idf

Deliverables
============

A single file called uni-install.tar.gz (e.g., cn2112-install.tar.gz) with
the following components:

- your code
- any external libraries needed (if appropriate)
- Makefile (if appropriate)
- the install, index, and query programs
- documentation
- Results (Similar word for a list of given words)

Unarchiving your *.tar.gz file and running ./install should be all
that we need to do to access your runtime code (index and query).

Submission
==========
Please submit all necessary
files in an archive called uni-install.tar.gz and upload it to the HW1 
on Courseworks.

Important
=========
If we cannot run the code as specified above, we will not grade it. We
will return it to you and penalize you by 10 points for each time we
have to go back to you for a new version.

Late Policy: Each day (or fraction of a day) that your homework is
late, your grade will decrease by 10 points.

Final notes
===========
We will spend time in class to discuss the assignment and clarify some
ambiguities.  It is recommended that you read the actual assignment
before class.  Some steps of the grading process will be
automated. Hence, It is very important that you strictly adhere to all
the requirements above.
