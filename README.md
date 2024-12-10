# Non-Profit-Search-Engine

## Setup

Create a virtual environment (first time only):

```sh
conda create -n nonprofit-env-2024 python=3.10
```

Activate the environment (whenever you come back to this project):

```sh
conda activate nonprofit-env-2024
```

Install packages:

```sh
pip install -r requirements.txt
```

## Usage

Run the non-profit search engine (Console):

```sh

python -m app.non_profit.py
```

Webapp:
flask run

## Testing

Run tests:

```sh
pytest
```