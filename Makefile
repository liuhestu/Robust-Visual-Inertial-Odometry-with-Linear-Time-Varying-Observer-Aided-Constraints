.PHONY: all chinese tables clean

all: tables
	latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
	mkdir -p output
	cp build/main.pdf output/manuscript.pdf

chinese: tables
	python3 scripts/generate_chinese_tables.py
	latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build/zh main_zh.tex
	mkdir -p output
	cp build/zh/main_zh.pdf output/manuscript_zh.pdf

tables:
	python3 scripts/generate_tables.py

clean:
	latexmk -C -outdir=build main.tex
