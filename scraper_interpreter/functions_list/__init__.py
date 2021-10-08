import scraper_interpreter.functions_list.scraping
import scraper_interpreter.functions_list.on_enter
import scraper_interpreter.functions_list.transform
import scraper_interpreter.functions_list.metric
import scraper_interpreter.functions_list.save

# # from selenium.webdriver import Chrome
# from scrapy.responsetypes import Response
# # from selenium.common.exceptions import NoSuchElementException
#
# from typing import List
# from inspect import signature
# from PIL.Image import Image


def get_function(name: str):
    # functions.update(functions_list.scraping.functions())
    functions = {}
    functions.update(scraping.functions())
    functions.update(on_enter.functions())
    functions.update(transform.functions())
    functions.update(metric.functions())
    functions.update(save.functions())
    return functions[name]


# def missing_field(name: str):
#     return {
#       "name": f"Missing field: {name}",
#       "functions": [],
#       "tags": []
#     }
#
#
# def _evaluate(value, row, function: dict, driver):
#     return get_function(function["function"])(value, row, **function['kwargs'], driver=driver)
#
#
# def evaluate_function(value, row, function: dict, driver):
#     if function.get('map', 0):
#         return [_evaluate(sub_value, row, function, driver) for sub_value in value]
#     return _evaluate(value, row, function, driver)
#
#
# def evaluate_way(driver, row, functions: [dict]):
#     value = None
#     try:
#         for function in functions:
#             value = evaluate_function(value, row, function, driver)
#     except NoSuchElementException:
#         pass
#     return value
#
#
# def evaluate_field(row: dict, driver: Response, ways: List[List[dict]]):
#     result = None
#     for way in ways:
#         result = evaluate_way(driver, row, way)
#         if result is not None:
#             return result
#     return result
#
#
# def scrap(row: dict, response, url_column: str, eretailer: dict, fields: list, **kwargs) -> list:
#     # get_url(row, driver, url_column)
#
#     evaluate_field(row, response, eretailer.get('on_starts', []))
#
#     available_fields = eretailer.get('product_card', dict())
#     fields = [available_fields.get(field, missing_field(field)) for field in fields]
#
#     results = {}
#     for field in fields:
#         results[field['name']] = evaluate_field(row, response, field["functions"])
#
#     return [results.get(field['name']) for field in fields]
#
#
# def preview_scrap(row: dict, url_column: str, eretailer: dict, fields: list, **kwargs) -> list:
#     assert url_column in row.keys()
#     available_fields = eretailer.get('product_card', dict())
#     fields = [available_fields.get(field, missing_field(field)) for field in fields]
#     results = {}
#     for field in fields:
#         results[field['name']] = preview_field(field["functions"])
#     return [results.get(field['name']) for field in fields]
#
#
# def preview_field(ways: List[List[dict]]):
#     if ways:
#         return preview_way(ways[0])
#
#
# def preview_way(functions: [dict]):
#     return preview_value(signature(get_function(functions[-1]['function'])).return_annotation)
#
#
# def preview_value(t: type):
#     if t is int:
#         return 123
#     if t is float:
#         return 1.23
#     if t is str:
#         return 'abc'
#     if t is list:
#         return [123, 1.23, 'abc']
#     if t is Image.Image:
#         return '<picture>'
#     if isinstance(t, list):
#         return [preview_value(elem) for elem in t]
#     if isinstance(t, tuple):
#         return (preview_value(elem) for elem in t)
#     if not isinstance(t, type):
#         return t
#     return '...'
#
#
# def map_by_clicking_elements(value: str, row: dict, **kwargs) -> list:
#     results = []
#     driver = kwargs['driver']
#     f = kwargs['map_functions']  # This is a list of functions!
#     clickable_elements = get_function('find_elements_by_css')(None, row, css=kwargs['css'], driver=driver)
#     for element in clickable_elements:
#         get_function('click')(element, row, driver=driver)
#         results.append(evaluate_way(driver=driver, row=row, functions=f))
#     return results
#
#
# def map_by_clicking_element(value: str, row: dict, **kwargs) -> list:
#     results = []
#     driver = kwargs['driver']
#     f = kwargs['map_functions']  # This is a list of functions!
#     clickable_element = get_function('find_element_by_css')(None, row, css=kwargs['css'], driver=driver)
#     while True:
#         try:
#             get_function('click')(clickable_element, row, driver=driver)
#             results.append(evaluate_way(driver=driver, row=row, functions=f))
#         except:
#             break
#     return results
