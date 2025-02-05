# LLM
Updated Feb 5th 2025

How to bring up LLM on local machine
 I used the guideline from
    https://www.datacamp.com/tutorial/deepseek-r1-ollama

to bring up the deepseek-r1:8b.

 I downloaded deepseek-r1:8b from Ollama
For me , this worked 
    % ollama serve
       This will bring up Ollama Server (no need for docker)
    This should be running on http://localhost:11434
    
    To test 
    % ollama run deepseek-r1:8b "hello"
    % curl http://localhost:11434/api/chat -d '{
     "model": "deepseek-r1:8b",
     "messages": [{ "role": "user", "content": "Solve: 25 * 25" }],
     "stream": false
If this works , you are up and flying. Otherwise Check if Server is running.

Next step , i wanted to try Python "test_ollama_api.py" . This file is included in Github . Good Luck

  % python test_ollama_api.py
Testing connection to Ollama server...

Listing models...
Available models:
- deepseek-r1:8b

Sending test prompt...
Sending request to http://localhost:11434/api/generate
Receiving response:
<think>
Okay, the user asked for a short joke. I need to come up with something simple and lighthearted.
  
