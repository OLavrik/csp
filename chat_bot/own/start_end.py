import re

greeting_words = ['привет', 'здравствуйте',
                  'добрового времени суток',
                  'приветики', 'приветствую',
                  'здрасьте', 'добрый день',
                  'добрый вечер', 'доброе утро',
                  'день добрый']

def check_greeting(text: str) -> bool:
    result = False
    for word in greeting_words:
        pattern = f'^{word}' + r'\b.*'
        match = re.fullmatch(pattern, text.strip().lower())
        if match:
            result = True
    return result


farewell_words = ['пока', 'до встречи',
                  'счастливо', 'до свидания',
                  'прощай', 'до скорого',
                  'до скорой встречи']

def check_farewell(text: str) -> bool:
    if "пока" in text:
        return True
    result = False
    for word in farewell_words:
        pattern = f'^{word}' + r'\b.*'
        match = re.fullmatch(pattern, text.strip().lower())
        if match:
            result = True
    return result
