
all:
	echo "Downloading data...";
	cd data; \
	./downloadData.sh;
	cd data; \
	pip3 install -r requirements.txt; \
	mkdir -p wiki/ \
	python3 wiki_information.py;
