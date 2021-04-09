from typing import List, Dict
import json

class Definition:
    '''
    Class encapsulating the different parts of a word's definition.
    '''
    def __init__(self, translation: str, components: List[str], confidence: int, notes: str):
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
    Static class containing a dictionary of all words and usefull functions related to it.
    '''
    entries = {} # Dictionary with words (strings) as keys and definitions (Definition instances) as values

    @staticmethod
    def add_entry(cls, word: str, definition: Definition):
        '''

        '''
        if word in Dictionary.entries:
            raise Exception("Word already exists in the dictionary")
        else:
            Dictionary.entries[word] = definition

    @staticmethod
    def save_dictionary(cls, file_dir: str):
        '''
        Saves current dictionary to json file.
        file_dir: directory of save file
        '''
        data = {}
        data["dictionary"] = []
        sorted_entries = Dictionary.entries[Dictionary.sort(Dictionary.keys())]
        for word,definition in sorted_entries.items():
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
        '''
        Loads dictionary from json file.
        file_dir: directory of save file
        '''
        with open(file_dir, "r") as load_file:
            data = json.load(load_file)
            for entry in data["dictionary"]:
                definition = Definition(entry["translation"], entry["components"], entry["confidence"], entry["notes"])
                Dictionary.entries[entry["word"]] = definition

    @staticmethod
    def sort(cls, words: List[str]=None) -> List[str]:
        '''
        Sorts a list of ancient words from right to left ignoring punctuation marks.
        words: list of words to sort. If words=None, use the words in the dictionary instead
        return: sorted list of words
        '''
        if not words:
            words = Dictionary.entries.keys()
        return sorted(words, lambda w: Dictionary._sort_key(w))

    @staticmethod
    def _sort_key(cls, word: str) -> str:
        '''
        Key function for sorting ancient words. Removes punctuation characters and inverts the string so that words will be sorted from right to left.
        word: ancient word to be sorted
        return: sorting key for the ancient word
        '''
        return reversed(word.strip([" ", "\ue00a", "\ue00b", "\ue00c"]))

    @staticmethod
    def search_words(cls, expression: str) -> List[str]:
        '''
        Search for words in the dictionary matching parts of the expression or containing the expression.
        expression: string to match
        return: list of dictionary keys matching the expression
        '''
        matches = []
        for word in Dictionary.entries.keys():
            if word in expression or expression in word:
                matches.append(word)
        return Dictionary.sort(matches)

    @staticmethod
    def search_translations(cls, expression: str) -> List[str]:
        '''
        Search for translations in the dictionary containing the expression.
        expression: string to match
        return: list of dictionary keys matching the expression
        '''
        matches = []
        for word, definition in Dictionary.entries.items():
            if expression in definition.translation:
                matches.append(word)
        return Dictionary.sort(matches)
