import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def translate_text(source_text: str, source_language: str, target_language: str) -> str:
    try:
        prompt = f"Translate the following text from {source_language} to {target_language}: {source_text}"

        completion = await openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ]
        )

        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Translation error: {str(e)}")