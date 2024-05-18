import openai
from sqlalchemy.orm import Session
from models import TranslationRequest, TranslationResult, IndividualTranslations
from datetime import datetime
from database import get_db
from typing import List
from my_secrets import api_key


# Set your OpenAI API key
openai.api_key = api_key


async def translate_text(text: str, language: str) -> str:
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following text to {language}:"},
            {"role": "user", "content": text},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

async def process_translations(request_id: int, text: str, languages: List[str]):
    with get_db() as session:
        for language in languages:
            translated_text = await translate_text(text, language)
            translation_result = TranslationResult(
                request_id=request_id, language=language, translated_text=translated_text
            )
            individual_translation = IndividualTranslations(
                request_id=request_id, translated_text=translated_text
            )
            session.add(translation_result)
            session.add(individual_translation)
            session.commit()
        request = session.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
        request.status = "completed"
        request.updated_at = datetime.utcnow()
        session.add(request)
        session.commit()