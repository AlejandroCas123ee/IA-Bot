"""Chatbot básico con API HTTP y una interfaz web mínima."""

from typing import Dict, List

# pyrefly: ignore[missing-import]
from fastapi import FastAPI
# pyrefly: ignore[missing-import]
from fastapi.responses import HTMLResponse
# pyrefly: ignore[missing-import]
from pydantic import BaseModel, Field
from iagenerativa import generar_respuesta

app = FastAPI(title="Chatbot básico", version="1.0.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: List[Dict[str, str]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


""" def responder(mensaje: str) -> str:
    Genera respuestas sobre CENIGRAF SENA.
    texto = mensaje.strip().lower()

    if not texto:
        return "Por favor, escribe un mensaje."

    if any(p in texto for p in ("hola", "buenas", "hey")):
        return "Hola, soy CeniBot. Estoy aquí para ayudarte con información sobre CENIGRAF SENA."

    if any(p in texto for p in ("nombre", "cómo te llamas", "quién eres")):
        return "Soy CeniBot, un chatbot que te orienta sobre CENIGRAF, su oferta educativa y sus servicios de formación."

    if any(p in texto for p in ("que es cenigraf", "qué es el sena")):
        return "CENIGRAF es el Centro para la Industria de la Comunicación Gráfica del SENA, ubicado en Bogotá. Está enfocado en la formación relacionada con la comunicación gráfica y la industria visual."

    if any(p in texto for p in ("oferta educativa", "qué puedo estudiar", "programas", "carreras")):
        return "CENIGRAF ofrece formación relacionada con la comunicación gráfica. Según la oferta disponible, puedes encontrar programas orientados al diseño gráfico, la producción gráfica, la impresión y los procesos editoriales. Estos programas buscan desarrollar habilidades para el sector gráfico."

    if any(p in texto for p in ("cursos", "cursos cortos", "capacitación")):
        return "El SENA ofrece cursos cortos para adquirir nuevos conocimientos y fortalecer habilidades laborales. Estos pueden incluir temas de diseño, herramientas digitales, producción gráfica y otras áreas, dependiendo de los cursos disponibles. Su duración y modalidad varían."

    if any(p in texto for p in ("inscripciones", "inscribirme", "cómo me inscribo")):
        return "Para inscribirte, debes elegir el programa o curso que te interesa, revisar las fechas de la convocatoria, verificar los requisitos y completar el proceso de inscripción indicado por el SENA."

    if any(p in texto for p in ("requisitos", "documentos", "qué necesito")):
        return "Los requisitos dependen del programa. Pueden incluir documento de identidad, un nivel educativo determinado y otras condiciones específicas. Es importante revisar los requisitos de ingreso antes de inscribirte."

    if any(p in texto for p in ("modalidad", "virtual", "presencial", "horarios")):
        return "La modalidad puede ser presencial o virtual, según el programa. Los horarios y las jornadas también varían. Cada convocatoria especifica cómo se desarrolla la formación y cuáles son los horarios disponibles."

    if any(p in texto for p in ("ubicación", "ubicacion", "dirección", "dónde queda")):
        return "CENIGRAF se encuentra en Bogotá, Colombia. Si deseas visitar el centro, es recomendable confirmar su dirección exacta y los horarios de atención antes de desplazarte."

    if any(p in texto for p in ("contacto", "teléfono", "correo", "cómo comunicarme")):
        return "Puedes comunicarte con CENIGRAF mediante los canales institucionales de atención del SENA. Allí puedes solicitar información sobre programas de formación, inscripciones, requisitos, horarios y servicios educativos."

    return f"Entiendo tu pregunta: «{mensaje.strip()} ». Puedo orientarte sobre programas, cursos, inscripciones y servicios de CENIGRAF. ¿Qué te gustaría conocer?"
 """

@app.get("/", response_class=HTMLResponse)
def pagina() -> str:
    return HTML


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    respuesta = await generar_respuesta(request.message)
    return ChatResponse(reply=respuesta)


HTML = r"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0e0709">
  <meta name="color-scheme" content="dark">
  <title>CeniBot · CENIGRAF SENA</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      color-scheme: dark;
      --red: #e0213f;
      --red-dark: #9c0f27;
      --red-glow: rgba(224, 33, 63, .35);
      --bg: #0e0709;
      --card: #170c0f;
      --panel: #120a0c;
      --bubble: #251317;
      --line: #3a1b21;
      --ink: #f6eaec;
      --muted: #a88c91;
    }
    * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body { height: 100%; }
    body {
      margin: 0;
      font: 15px/1.5 "Plus Jakarta Sans", system-ui, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(800px 500px at 90% -10%, rgba(224, 33, 63, .22) 0%, transparent 60%),
        radial-gradient(700px 500px at -10% 110%, rgba(156, 15, 39, .25) 0%, transparent 60%),
        var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1.25rem;
    }

    .app {
      width: 100%;
      max-width: 720px;
      height: min(780px, calc(100dvh - 2.5rem));
      display: flex;
      flex-direction: column;
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 22px;
      overflow: hidden;
      box-shadow: 0 30px 70px -20px rgba(0, 0, 0, .8), 0 0 60px -25px var(--red-glow);
    }

    /* Encabezado */
    .header {
      display: flex;
      align-items: center;
      gap: .9rem;
      padding: 1.1rem 1.4rem;
      color: #fff;
      background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%);
    }
    .avatar {
      width: 46px; height: 46px; flex: none;
      display: grid; place-items: center;
      border-radius: 50%;
      background: rgba(255, 255, 255, .16);
      border: 1.5px solid rgba(255, 255, 255, .5);
    }
    .avatar svg { width: 26px; height: 26px; fill: #fff; }
    .header h1 { margin: 0; font-size: 1.15rem; font-weight: 700; letter-spacing: -.01em; }
    .header p { margin: 0; font-size: .82rem; opacity: .85; }
    .status { margin-left: auto; display: flex; align-items: center; gap: .45rem; font-size: .8rem; opacity: .95; }
    .status i { width: 8px; height: 8px; border-radius: 50%; background: #7dffa8; box-shadow: 0 0 0 3px rgba(125, 255, 168, .25); }

    /* Conversación */
    #chat {
      flex: 1;
      min-height: 0;
      overflow-y: auto;
      overscroll-behavior: contain;
      padding: 1.4rem 1.2rem;
      display: flex;
      flex-direction: column;
      gap: .8rem;
      background: var(--panel);
      scroll-behavior: smooth;
    }
    #chat::-webkit-scrollbar { width: 8px; }
    #chat::-webkit-scrollbar-thumb { background: var(--line); border-radius: 8px; }

    .message {
      max-width: 82%;
      margin: 0;
      padding: .7rem 1rem;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      border-radius: 18px;
    }
    .message.bot {
      align-self: flex-start;
      background: var(--bubble);
      border: 1px solid var(--line);
      border-bottom-left-radius: 5px;
    }
    .message.user {
      align-self: flex-end;
      color: #fff;
      background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%);
      border-bottom-right-radius: 5px;
      box-shadow: 0 8px 18px -8px var(--red-glow);
    }
    .message.error {
      align-self: flex-start;
      color: #ffb9c4;
      background: rgba(224, 33, 63, .14);
      border: 1px solid var(--red);
      border-bottom-left-radius: 5px;
    }

    /* Indicador "escribiendo" */
    .typing { display: inline-flex; gap: 5px; padding: .85rem 1rem; }
    .typing span {
      width: 7px; height: 7px; border-radius: 50%;
      background: var(--red);
      opacity: .35;
      animation: blink 1.2s infinite;
    }
    .typing span:nth-child(2) { animation-delay: .15s; }
    .typing span:nth-child(3) { animation-delay: .3s; }
    @keyframes blink { 0%, 80%, 100% { opacity: .25; } 40% { opacity: 1; } }

    /* Formulario */
    form {
      display: flex;
      gap: .6rem;
      padding: .9rem 1rem 1rem;
      background: var(--card);
      border-top: 1px solid var(--line);
    }
    input {
      flex: 1;
      min-width: 0;
      padding: .85rem 1.1rem;
      font: inherit;
      font-size: 16px; /* evita el zoom automático en iPhone */
      color: var(--ink);
      background: var(--panel);
      border: 1.5px solid var(--line);
      border-radius: 999px;
      transition: border-color .15s, box-shadow .15s;
    }
    input::placeholder { color: var(--muted); }
    input:focus { outline: none; border-color: var(--red); box-shadow: 0 0 0 4px rgba(224, 33, 63, .22); }
    button {
      flex: none;
      display: inline-flex; align-items: center; justify-content: center; gap: .45rem;
      min-height: 46px;
      padding: .85rem 1.3rem;
      font: inherit; font-weight: 600;
      color: #fff;
      background: linear-gradient(135deg, var(--red) 0%, var(--red-dark) 100%);
      border: 0;
      border-radius: 999px;
      cursor: pointer;
      transition: transform .12s, box-shadow .12s, opacity .12s;
      box-shadow: 0 8px 18px -8px var(--red-glow);
    }
    button svg { width: 18px; height: 18px; fill: #fff; }
    button:hover { transform: translateY(-1px); box-shadow: 0 10px 20px -8px rgba(224, 33, 63, .6); }
    button:active { transform: translateY(0); }
    button:focus-visible { outline: 3px solid rgba(224, 33, 63, .5); outline-offset: 2px; }
    button:disabled { opacity: .5; cursor: not-allowed; transform: none; }

    /* Tablet y móvil */
    @media (max-width: 720px) {
      body { padding: 0; align-items: stretch; }
      .app {
        height: 100dvh;
        max-width: none;
        border: 0;
        border-radius: 0;
        box-shadow: none;
      }
      .header { padding: calc(.9rem + env(safe-area-inset-top, 0px)) 1rem .9rem; }
      .avatar { width: 40px; height: 40px; }
      .avatar svg { width: 22px; height: 22px; }
      #chat { padding: 1rem .85rem; }
      .message { max-width: 88%; }
      form { padding: .7rem .75rem calc(.8rem + env(safe-area-inset-bottom, 0px)); }
    }
    @media (max-width: 480px) {
      .status { display: none; }
      .header h1 { font-size: 1.05rem; }
      button span { display: none; }
      button { width: 46px; padding: 0; }
    }
    @media (prefers-reduced-motion: reduce) {
      * { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
    }
  </style>
</head>
<body>
  <main class="app">
    <header class="header">
      <div class="avatar" aria-hidden="true">
        <svg viewBox="0 0 24 24"><path d="M12 2a1.5 1.5 0 0 1 1.5 1.5V5H17a3 3 0 0 1 3 3v8a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3V8a3 3 0 0 1 3-3h3.5V3.5A1.5 1.5 0 0 1 12 2Zm-3 8.5a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3Zm6 0a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3ZM9 16a.75.75 0 0 0 0 1.5h6A.75.75 0 0 0 15 16H9Z"/></svg>
      </div>
      <div>
        <h1>CeniBot</h1>
        <p>Asistente de CENIGRAF SENA</p>
      </div>
      <div class="status"><i></i>En línea</div>
    </header>

    <div id="chat" aria-live="polite">
      <p class="message bot">¡Hola! Soy CeniBot. Pregúntame por programas, cursos, inscripciones o requisitos de CENIGRAF.</p>
    </div>

    <form id="form">
      <input id="message" autocomplete="off" placeholder="Escribe tu mensaje…" required maxlength="2000" aria-label="Mensaje">
      <button type="submit" id="send">
        <span>Enviar</span>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3.4 20.4 21 12 3.4 3.6 3.4 10l12 2-12 2z"/></svg>
      </button>
    </form>
  </main>

  <script>
    const chat = document.querySelector('#chat');
    const form = document.querySelector('#form');
    const input = document.querySelector('#message');
    const send = document.querySelector('#send');

    function addMessage(type, text) {
      const p = document.createElement('p');
      p.className = `message ${type}`;
      p.textContent = text;
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
      return p;
    }

    function showTyping() {
      const p = document.createElement('p');
      p.className = 'message bot typing';
      p.innerHTML = '<span></span><span></span><span></span>';
      chat.appendChild(p);
      chat.scrollTop = chat.scrollHeight;
      return p;
    }

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      addMessage('user', message);
      input.value = '';
      send.disabled = true;
      const typing = showTyping();
      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        if (!response.ok) throw new Error('No se pudo obtener una respuesta.');
        const data = await response.json();
        typing.remove();
        addMessage('bot', data.reply);
      } catch (error) {
        typing.remove();
        addMessage('error', `Error: ${error.message}`);
      } finally {
        send.disabled = false;
        input.focus();
      }
    });
  </script>
</body>
</html>"""