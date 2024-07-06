# Ignacio Bot

A simple Flask App that uses a fine-tuned OpenAI model to let users chat with a custom bot. 
The bot is trained on interview transcripts from youtube. Additional information can be provided by editing the file system_context.txt.

To run the app, user must set **OPENAI_API_KEY** environment variable, which can be obtained from OpenAI.

The app has been tested on M1 Macbook Air running Python version 3.11.9. 

Install the packages using:
```
pip install -e .
```

Run the app using the executable in your virtual environment:
```
./venv/bin/ignacio_bot
```

The chatbot will be availabe through a browser at the URL: http://127.0.0.1:5000/ 