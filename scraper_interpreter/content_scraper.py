from typing import List
from .functions_list import get_function


class ContentBot:

    def __init__(self):
        # super().__init__(**kwargs)
        self.content = {}
        self.response = None
        self.web_element = None

    def _evaluate_content(self, value, function: dict):
        print('value: ', value)
        print('function: ', function)
        return get_function(function["function"])(value, **function['kwargs'], response=self.response)

    def _evaluate_listing(self, value, function: dict):
        # print('value: ', value)
        # print('function: ', function)

        return get_function(function["function"])(value, **function['kwargs'], response=self.web_element)

    def _evaluate(self, value, function: dict):
        if self.web_element:
            # print('_evaluate 1')
            # print(f'value _evaluate web_element function {function}')
            # print(f'value _evaluate web_element value {value}')
            return self._evaluate_listing(value, function)
        else:
            # print('_evaluate 2')
            # print(f'value _evaluate {value}')
            # print(f'function _evaluate {function}')
            return self._evaluate_content(value, function)

    def evaluate_function(self, value, function: dict):
        if function.get('map', 0):
            return [self._evaluate(sub_value, function) for sub_value in value]
        return self._evaluate(value=value, function=function)

    def evaluate_way(self, functions: [dict]):
        value = None
        if self.web_element:
            try:
                value = self.web_element
                for function in functions:
                    value = self.evaluate_function(value, function)
                return value
            except Exception as e:
                print(f'Error 1 in evaluate_way() in ContentBot: {e}  value: {value}')
                return ''
        else:
            try:
                for function in functions:
                    value = self.evaluate_function(value, function)
                    # if not value:
                    #     value = self.evaluate_function(self.web_element, function)
                return value
            except Exception as e:
                print(f'Error 2 in evaluate_way() in ContentBot: {e} - value: {value}')
                return ''
        # return value

    def evaluate_field(self, ways: List[List[dict]]):
        # print(ways)
        result = None
        n = 1
        for way in ways:
            result = self.evaluate_way(way)
            if result:
                # print(f'Way {n} worked')
                # print(f'Passed {result}')
                return result
            else:
                n = n + 1
                continue
        return result

    # """
    #                         product_data.update(self.get_content(product_link=False,
    #                                                              content_instructions=container_kind['fields'],
    #                                                              web_element=web_element,
    #                                                              fields=fields))
    # """
    def get_content(self, content_instructions, web_element=False, response=False, fields=False):

        self.web_element = web_element
        self.response = response
        self.content = {}

        if fields:
            interesting_fields = fields
        else:
            interesting_fields = content_instructions.keys()
            # print('interesting_fields', interesting_fields)
        for field in interesting_fields:
            field_dict = content_instructions[field]
            try:
                self.content[field_dict['name']] = self.evaluate_field(field_dict['functions'])
            except Exception as e:
                print(f'Error in get_content() in ContentBot: {field_dict["name"]}: {e} - interesting_fields {interesting_fields}')
                self.content[field_dict['name']] = ''
            # print(self.content)
        # to dataframe?
        return self.content

# content = ContentBot()

# content.get_content(product_link='https://www.amazon.es/dp/B07F3TDGQC', content_instructions={})
