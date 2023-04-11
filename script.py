import openai
import os
os.environ["OPENAI_API_KEY"] = "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"

# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
openai.api_key = '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'
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an assistant that only prints the answers to the questions. A list of bash commands is the only response allowed. You don't have to write ennumerations, explanations, or conclusions. Only write bash commands. "},
        # {"role": "user", "content": "Write a morgage contract"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Build a react website in a local environment"}
    ]
)

print(response.choices[0].message.content.split("`"))
