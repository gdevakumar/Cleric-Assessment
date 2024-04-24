import os
from openai import OpenAI
import requests
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_facts(question, log):
    try:
        gpt_response = client.chat.completions.create(
            model="gpt-4",
            messages = [
                {
                    "role": "system",
    "content": """
You are an intelligent bot that summarizes and captures important facts from a given call log of discussion between team members. Based on the call log, extract only important facts, each one in a line in simple and clear language according to the given question. It must not have unnecessary facts and list of facts must not have double facts (two facts per line). Below are 3 examples for your reference:
Call Log: 
1
00:01:11,430 --> 00:01:40,520
John: Hello, everybody. Let's start with the product design discussion. I think we should go with a modular design for our product. It will allow us to easily add or remove features as needed.

2
00:01:41,450 --> 00:01:49,190
Sara: I agree with John. A modular design will provide us with the flexibility we need. Also, I suggest we use a responsive design to ensure our product works well on all devices. Finally, I think we should use websockets to improve latency and provide real-time updates.

3
00:01:49,340 --> 00:01:50,040
Mike: Sounds good to me. I also propose we use a dark theme for the user interface. It's trendy and reduces eye strain for users. Let's hold off on the websockets for now since it's a little bit too much work.

Question:
What are our product design decisions?

Facts:
- The team has decided to go with a modular design for the product.
- The team has decided to use a responsive design to ensure the product works well on all devices.
- The team has decided to use a dark theme for the user interface.


Call Log:
1
00:01:11,430 --> 00:01:40,520
John: After giving it some more thought, I believe we should also consider a light theme option for the user interface. This will cater to users who prefer a brighter interface.

2
00:01:41,450 --> 00:01:49,190
Sara: That's a great idea, John. A light theme will provide an alternative to users who find the dark theme too intense.

3
00:01:49,340 --> 00:01:50,040
Mike: I'm on board with that.

Question:
What are our product design decisions?

Facts:
- The team has decided to go with a modular design for the product.
- The team has decided to use a responsive design to ensure the product works well on all devices.
- The team has decided to provide both dark and light theme options for the user interface.


Call Log:
1
00:01:11,430 --> 00:01:40,520
John: I've been thinking about our decision on the responsive design. While it's important to ensure our product works well on all devices, I think we should focus on desktop first. Our primary users will be using our product on desktops.

2
00:01:41,450 --> 00:01:49,190
Sara: I see your point, John. Focusing on desktop first will allow us to better cater to our primary users. I agree with this change.

3
00:01:49,340 --> 00:01:50,040
Mike: I agree as well. I also think the idea of using a modular design doesn't make sense. Let's not make that decision yet.

Question:
What are our product design decisions?

Facts:
- The team has decided to focus on a desktop-first design
- The team has decided to provide both dark and light theme options for the user interface.
"""
},
{
    "role": "user",
    "content": """Give me facts based on the below discussion.
Call Log: 
{}

Question:
{}

Facts:
""".format(log, question)
                }
            ],
            temperature = 0.1
        )

        return gpt_response.choices[0].message.content

    except Exception as e:
        print(f"Processing failed due to {e} :( \nTry again later!")


def get_text_from_log(url):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
    else:
        text = ""
    return text

