.PHONY: install test simulate benchmark reproduce proposal clean

install:
	pip install -e .[dev]

test:
	pytest -q

simulate:
	openlift simulate --config configs/reference.yaml --output results/reference-run.csv

benchmark:
	openlift benchmark --config configs/reference.yaml --output results/benchmark.json

reproduce: test simulate benchmark

proposal:
	cd proposal && pdflatex -interaction=nonstopmode openlift-ded-proposal.tex && bibtex openlift-ded-proposal && pdflatex -interaction=nonstopmode openlift-ded-proposal.tex && pdflatex -interaction=nonstopmode openlift-ded-proposal.tex

clean:
	find proposal -maxdepth 1 -type f \( -name '*.aux' -o -name '*.bbl' -o -name '*.blg' -o -name '*.log' -o -name '*.out' \) -delete

