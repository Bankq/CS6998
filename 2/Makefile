all:
	rm -rf ./data/naive_bayes_model
	./train ./data/train.csv ./data/naive_bayes_model
pre:
	./test ./data/naive_bayes_model ./data/test-data.csv ./pre
test:
	nosetests -s project/mytest.py
clean:
	rm -rf ./pre
