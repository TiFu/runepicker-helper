
all:
	echo "Downloading data...";
	cd data; \
	./downloadData.sh;
	cd data; \
	pip3 install -r requirements.txt; \
	mkdir -p wiki/html; \
	python3 download_wiki.py;
