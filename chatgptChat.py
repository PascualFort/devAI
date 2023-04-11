import openai
import os

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
openai.api_key = os.environ.get('OPENAI_API_KEY')
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that only prints the answers to the questions. A list of bash commands is the only response allowed. You don't have to write ennumerations, explanations, or conclusions. Only write bash commands. "},
        {"role": "user", "content": "Build a react website in a local environment"}
    ]
)

print(response.choices[0].message.content.split("`"))
