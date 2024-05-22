import json
import os
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))

def create_assistant(client):
    assistant_file_path = "assistant.json"

    if os.path.exists(assistant_file_path):
        with open(assistant_file_path, "r") as file:
            assistant_data = json.load(file)
            assistant_id = assistant_data["assistant_id"]
            print("Loaded existing assistant ID.")
    else:
        file = client.files.create(
            file=Path(os.path.join(basedir,"knowledge.docx")), purpose="assistants"
        )

        assistant = client.beta.assistants.create(
            instructions="""
                You are a customer service agent for Al Minbar Institute. Your job is to answer questions from clients on our website using the provided documents. Follow these guidelines:

                1. Your answers must be concise and brief unless the client asks for more details.
                2. Respond as if you are a member of our staff, referring to Al Minbar Institute as 'We' or 'Our' in your responses.
                3. Do not initiate any processes.
                4. If you cannot answer a question using the provided documents, recommend reaching out to this email for more information: minbar@example.com.
                5. IMPORTANT: Never mention 'documents,' 'internal information,' 'files,' or any similar term to the client. Simply provide the best possible answer or direct them to the contact email if necessary.
                Under no circumstances should you refer to the source of your information. Always present yourself as part of our team.
          """,
            model="gpt-3.5-turbo-0125", # or  gpt-4-1106-preview
            tools=[
                    # {"type": "code_interpreter"},
                    {"type": "retrieval"}
                ],
            file_ids=[file.id],
        )

        with open(assistant_file_path, "w") as file:
            json.dump({"assistant_id": assistant.id}, file)
            print("Created a new assistant and saved the ID.")

        assistant_id = assistant.id

    return assistant_id
