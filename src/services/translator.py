from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.CHUNK_SIZE = 4500
        
    def translate_text(self, text, to_lang='en'):
        try:
            translator = GoogleTranslator(source='auto', target=to_lang)
            return translator.translate(text)
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return None