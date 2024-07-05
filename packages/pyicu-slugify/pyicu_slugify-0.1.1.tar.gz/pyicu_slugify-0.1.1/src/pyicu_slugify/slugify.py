from icu import Transliterator
import re

def pyicu_slugify(text, source_lang=''):
    # Create a transliterator from source language to ASCII
    trans = Transliterator.createInstance(f'{source_lang}-ASCII' if source_lang else 'Any-ASCII')
    
    # Transliterate to ASCII
    ascii_text = trans.transliterate(text)
    
    # Convert to lowercase
    lowercase_text = ascii_text.lower()
    
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^\w\s-]', '', lowercase_text)
    slug = re.sub(r'[-\s]+', '-', slug).strip('-_')
    
    return slug