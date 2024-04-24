## Steps to run this project

1. Clone the repo and move to working directory
```
git clone https://github.com/gdevakumar/Cleric-Assignment-V2.git 

cd Cleric-Assignment-V2
```

2. Create a virtual environment using venv using Command Prompt or bash
```
python -m venv venv
```

2. Activate virtual environment on 
- Windows:
```
venv\Scripts\activate.bat
```
- Mac/Linux:
```
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Add OpenAI API key. Create a file `.env` in the current directory and replace `API_KEY` with your key.
```
OPENAI_API_KEY="API_KEY"
```

5. Run the Flask app to start the Front-end
```
python app.py
```
