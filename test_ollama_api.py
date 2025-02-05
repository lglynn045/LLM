import requests
import json
from requests.exceptions import Timeout, ConnectionError

class OllamaAPI:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.timeout = 30
        
    def generate(self, prompt, model="deepseek-r1:8b", options=None):
        """
        Generate a response using the Ollama API with streaming
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True  # Enable streaming
        }
        
        if options:
            for key, value in options.items():
                payload[key] = value
            
        try:
            print(f"Sending request to {url}")
            
            # Make streaming request
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            # Collect the complete response
            full_response = ""
            print("Receiving response:")
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line)
                    chunk = json_response.get('response', '')
                    print(chunk, end='', flush=True)  # Print each chunk as it arrives
                    full_response += chunk
                    
                    # Check if this is the last message
                    if json_response.get('done', False):
                        break
            
            print("\n")  # Add newline after response
            return full_response
            
        except Timeout:
            print("Request timed out after {} seconds".format(self.timeout))
            return None
        except ConnectionError:
            print("Failed to connect to Ollama server. Make sure it's running.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response text: {e.response.text}")
            return None

    def list_models(self):
        """List all available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            return response.json()['models']
        except requests.exceptions.RequestException as e:
            print(f"Error listing models: {e}")
            return None

def test_connection():
    """Test the connection to Ollama server"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        return True
    except:
        return False

if __name__ == "__main__":
    # First test the connection
    print("Testing connection to Ollama server...")
    if not test_connection():
        print("Cannot connect to Ollama server. Make sure it's running on http://localhost:11434")
        exit(1)
        
    # Initialize the API client
    ollama = OllamaAPI()
    
    # List available models
    print("\nListing models...")
    models = ollama.list_models()
    if models:
        print("Available models:")
        for model in models:
            print(f"- {model['name']}")
    
    # Generate a response with streaming
    print("\nSending test prompt...")
    response = ollama.generate("Tell me a short joke.", model="deepseek-r1:8b")
    
    print("\nScript completed.")