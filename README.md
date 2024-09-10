# Rum Data Analysis

This project collects and analyses the rum data provided in [the rum ratings website](https://rumratings.com/). 

## Setup
1. This project uses `poetry` for dependency management. Follow the [installation instructions](https://python-poetry.org/docs/) to install poetry if not already
2. Install dependencies using poetry and activate the virtual environment:
```
poetry install
poetry shell
```
Note: switch to python 3.11 if running into errors. You can use [pyenv](https://github.com/pyenv/pyenv) to manage different python versions.
```
poetry env use 3.11
```

3. Start the app
```
python dashboard.py
```
4. Access the web-based dashboard via http://127.0.0.1:8050/

## Dashboard Preview
### Distribution
<img width="1728" alt="Screenshot 2024-09-10 at 3 00 39 PM" src="https://github.com/user-attachments/assets/a70c0e33-54f3-473d-9136-bf9980736fef">

### Relationship
<img width="1728" alt="Screenshot 2024-09-10 at 3 02 52 PM" src="https://github.com/user-attachments/assets/9c8dd7a7-856b-42b8-89f2-bbc716609e8f">

## Files
- `data` folder contains the original and preprocessed dataset and the scripts that are used to scrape the data.
- `data_analysis.ipynb` analyses the obtained dataset.

## Acknowledgement
- Rum ratings dataset
- Python
- [Project](https://github.com/mrpantherson/rum_scrape) for reference
- Bar Le Mal Necessaire and The Coldroom for inspiration 

