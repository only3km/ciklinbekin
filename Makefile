PYTHON = python3
OUTPUT = ./build
OUTPUT_RIME = "./build/Rime schema/"

all: clean createfolder homepage assets dfd ciklinbekin rime_schemas

clean:
	rm -rf $(OUTPUT)

createfolder:
	mkdir -p $(OUTPUT)
	mkdir -p $(OUTPUT_RIME)
	echo "This branch is generated from master" > $(OUTPUT)/README.txt

homepage: createfolder
	cd scripts/homepage && $(PYTHON) generate_homepage.py
	cp -rf scripts/homepage/javascripts $(OUTPUT)
	cp -rf scripts/homepage/stylesheets $(OUTPUT)

assets: createfolder
	cp -rf ./css $(OUTPUT)
	cp -rf ./img $(OUTPUT)

dfd: createfolder assets
	cd scripts && $(PYTHON) dfd_to_csv.py \
	  && $(PYTHON) dfd_to_rime.py \
	  && $(PYTHON) dfd_to_html.py
	cp -rf DFDCharacters.txt $(OUTPUT)
	cp -rf DFDRadicals.txt $(OUTPUT)

ciklinbekin: createfolder
	cd scripts && $(PYTHON) parse_ciklin.py
	cp -rf CikLinBekIn.md $(OUTPUT)
	cd scripts && $(PYTHON) CikLinBekIn.Export.py

rime_schemas: createfolder
	cp ./rime_schema/* "./build/Rime schema"
