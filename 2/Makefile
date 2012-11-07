all:
	rm -rf ./data/naive_bayes_model
	./train ./data/train.csv ./data/naive_bayes_model
pre:
	./test ./data/naive_bayes_model ./data/test-data.csv ./pre
test:
	nosetests -s project/mytest.py
report:
	pandoc report.md -o hq2124-report.pdf
clean:
	rm -rf ./pre
	rm -rf ./hq2124-report.pdf
