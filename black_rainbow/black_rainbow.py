from typing import Dict, Callable

class BlackRainbow:
    def __init__(self):
        self.page_functions: Dict[str, Callable] = {}
        self.current_path = "/"

        self.storage = {"test": 51}

    def register_page(self, path: str):
        def decorator(func):
            self.page_functions[path] = func
        return decorator
    
    def render_page(self, page_function):
        page = page_function(storage=self.storage)
        page.render()

    def run(self):
        for _ in range(10):
            page_function = self.page_functions[self.current_path]
            self.render_page(page_function)
            
class Page:
    def __init__(self, header, caption):
        self.header = header
        self.caption = caption
    
    def render(self):
        print('---', self.header, '---')
        print(self.caption)
        print('----------------')