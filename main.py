import logging
import time
import openai
from dotenv import find_dotenv,load_dotenv
import streamlit as st

load_dotenv()
# # openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()
model = "gpt-3.5-turbo-0125"

#upload a file to openAI embeddings
filepath = './word_power_made_easy.pdf'
file_object = client.files.create(file=open(filepath, "rb"), purpose="assistants")

#create an assistant
assistant = client.beta.assistants.create(
    name="Study Buddy",
    instructions="You are a study assistant for english language",
    tools=[{"type": "retrieval"}],
    model=model,
    file_ids=[file_object.id]
)

#get the assis id
assistant_id = assistant.id
print(assistant_id)

message = "What is a verb?"
thread = client.beta.threads.create()
thread_id = thread.id
print(thread_id)

run = client.beta.threads.runs.create(
  thread_id=thread_id,
  assistant_id=assistant_id,
  instructions="Please address the user as Aastha."
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    logging.info("Into wait function")
    while True:
        try:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")

                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            # You might want to handle the error differently here
            break
        time.sleep(sleep_interval)
logging.info("Waiting for run to complete...")

#Run
wait_for_run_completion(client=client,thread_id=thread_id,run_id=run.id)  
# ==== Steps --- Logs ==
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Steps---> {run_steps.data[0]}")      
