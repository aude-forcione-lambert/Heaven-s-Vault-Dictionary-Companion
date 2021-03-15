import json

class Definition:
'''
Class encapsulating the different parts of a word's definition
'''

    def __init__(self, translation: str, components: list[str], confidence: int, notes:str):
    '''
    translation: word's translation in the user's language
    components: list of smaller words composing the ancient word
    confidence: confidence in the accuracy of the translation (0: unspecified, 1: low, 2: high, 3: confirmed)
    notes: additional user's notes
    '''
        self.translation = translation
        self.components = components
        self.confidence = confidence
        self.notes = notes


class Dictionary:
'''
Static class containing a dictionary of all words and usefull functions related to it
'''

    entries = {} # Dictionary with words (strings) as keys and definitions (Definition instances) as values

    @staticmethod
    def add_entry(cls, word: str, definition: Definition):
        if word in Dictionary.entries:
            raise Exception("Word already exists in the dictionary")
        else
            Dictionary.entries[word] = definition

    @staticmethod
    def save_dictionary(cls, file_dir: str):
        data = {}
        data["dictionary"] = []
        sorted_entries = Dictionary.entries[Dictionary.sort(Dictionary.keys())]
        for word,definition in sorted_entries:
            data["dictionary"].append({
                    "word": word,
                    "translation": definition.translation,
                    "components": definition.components,
                    "confidence": definition.confidence,
                    "notes": definition.notes
            })
        with open(file_dir, "w") as save_file:
            json.dump(data, save_file)

    @staticmethod
    def load_dictionary(cls, file_dir: str):
        with open(file_dir, "r") as load_file:
            data = json.load(load_file)
            for entry in data["dictionary"]:
                definition = Definition(entry["translation"], entry["components"], entry["confidence"], entry["notes"])
                Dictionary.entries[entry["word"]] = definition

    @staticmethod
    def sort(cls, words: list[str]=None -> list[str]):
        '''
        Sorts a list of ancient words from right to left ignoring punctuation marks
        words: list of words to sort. If words=None, use the words in the dictionary instead
        return: sorted list of words
        '''
        if not words:
            words = Dictionary.entries.keys()
        return sorted(words, lambda w: Dictionary.__sort_key(w))

    @staticmethod
    def __sort_key(cls, word):
        return reversed(word.strip([" ", "\ue00a", "\ue00b", "\ue00c"]))

    @staticmethod
    def search_words(cls, expression: str -> list[str]):
        '''
        Search for words in the dictionary matching parts of the expression or containing the expression
        return: list of dictionary keys
        '''
        matches = []
        for word in Dictionary.entries.keys():
            if word in expression or expression in word:
                matches.append(word)
        return Dictionary.sort(matches)

    @staticmethod
    def search_translations(cls, expression: str -> list[str]):
        '''
        Search for translations in the dictionary containing the expression 
        return: list of dictionary keys
        '''
        matches = []
        for word, definition in Dictionary.entries:
            if expression in definition.translation:
                matches.append(word)
        return Dictionary.sort(matches)
