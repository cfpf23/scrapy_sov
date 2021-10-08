import json
import re
# import string


"""
metric functions for content Turbo
"""


class ContentMetrics:
    """
    Takes the product data in a form of a dictionary (product_dict) and apply all the methods in turbo
    """
    def __init__(self, product_dict):
        self.product_dict = product_dict

    def calculate_all_metrics(self):
        return {
            "average_length_of_bullet": self.average_length_of_bullet(),
            "bulletpoints_metric": self.bulletpoints_metric(),
            "description_metric": self.description_metric(),
            "images_video_metric": self.images_video_metric(),
            "number_of_bullets": self.number_of_bullets(),
            "plus_content_metric": self.plus_content_metric(),
            "rating_reviews_metric": self.rating_reviews_metric(),
            "title_metric": self.title_metric()
            }

    def average_length_of_bullet(self):
        try:
            number = self.number_of_bullets()
            total_length = " ".join(self.product_dict['bulletpoints'])
            return len(total_length) / number
        except Exception as e:
            print(f"bullets length metric: {e}")
            return "-"

    def bulletpoints_metric(self):
        try:
            if self.number_of_bullets() in [5, 6, 7, 8]:
                return 0.5 + self.average_length_of_bullet() / 200 * 0.5
            else:
                return self.average_length_of_bullet() / 200 * 0.5
        except Exception as e:
            print(f"bullets metric: {e}")
            return "-"

    def description_metric(self):
        try:
            if len(self.product_dict['description']) > 1900:
                return 1
            else:
                return len(self.product_dict['description']) / 1900
        except Exception as e:
            print(f"description metric: {e}")
            return "-"

    def images_video_metric(self):
        try:
            if self.product_dict['video']:
                if self.product_dict['number_of_images'] > 7:
                    return (((7 - (self.product_dict['number_of_images'] - 7)) / 7) * 0.5) + 0.5
                else:
                    return ((self.product_dict['number_of_images'] / 7) * 0.5) + 0.5
            if self.product_dict['number_of_images'] > 7:
                return ((7 - (self.product_dict['number_of_images'] - 7)) / 7) * 0.5
            else:
                return (self.product_dict['number_of_images'] / 7) * 0.5
        except Exception as e:
            print(f"images / video metric: {e}")
            return 0

    def number_of_bullets(self):
        try:
            if len(self.product_dict['bulletpoints_length'].split(','))>1:
                return len([element for element in self.product_dict['bulletpoints_length'].split(',') if element != '0'])
            if len(self.product_dict['bulletpoints_length'].split(';'))>1:
                return len([element for element in self.product_dict['bulletpoints_length'].split(';') if element != '0'])
        except Exception as e:
            print(f"bullets number metric: {e}")
            return "-"

    def plus_content_metric(self):
        if self.product_dict['a_plus']:
            if self.product_dict['a_plus_plus']:
                return 1
            else:
                return 0.75
        else:
            return 0

    def rating_reviews_metric(self):
        try:
            rating_metric = self.product_dict['rating'] / 5 * 0.5
        except Exception as e:
            print(f"r&r metric rating_metric: {e}")
            rating_metric = 0
        try:
            if self.product_dict['reviews'] / 5000 > 1:
                reviews_metric = 0.5
            else:
                reviews_metric = self.product_dict['reviews'] / 5000 * 0.5
        except Exception as e:
            print(f"r&r metric reviews_metric: {e}")
            reviews_metric = 0

        return rating_metric + reviews_metric

    def title_metric(self):
        try:
            return len(self.product_dict['title']) / 200
        except Exception as e:
            print(f"title metric: {e}")
            return "-"


"""
further metric functions
"""


def join(value: list, **kwargs) -> str:
    return kwargs['delimiter'].join(value)


def drop_empty_elements(value: list, **kwargs) -> list:
    return [element for element in value if len(element)]


def get_(value: dict, **kwargs) -> str:
    return value[kwargs['key']]


def join_number(value: list, **kwargs) -> str:
    return kwargs['delimiter'].join([str(number) for number in value])


def remove_duplicates(value: list, **kwargs) -> list:
    return list(dict.fromkeys(value))


def read_json(value: str, **kwargs) -> dict:
    return json.loads(value)


def get_elem(value, **kwargs):
    return value[kwargs['i']]


def clean_float(value: str, **kwargs) -> float:
    matches = re.findall(r'[0-9]+\.[0-9]+', value.replace(',', '.'))
    return float(matches[0])


def clean_int(value: str, **kwargs) -> int:
    return int(re.sub(r"\D", "", value))


def add_prefix(value: str, **kwargs) -> str:
    return kwargs['prefix'] + value


def add_suffix(value: str, **kwargs) -> str:
    return value + kwargs['suffix']


def lower(value: str, **kwargs) -> str:
    return value.lower()


def is_bigger(value: int, **kwargs) -> bool:
    return value > kwargs.get('than', row[kwargs['than_col']])


