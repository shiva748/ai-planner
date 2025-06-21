import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import httpx
import json
import uuid
from fastapi.middleware.cors import CORSMiddleware
import re
from function_library import get_function_library
from fastapi import Body

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

# In-memory session context: {session_id: [history]}
session_context = {}

GENERAL_PROMPT = "You are a friendly and helpful AI assistant. Engage in natural conversation, answer questions, and help the user as best as you can."

class UseCaseRequest(BaseModel):
    message: str
    session_id: str = None
    model: str = None  # Allow user to specify model

class PlanRequest(BaseModel):
    query: str

class PlanResponse(BaseModel):
    steps: list

def get_session_id(request: UseCaseRequest):
    if request.session_id:
        return request.session_id
    return str(uuid.uuid4())

async def call_ollama(prompt: str, model: str = None) -> str:
    payload = {
        "model": model or OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auto")
async def auto_route(request: UseCaseRequest):
    session_id = get_session_id(request)
    history = session_context.setdefault(session_id, [])
    context = ""
    for turn in history:
        context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"
    full_prompt = f"{GENERAL_PROMPT}\n{context}User: {request.message}\nAssistant:"
    response = await call_ollama(full_prompt)
    history.append({"user": request.message, "assistant": response})

    # Detect code block in response
    code_match = re.search(r'```[a-zA-Z]*\n([\s\S]+?)```', response)
    if code_match:
        code = code_match.group(1).strip()
        plain = re.sub(r'```[a-zA-Z]*\n([\s\S]+?)```', '', response).strip()
        return JSONResponse(content={"response": plain, "code": code, "session_id": session_id})
    else:
        return JSONResponse(content={"response": response, "session_id": session_id})

def build_planner_prompt(query: str) -> str:
    function_library = get_function_library()
    func_list = '\n'.join([
        f"- {f['name']}: {f['description']} (inputs: {f['inputs']}, outputs: {f['outputs']})"
        for f in function_library
    ])
    prompt = f"""
You are an expert AI planning assistant. Your ONLY job is to output a valid JSON array of function call steps, and nothing else.
Do NOT include any explanation, markdown, or extra text.
Each step must be an object with 'function', 'arguments', and 'output'.
Use only the function names provided in the function library.
Sequence the steps logically to fulfill the user's request.

Function Library:
{func_list}

User Query: {query}

Respond ONLY with a JSON array of steps, each with 'function', 'arguments', and 'output'.

Example:
[
  {{"function": "retrieve_invoices", "arguments": {{"month": "March"}}, "output": "invoices"}},
  {{"function": "summarize_invoices", "arguments": {{"invoices": "invoices"}}, "output": "summary"}},
  {{"function": "send_email", "arguments": {{"recipient": "user@email.com", "content": "summary"}}, "output": "status"}}
]
"""
    return prompt

def extract_json_array(text: str) -> str:
    text = text.strip()
    if text.startswith('```'):
        text = re.sub(r'^```[a-zA-Z]*', '', text)
        text = text.strip('`\n')
    match = re.search(r'(\[.*?\])', text, re.DOTALL)
    if match:
        return match.group(1)
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

@app.post("/plan", response_model=PlanResponse)
async def plan(request: PlanRequest):
    prompt = build_planner_prompt(request.query)
    response = await call_ollama(prompt)
    print('Raw model response:', response)  # For debugging
    try:
        steps = json.loads(response)
        return {"steps": steps}
    except json.JSONDecodeError:
        json_str = extract_json_array(response)
        try:
            # Remove trailing commas
            json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
            steps = json.loads(json_str)
            return {"steps": steps}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Model did not return valid JSON. Raw response: {response}. Error: {e}")
