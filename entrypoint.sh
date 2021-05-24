#!/usr/bin/env bash

# add variables to environment
source .env

# download nltk data
python -c "import models;models.download_nltk_data()"

# start bot server
python .
