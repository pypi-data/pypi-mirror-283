# __init__.py

import re
from flask import request


class SanitizeEscapeExtension:
    def sanitize_string(self, value):
        # Remove all tags and attributes:
        value = re.sub(r'<[^>]+>', '', value, flags=re.IGNORECASE)
        # Remove event handlers and JavaScript links:
        value = re.sub(r'on\w+=\S+', '', value, flags=re.IGNORECASE)
        value = re.sub(r'javascript:\S+', '', value, flags=re.IGNORECASE)
        # Encode HTML entities, except for & (ampersand):
        value = value.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
        return value

    def sanitize_int(self, value):
        # Allow only numbers, a potential minus sign, and a decimal point:
        return re.sub(r'[^\d.-]', '', str(value))

    class Middleware:
        def __init__(self, app):
            self.app = app
            self.extension = SanitizeEscapeExtension()  # Create an instance of the extension

        def __call__(self, environ, start_response):
            # Get query parameters (URL arguments)
            query_params = request.args
            for key in query_params:
                query_params[key] = self.extension.sanitize_string(query_params[key])

            # Get form data
            form_data = request.form
            for key in form_data:
                form_data[key] = self.extension.sanitize_string(form_data[key])

            # Sanitize JSON data
            if request.is_json:
                json_data = request.get_json()
                for key, value in json_data.items():
                    if isinstance(value, str):
                        json_data[key] = self.extension.sanitize_string(value)
                    elif isinstance(value, int):
                        json_data[key] = self.extension.sanitize_int(value)
                # Update the request JSON
                request.json = json_data

            return self.app(environ, start_response)
