from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import uuid

app = FastAPI()

API_URL = os.getenv("API_URL", "http://localhost:8000/auto")

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>AI Assistant</title>
        <style>
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #e0e7ff 0%, #f0fdfa 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .container {
                max-width: 700px;
                margin: 48px auto 0 auto;
                background: #fff;
                border-radius: 0;
                box-shadow: 0 8px 32px #0002, 0 1.5px 4px #0001;
                padding: 0 0 32px 0;
                overflow: hidden;
            }
            .header {
                background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
                color: #fff;
                padding: 32px 32px 24px 32px;
                text-align: center;
                border-radius: 0;
                box-shadow: 0 2px 8px #0001;
            }
            .header h1 {
                margin: 0 0 8px 0;
                font-size: 2.2rem;
                letter-spacing: 1px;
            }
            .header p {
                margin: 0;
                font-size: 1.1rem;
                opacity: 0.92;
            }
            .tab-bar {
                display: flex;
                gap: 0;
                margin: 0 0 0 0;
                border-bottom: 1.5px solid #e5e7eb;
                background: #f3f4f6;
            }
            .tab-btn {
                flex: 1;
                padding: 16px 0;
                font-size: 1.1rem;
                background: none;
                border: none;
                border-bottom: 3px solid transparent;
                color: #6366f1;
                font-weight: 500;
                cursor: pointer;
                transition: background 0.2s, border-bottom 0.2s;
            }
            .tab-btn.active {
                background: #fff;
                border-bottom: 3px solid #6366f1;
                color: #0f172a;
            }
            #chat-section, #plan-section {
                padding: 32px 32px 0 32px;
            }
            #chat {
                height: 340px;
                overflow-y: auto;
                border-radius: 0;
                background: #f8fafc;
                border: 1.5px solid #e5e7eb;
                padding: 18px 16px 18px 16px;
                margin-bottom: 18px;
                box-shadow: 0 1.5px 4px #0001;
                display: flex;
                flex-direction: column;
            }
            .user, .bot {
                max-width: 80%;
                margin-bottom: 12px;
                padding: 12px 18px;
                border-radius: 0;
                word-break: break-word;
                font-size: 1.05rem;
                box-shadow: 0 1px 4px #0001;
            }
            .user {
                background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
                color: #fff;
                align-self: flex-end;
                margin-left: 20%;
                text-align: right;
            }
            .bot {
                background: #fff;
                color: #222;
                border: 1.5px solid #e5e7eb;
                align-self: flex-start;
                margin-right: 20%;
            }
            form {
                display: flex;
                gap: 10px;
                margin-top: 0;
            }
            input[type=text] {
                flex: 1;
                padding: 12px;
                border-radius: 0;
                border: 1.5px solid #cbd5e1;
                font-size: 1.05rem;
                background: #f1f5f9;
                transition: border 0.2s;
            }
            input[type=text]:focus {
                border: 1.5px solid #6366f1;
                outline: none;
            }
            button {
                padding: 12px 22px;
                border: none;
                border-radius: 0;
                background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
                color: #fff;
                font-weight: bold;
                font-size: 1.05rem;
                cursor: pointer;
                box-shadow: 0 1px 4px #0001;
                transition: background 0.2s;
            }
            button:disabled {
                background: #a5b4fc;
                cursor: not-allowed;
            }
            select {
                padding: 10px 12px;
                border-radius: 0;
                border: 1.5px solid #cbd5e1;
                background: #f1f5f9;
                font-size: 1.05rem;
            }
            .category {
                font-size: 0.95em;
                color: #6366f1;
                margin-bottom: 8px;
                font-weight: 500;
            }
            pre {
                background: #f3f4f6;
                border: 1.5px solid #e5e7eb;
                border-radius: 0;
                padding: 16px;
                font-size: 1.05rem;
                margin: 0 0 12px 0;
                overflow-x: auto;
            }
            code {
                font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
                font-size: 1.01em;
            }
            @media (max-width: 700px) {
                .container { max-width: 100vw; border-radius: 0; box-shadow: none; }
                #chat-section, #plan-section, .header { padding-left: 10px; padding-right: 10px; }
            }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>AI Assistant</h1>
                <p>Chat, plan, and automate with a beautiful, modern interface.</p>
            </div>
            <div class='tab-bar'>
                <button id='chat-tab' class='tab-btn active'>Chat</button>
                <button id='plan-tab' class='tab-btn'>Planner</button>
            </div>
            <div id='chat-section'>
                <div id='chat'></div>
                <form id='chat-form' autocomplete='off'>
                    <select id='model'>
                        <option value='llama3.2:3b'>Llama 3.2 3B</option>
                    </select>
                    <input type='text' id='message' placeholder='Type your message...' required autofocus />
                    <button type='submit'>Send</button>
                </form>
            </div>
            <div id='plan-section' style='display:none;'>
                <form id='plan-form' autocomplete='off' style='display:flex; gap:10px; margin-bottom:12px;'>
                    <input type='text' id='plan-query' placeholder='Enter your task (e.g., summarize invoices and email me)' required style='flex:1; padding:12px; border-radius:0; border:1.5px solid #cbd5e1; background:#f1f5f9; font-size:1.05rem;' />
                    <button type='submit'>Plan</button>
                </form>
                <pre id='plan-result' style='background:#f3f4f6; border:1.5px solid #e5e7eb; border-radius:0; padding:16px; min-height:60px;'></pre>
            </div>
        </div>
        <script>
            let sessionId = null;
            const chatDiv = document.getElementById('chat');
            const form = document.getElementById('chat-form');
            const input = document.getElementById('message');

            // Use the backend API URL from the server
            const API_URL = '""" + API_URL + """';

            // Generate a random session ID if not present
            function getSessionId() {
                if (!sessionId) {
                    if (window.crypto && window.crypto.randomUUID) {
                        sessionId = window.crypto.randomUUID();
                    } else {
                        sessionId = 'sess-' + Math.random().toString(36).substr(2, 12);
                    }
                }
                return sessionId;
            }

            let loadingMsg = null;
            let loadingInterval = null;
            function showLoading() {
                loadingMsg = document.createElement('div');
                loadingMsg.className = 'bot';
                loadingMsg.id = 'loading-msg';
                loadingMsg.textContent = 'Thinking';
                chatDiv.appendChild(loadingMsg);
                chatDiv.scrollTop = chatDiv.scrollHeight;
                let dots = 0;
                loadingInterval = setInterval(() => {
                    dots = (dots + 1) % 4;
                    loadingMsg.textContent = 'Thinking' + '.'.repeat(dots);
                }, 400);
            }
            function hideLoading() {
                if (loadingMsg) {
                    chatDiv.removeChild(loadingMsg);
                    loadingMsg = null;
                }
                if (loadingInterval) {
                    clearInterval(loadingInterval);
                    loadingInterval = null;
                }
            }

            function appendMessage(sender, text, category, code) {
                const msg = document.createElement('div');
                msg.className = sender;
                if (category && sender === 'bot') {
                    msg.innerHTML = `<span class='category'>[${category}]</span><br>` + text;
                } else {
                    msg.textContent = text;
                }
                if (code && sender === 'bot') {
                    const codeBlock = document.createElement('pre');
                    codeBlock.style.background = '#f5f5f5';
                    codeBlock.style.border = '1px solid #ddd';
                    codeBlock.style.borderRadius = '0';
                    codeBlock.style.padding = '12px';
                    codeBlock.style.position = 'relative';
                    codeBlock.style.marginTop = '8px';
                    const codeElem = document.createElement('code');
                    codeElem.textContent = code;
                    codeBlock.appendChild(codeElem);
                    const copyBtn = document.createElement('button');
                    copyBtn.textContent = 'Copy Code';
                    copyBtn.style.position = 'absolute';
                    copyBtn.style.top = '8px';
                    copyBtn.style.right = '8px';
                    copyBtn.style.padding = '4px 10px';
                    copyBtn.style.fontSize = '0.9em';
                    copyBtn.style.background = '#1a73e8';
                    copyBtn.style.color = '#fff';
                    copyBtn.style.border = 'none';
                    copyBtn.style.borderRadius = '0';
                    copyBtn.style.cursor = 'pointer';
                    copyBtn.onclick = () => {
                        navigator.clipboard.writeText(code);
                        copyBtn.textContent = 'Copied!';
                        setTimeout(() => { copyBtn.textContent = 'Copy Code'; }, 1200);
                    };
                    codeBlock.appendChild(copyBtn);
                    msg.appendChild(codeBlock);
                }
                chatDiv.appendChild(msg);
                chatDiv.scrollTop = chatDiv.scrollHeight;
            }

            form.onsubmit = async (e) => {
                e.preventDefault();
                const message = input.value.trim();
                const model = document.getElementById('model').value;
                if (!message) return;
                appendMessage('user', message);
                input.value = '';
                form.querySelector('button').disabled = true;
                showLoading();
                try {
                    const res = await fetch(API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, session_id: getSessionId(), model })
                    });
                    const data = await res.json();
                    sessionId = data.session_id || sessionId;
                    hideLoading();
                    appendMessage('bot', data.response, data.category, data.code);
                } catch (err) {
                    hideLoading();
                    appendMessage('bot', 'Error: Could not reach backend.');
                }
                form.querySelector('button').disabled = false;
            };

            // Tab logic
            const chatTab = document.getElementById('chat-tab');
            const planTab = document.getElementById('plan-tab');
            const chatSection = document.getElementById('chat-section');
            const planSection = document.getElementById('plan-section');
            chatTab.onclick = () => {
                chatSection.style.display = '';
                planSection.style.display = 'none';
                chatTab.style.background = '#e3e3e3';
                planTab.style.background = '';
            };
            planTab.onclick = () => {
                chatSection.style.display = 'none';
                planSection.style.display = '';
                planTab.style.background = '#e3e3e3';
                chatTab.style.background = '';
            };
            chatTab.style.background = '#e3e3e3';

            // Planner logic
            const PLAN_API_URL = 'http://localhost:8000/plan';
            const planForm = document.getElementById('plan-form');
            const planQuery = document.getElementById('plan-query');
            const planResult = document.getElementById('plan-result');
            planForm.onsubmit = async (e) => {
                e.preventDefault();
                planResult.textContent = 'Planning...';
                try {
                    const res = await fetch(PLAN_API_URL, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: planQuery.value })
                    });
                    const data = await res.json();
                    planResult.textContent = JSON.stringify(data.steps, null, 2);
                } catch (err) {
                    planResult.textContent = 'Error: Could not reach backend.';
                }
            };
        </script>
    </body>
    </html>
    """ 