def get_bestseller_rank(value: list, **kwargs) -> list:
    clean_info = [
        {"market": "DE",
         "word": "bestseller",
         "erase_word": ["Amazon Bestseller-Rang"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "SE",
         "word": "bästsäljare",
         "erase_word": ["Rangordning för bästsäljare"],
         "splitter": " i ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "FR",
         "word": "meilleures",
         "erase_word": ["Classement des meilleures ventes d'Amazon"],
         "splitter": " en ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "ES",
         "word": "más vendidos",
         "erase_word": ["Clasificación en los más vendidos de Amazon"],
         "splitter": " en ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "IT",
         "word": "bestseller",
         "erase_word": ["Posizione nella classifica Bestseller di Amazon"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "UK",
         "word": "best sellers",
         "erase_word": ["Best Sellers Rank"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]}
    ]
    for cleaner in clean_info:
        value_n = []
        for v in value:
            if cleaner['word'].lower() in v.lower():
                value_n.append(v)
            else:
                continue
        if not value_n:
            continue

        if value_n:
            value = [v for v in value if cleaner['word'].lower() in v.lower()]
            for word in cleaner['erase_word']:
                value = ''.join(value).replace(word, '').strip()
            value = re.sub("[\(\[].*?[\)\]]", "", value)
            for n in cleaner['number_cleaner']:
                value = str(value).replace(n, '').strip()
            #             print(value)
            return [key.strip() for key in {element.split(cleaner['splitter'])[0]: element.split(cleaner['splitter'])[1]
                                            for element in ''.join(value).split('\n')}.keys()]
        else:
            return []


def get_bestseller_class(value: list, **kwargs) -> list:
    clean_info = [
        {"market": "DE",
         "word": "bestseller",
         "erase_word": ["Amazon Bestseller-Rang"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "SE",
         "word": "rangordning",
         "erase_word": ["Rangordning för bästsäljare"],
         "splitter": " i ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "FR",
         "word": "meilleures",
         "erase_word": ["Classement des meilleures ventes d'Amazon"],
         "splitter": " en ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "ES",
         "word": "más vendidos",
         "erase_word": ["Clasificación en los más vendidos de Amazon"],
         "splitter": " en ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "IT",
         "word": "bestseller",
         "erase_word": ["Posizione nella classifica Bestseller di Amazon"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]},
        {"market": "UK",
         "word": "best sellers",
         "erase_word": ["Best Sellers Rank"],
         "splitter": " in ",
         "number_cleaner": ["n.", "Nr.", "#", "nº"]}
    ]
    for cleaner in clean_info:
        value_n = []
        for v in value:
            if cleaner['word'].lower() in v.lower():
                value_n.append(v)
            else:
                continue
        if not value_n:
            continue
        # value_n = [v for v in value if cleaner['word'].lower() in v.lower()]
        if value_n:
            value = [v for v in value if cleaner['word'].lower() in v.lower()]
            for word in cleaner['erase_word']:
                value = ''.join(value).replace(word, '').strip()
            value = re.sub("[\(\[].*?[\)\]]", "", value)
            for n in cleaner['number_cleaner']:
                value = str(value).replace(n, '').strip()
            #             print(value)
            return [v.strip() for v in {element.split(cleaner['splitter'])[0]: element.split(cleaner['splitter'])[1]
                                        for element in ''.join(value).split('\n')}.values()]
        else:
            return []


def remove_word(value: str, **kwargs) -> str:
    value = str(value).replace(kwargs["word"], '')
    return value


def len_(value, **kwargs) -> int:
    return len(value)


def eliminate_currency(value: str, **kwargs) -> str:
    curr = ['£', '€', 'kr', 'zł']
    for c in curr:
        value = value.replace(c, '').replace(',', '.')
    return value


def bulletpoints_length(value, **kwargs) -> list:
    bullet_lengths = [str(len(line)) for line in value]
    bullet_7 = bullet_lengths + ['0' for _ in range(7 - len(bullet_lengths))]
    return bullet_7


def bool_(value, **kwargs) -> bool:
    return bool(value)


def strip(value, **kwargs) -> str:
    return value.strip()


def extract_stuff_between(value, **kwargs) -> list:
    return re.findall(rf"{kwargs['separator']}(.*?){kwargs['separator']}", value, re.DOTALL)


def extract_stuff_between_diffs(value, **kwargs) -> list:
    return re.findall(f"{kwargs['separator1']}(.*?){kwargs['separator2']}", value, re.DOTALL)[0]


def functions():
    return {"join": join,
            "drop_empty_elements": drop_empty_elements,
            "get_": get_,
            "join_number": join_number,
            "remove_duplicates": remove_duplicates,
            "read_json": read_json,
            "get_elem": get_elem,
            "clean_float": clean_float,
            "clean_int": clean_int,
            "add_prefix": add_prefix,
            "add_suffix": add_suffix,
            "is_bigger": is_bigger,
            "len": len_,
            "bool": bool_,
            "lower": lower,
            "strip": strip,
            "remove_word": remove_word,
            "eliminate_currency": eliminate_currency,
            "bulletpoints_length": bulletpoints_length,
            "get_bestseller_rank": get_bestseller_rank,
            "get_bestseller_class": get_bestseller_class,
            "extract_stuff_between": extract_stuff_between,
            "extract_stuff_between_diffs": extract_stuff_between_diffs}
