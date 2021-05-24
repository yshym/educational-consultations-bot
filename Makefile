SPACY_MODEL=en_core_web_lg

.PHONY: spacy models docker

spacy:
	wget -nc "https://github.com/explosion/spacy-models/releases/download/$(SPACY_MODEL)-3.0.0/en_core_web_lg-3.0.0.tar.gz"

models: spacy
	python -c "import importlib;importlib.util.find_spec('$(SPACY_MODEL)') or exit(1)"
	[[ "$?" -eq 1 ]] \
		&& pip install "$(SPACY_MODEL)-3.0.0.tar.gz" \
		|| echo "SpaCy model is already installed"
	python init_models.py

docker: spacy
	docker build -t ec-bot .
