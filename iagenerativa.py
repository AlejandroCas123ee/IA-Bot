
import os
from pathlib import Path

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Carpeta donde están iagenerativa.py, .env y datos.txt
BASE_DIR = Path(__file__).resolve().parent

# Cargar las variables de entorno
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Crear el cliente solamente si existe una API key
client = genai.Client(api_key=API_KEY) if API_KEY else None


def leer_contexto() -> str:
    """Lee la base de conocimientos desde datos.txt."""

    ruta_datos = BASE_DIR / "datos.txt"

    print(f"[INFO] Buscando datos.txt en: {ruta_datos}")

    if not ruta_datos.is_file():
        print("[ERROR] No se encontró datos.txt.")
        return ""

    try:
        contexto = ruta_datos.read_text(encoding="utf-8").strip()

        if not contexto:
            print("[ERROR] El archivo datos.txt está vacío.")
            return ""

        print(
            f"[INFO] datos.txt cargado correctamente. "
            f"Caracteres: {len(contexto)}"
        )
        return contexto

    except OSError as error:
        print(f"[ERROR] No se pudo leer datos.txt: {error}")
        return ""


async def generar_respuesta(mensaje: str) -> str:
    """Genera respuestas mediante la API de Gemini."""

    mensaje = mensaje.strip()

    if not mensaje:
        return "Por favor, escribe una pregunta."

    if client is None:
        print("[ERROR] Falta configurar GEMINI_API_KEY.")
        return (
            "No está configurada la API de Gemini. "
            "Revisa la variable GEMINI_API_KEY en el archivo .env."
        )

    contexto = leer_contexto()

    if not contexto:
        return (
            "No puedo consultar la base de conocimientos porque "
            "datos.txt no existe, está vacío o no se pudo leer."
        )

    instrucciones = """
Eres CeniBot, un asistente educativo que orienta a los usuarios
sobre CENIGRAF y el SENA.

Responde en español, de forma natural, clara y útil.
Adapta cada respuesta a la pregunta del usuario.

Utiliza datos.txt como fuente principal para la información
específica de la institución.

No inventes programas de formación, fechas, requisitos,
duraciones, horarios ni datos oficiales.

Si la información institucional solicitada no aparece en
la base de conocimientos, explica que no tienes ese dato
confirmado y recomienda consultar los canales oficiales del SENA.

Puedes explicar conceptos generales de tecnología y educación
con tus conocimientos generales, distinguiéndolos de los datos
institucionales que no estén confirmados.
"""

    contenido = f"""
{instrucciones}

BASE DE CONOCIMIENTOS:
<contexto>
{contexto}
</contexto>

PREGUNTA DEL USUARIO:
{mensaje}
"""

    try:
        respuesta = await client.aio.models.generate_content(
            model=MODELO,
            contents=contenido,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=500,
            ),
        )

        texto = (respuesta.text or "").strip()

        if not texto:
            print("[ERROR] Gemini devolvió una respuesta vacía.")
            return "Gemini no generó una respuesta. Inténtalo nuevamente."

        return texto

    except Exception as error:
        print(f"[ERROR] Gemini ({type(error).__name__}): {error}")

        return (
            "No pude generar una respuesta en este momento. "
            "Inténtalo nuevamente y, si el problema continúa, "
            "revisa los errores que aparecen en la terminal."
        )
