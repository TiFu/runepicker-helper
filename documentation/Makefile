all:
	cleaver ./howitworks.md
	sed -i -e 's/<div class="slide hidden  "/<div class="slide hidden" style="background-image: url(assets\/background.jpg); background-size: cover"/g' howitworks.html
	sed -i -e 's/<div class="slide"/<div class="slide" style="background:none; background-image: url(assets\/background.jpg); background-size: cover"/g' howitworks.html   
	sed -i -e 's/<div class="slide hidden"/<div class="slide hidden" style="background-image: url(assets\/background.jpg); background-size: cover"/g' howitworks.html
	sed -i -e 's/<div class="progress"/<div class="progress" style="z-index:100"/g' howitworks.html
	sed -i -e 's/<h1/<h1 style="margin-top:0px"/g' howitworks.html
	sed -i -e 's/<ul>/<ul style="font-weight: bold">/g' howitworks.html
	pandoc -s description.md -o description.html
	sed -i -e 's/<body>/<body style="color:white; font-size:120%;background-color: black; background-size: cover">/g' description.html