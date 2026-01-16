from dotenv import load_dotenv
import os
import cohere

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))
print(co)  # Should print a client object, no errors
