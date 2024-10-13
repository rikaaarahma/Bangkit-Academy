## Setup Environment - Anaconda
```
conda create --name ecom-analysis python=3.9
conda activate ecom-analysis
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir ecom-analysis
cd ecom-analysis
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard.py
```