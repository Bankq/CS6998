----------------------------------
CS6998 Search Engine Technology
2012 fall
Columbia Unviersity

Hang Qian
hq2124(at)columbia.edu
---------------------------------

Main Files:

- README
- install
- install_script
- query
- index
- raw_data/
- project/
---------/api.py
---------src/index.py
---------src/document.py
         

./install
        All the dependencies are included. ./install start a new shell and set the environment 
        to the current directory.

./index PATH
        For given PATH, ./index collect all the files under it and generate the index and metadata we need
        in the ./query.

./query
        - All valid queries are described in the instruction.md file.
        - Use "exit"/"quit"/CTRL-D to exit


In my approach, the Index object not only generates an inverted index but also contains all the data.
That may make the index file large, but consider the index step is off-line and we need our query respond
fast. I didn't use a data-base or a XML file to maintain the information, instead, I choose to use Python
built-in shelve object, which represented as plain text while able to contain and accessed any Python object.
So I just simply write the whole Index into the shelve. In practice, it has a good accessing time that makes
the program responds fast.

The api.py under project folder provides a higher level abstraction of data, which makes ./query more focusing
on handle the query and call the corresponding apis.
        
        
