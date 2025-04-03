from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Set Gemini API key directly
GEMINI_API_KEY = "AIzaSyBjWbCU9ler4HsHDLOKhSDz3mtRA3_uXEU"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize FastAPI app
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:5501"],  # Adjust for production security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request schema
# In chatbotback2.py, update the QueryRequest class
class QueryRequest(BaseModel):
    message: str = None
    disease_name: str = None
    query: str = None
    
@app.post("/query")
async def query_gemini(request: QueryRequest):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-001")
        
        # Determine which type of request we're handling
        if request.disease_name:
            # For disease descriptions
            prompt = f"Provide a concise description of the plant disease '{request.disease_name}', including symptoms and basic treatment recommendations in 2-3 sentences."
            print(f"Processing disease request for: {request.disease_name}")
        elif request.message:
            # For regular chat messages
            prompt = request.message
            print(f"Processing chat message: {prompt[:50]}...")
        else:
            return {"response": "No valid query provided"}
            
        # Generate response
        response = model.generate_content(prompt)
        
        return {"response": response.text.strip()}
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        # Return a JSON response even for errors
        return {"response": f"Error: {str(e)}", "error": True}