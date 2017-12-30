
all: download database

database:
	python3 perkstyle/perkstyle.py 1000000

download:
	echo "Downloading data...";
	cd data; \
	./downloadData.sh;
	cd data; \
	pip3 install -r requirements.txt; \
	mkdir -p wiki/; \
	python3 wiki_information.py;
