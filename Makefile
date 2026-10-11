.PHONY: all tables clean

all: tables
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	mkdir -p output
	cp build/main.pdf output/manuscript.pdf

tables:
	python3 scripts/generate_tables.py

clean:
	latexmk -C -outdir=build main.tex
