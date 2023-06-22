from translatepy import Translator

translator = Translator(fast=True)

def to_ka(txt_en: str):
    txt_ru = to_ru(txt_en)
    translation = translator.translate(txt_en,source_language='en',destination_language='ka').result
    return translation

def to_en(txt_ka: str):
    txt_ru = to_ru(txt_ka)
    translation = translator.translate(txt_ka,source_language='ka',destination_language='en').result
    return translation

def to_ru(txt: str):
    translation = translator.translate(txt,source_language='auto', destination_language='ru').result
    return translation

