# Algolia Solutions Architect Assignment

This repository contains:

- A Python script for uploading the supplied product dataset to Algolia
- A Svelte search UI built with Algolia InstantSearch.js

## Project structure

```bash
.
├── upload_script.py
├── requirements.txt
├── data.json
└── search_ui/
```


## Prerequisites

* Python 3
* Node.js and npm
* An Algolia application and index

## 1. Upload the product data

Place the desired JSON dataset in the repository root.

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Open `upload_script.py` and provide:

```python
DATA_FILE = 'data.json'
ALGOLIA_APP_ID = "YOUR_APPLICATION_ID"
ALGOLIA_API_KEY = "YOUR_WRITE_API_KEY"
ALGOLIA_INDEX_NAME = "YOUR_INDEX_NAME"
```

Run the upload:

```bash
python upload_script.py
```

The script:

1. Loads the JSON dataset
2. Confirms every record has a unique `objectID`
3. Uploads the records to the selected Algolia index

## 2. Run the search UI

Open the Svelte project:

```bash
cd search_ui
```

Install the dependencies:

```bash
npm install
```

Open `src/App.svelte` and provide:

```javascript
const ALGOLIA_APP_ID = "YOUR_APPLICATION_ID";
const ALGOLIA_SEARCH_API_KEY = "YOUR_SEARCH_ONLY_API_KEY";
const ALGOLIA_INDEX_NAME = "YOUR_INDEX_NAME";
```

Use an Algolia **Search-Only API key** in the frontend. Do not use the write or Admin API key.

Start the development server:

```bash
npm run dev
```

Open the local URL printed in the terminal, usually:

```text
http://localhost:5173
```

## Search features

The demo includes:

* Search-as-you-type
* Product result cards
* Brand filtering
* Price filtering
* Free-shipping filtering
* Active filter display
* Result counts
* Pagination
* Typo tolerance and Algolia relevance
