

def find_elements_by_xpath(value, **kwargs):
    return kwargs.get('response').xpath(kwargs['xpath'])


def find_elements_by_css(value, **kwargs):
    return kwargs.get('response').css(kwargs['css'])


def find_elements_by_css_interval(value, **kwargs):
    return kwargs.get('response').css(kwargs['css'])[int(kwargs['start']):int(kwargs['end'])]


def find_element_by_css(value, **kwargs):
    return kwargs.get('response').css(kwargs['css']).get()


def find_element_by_xpath(value, **kwargs):
    return kwargs.get('response').xpath(kwargs['xpath']).get()


def get_element_number(value, **kwargs):
    return value[kwargs['element_number']]


def get_scrapy(value, **kwargs):
    return value.get()


def getall_(value, **kwargs):
    return value.getall()


def get_attribute(value, **kwargs):
    # print('ATTRIBUTE', value.get_attribute(kwargs['attribute']))
    return value.attrib[kwargs['attribute']]


def get_attribute_origin(value, **kwargs):
    # print('ATTRIBUTE', value.get_attribute(kwargs['attribute']))
    return kwargs.get('response').attrib[kwargs['attribute']]


def functions():
    return {"find_element_by_css": find_element_by_css,
            "find_elements_by_css_interval": find_elements_by_css_interval,
            "find_element_by_xpath": find_element_by_xpath,
            "find_elements_by_css": find_elements_by_css,
            "find_elements_by_xpath": find_elements_by_xpath,
            "get_scrapy": get_scrapy,
            "getall": getall_,
            "get_attribute": get_attribute,
            "get_attribute_origin": get_attribute_origin}
