import os
import json

_basedir = os.path.abspath(os.path.dirname(__file__))

_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r').read())
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r').read())


def get_string(key, language='ru'):
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    else:
        raise Exception('Invalid language')
