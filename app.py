from flask import Flask, request, jsonify, render_template
import threading
import time
import requests
import json
from utils import generate_facts, get_text_from_log


app = Flask(__name__)
questions_and_facts = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        # Collect all link inputs
        links = request.form.getlist('links[]')

        post_res = requests.post("http://localhost:5000/submit_question_and_documents", json={"question": question, "documents":links})
        time.sleep(3)
        if post_res.status_code != 200:
            return "Unable to process your logs!"
        get_res = requests.get("http://localhost:5000/get_question_and_facts")

        if get_res.status_code == 200:
            return jsonify(get_res.text)

    return render_template('index.html')


def process_documents(question, documents):

    # Initialize the question status
    global questions_and_facts 
    questions_and_facts = {"question": question, "facts": None, "status": "processing"}

    log = ""
    try:
        for i in range(len(documents)):
            log += get_text_from_log(documents[i]) #+ "\n"
    except:
        pass

    facts = generate_facts(question, log)
    facts = [fact[2:] for fact in facts.split('\n')]

    questions_and_facts = {
        "question": question,
        "facts": facts,
        "status": "done"
    }


@app.route('/submit_question_and_documents', methods=['POST'])
def submit_question_and_documents():
    data = request.get_json()
    question = data["question"]
    documents = data["documents"]

    # Start a background thread to process documents and extract facts
    threading.Thread(target=process_documents, args=(question, documents)).start()

    return jsonify({}), 200


@app.route('/get_question_and_facts', methods=['GET'])
def get_question_and_facts():
    if questions_and_facts:
        return jsonify(questions_and_facts), 200
    else:
        return jsonify({"error": "Question not found"}), 404



if __name__ == '__main__':
    app.run(debug=False)
