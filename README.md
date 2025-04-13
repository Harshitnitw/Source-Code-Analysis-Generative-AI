# End-to-end-Source-Code-Analysis-Generative-AI

# How to run?
### STEPS:

Clone the repository

```bash
Project repo: https://github.com/
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n venv python=3.10 -y
```

```bash
conda activate venv
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your MISTRAL_API_KEY credentials as follows:

```ini
MISTRAL_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


```bash
# Finally run the following command
python app.py
```

### Now, open the project and enter the public github repo link for which you want your source code analysis

### Ask relevent questions and doubts regarding your code in the chat

### To clear the repo, write "clear" in the chat

### Techstack Used:

- Python
- LangChain
- Flask
- MistralAI
- vector embeddings
- ChoromaDB
