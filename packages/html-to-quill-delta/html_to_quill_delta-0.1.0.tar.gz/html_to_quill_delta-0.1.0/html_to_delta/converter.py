from bs4 import BeautifulSoup, NavigableString, Tag
import json

class CustomDelta:
    def __init__(self):
        self.ops = []

    def insert(self, text, attributes=None):
        if attributes:
            self.ops.append({'insert': text, 'attributes': attributes})
        else:
            self.ops.append({'insert': text})

    def to_dict(self):
        return {'ops': self.ops}

def parse_element(element, delta):
    try:
        if isinstance(element, NavigableString):
            delta.insert(str(element))
        elif isinstance(element, Tag):
            if element.name == 'p':
                parse_children(element, delta)
                delta.insert('\n', {'block': 'paragraph'})
            elif element.name in ['strong', 'b']:
                parse_children(element, delta, {'bold': True})
            elif element.name == 'em':
                parse_children(element, delta, {'italic': True})
            elif element.name == 'u':
                parse_children(element, delta, {'underline': True})
            elif element.name == 'a':
                href = element.get('href', '')
                parse_children(element, delta, {'link': href})
            elif element.name == 'h1':
                parse_children(element, delta)
                delta.insert('\n', {'header': 1})
            elif element.name == 'h2':
                parse_children(element, delta)
                delta.insert('\n', {'header': 2})
            elif element.name == 'h3':
                parse_children(element, delta)
                delta.insert('\n', {'header': 3})
            elif element.name == 'ol':
                parse_children(element, delta)
                delta.insert('\n', {'list': 'ordered'})
            elif element.name == 'ul':
                parse_children(element, delta)
                delta.insert('\n', {'list': 'bullet'})
            elif element.name == 'li':
                parse_children(element, delta)
                delta.insert('\n', {'list-item': True})
            elif element.name == 'br':
                delta.insert('\n')
            elif element.name == 'img':
                src = element.get('src', '')
                delta.insert({'image': src})
            elif element.name == 'iframe':
                src = element.get('src', '')
                delta.insert({'iframe': src})
            elif element.name == 'table':
                parse_table(element, delta)
            elif element.name == 'blockquote':
                parse_children(element, delta)
                delta.insert('\n', {'blockquote': True})
            elif element.name == 'div':
                parse_children(element, delta)
            elif element.name == 'span':
                parse_children(element, delta)
            elif element.name == 'code':
                parse_children(element, delta)
                delta.insert('\n', {'code': True})
            elif element.name == 'pre':
                parse_children(element, delta)
                delta.insert('\n', {'code-block': True})
            elif element.name == 'sup':
                parse_children(element, delta)
                delta.insert('\n', {'script': 'super'})
            elif element.name == 'sub':
                parse_children(element, delta)
                delta.insert('\n', {'script': 'sub'})
            else:
                parse_children(element, delta)
    except Exception as e:
        print(f"Error parsing element: {e}")

def parse_children(element, delta, attributes=None):
    try:
        for child in element.children:
            parse_element(child, delta if not attributes else CustomDeltaWithAttributes(delta, attributes))
    except Exception as e:
        print(f"Error parsing children: {e}")

def parse_table(table, delta):
    try:
        table_content = []
        for row in table.find_all('tr'):
            row_content = []
            for cell in row.find_all(['td', 'th']):
                cell_text = ''.join(cell.stripped_strings)
                row_content.append(cell_text)
            table_content.append(row_content)
        delta.insert({'table': table_content})
    except Exception as e:
        print(f"Error parsing table: {e}")

class CustomDeltaWithAttributes(CustomDelta):
    def __init__(self, delta, attributes):
        super().__init__()
        self.delta = delta
        self.attributes = attributes

    def insert(self, text, attributes=None):
        try:
            combined_attributes = self.attributes.copy()
            if attributes:
                combined_attributes.update(attributes)
            self.delta.insert(text, combined_attributes)
        except Exception as e:
            print(f"Error inserting text with attributes: {e}")

def html_to_delta(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check if body tag is present, otherwise wrap content in a div
        if not soup.body:
            body = soup.new_tag('body')
            soup.insert(0, body)
            body.append(BeautifulSoup(html, 'html.parser'))
        
        delta = CustomDelta()
        for element in soup.body.children:
            parse_element(element, delta)
        return json.dumps(delta.to_dict(), indent=2)
    except Exception as e:
        print(f"Error converting HTML to Delta: {e}")

# Example usage:
html_content = """
<p style="text-indent: 20px;">This is indented text.</p>
"""

delta_format = html_to_delta(html_content)
print(delta_format)
