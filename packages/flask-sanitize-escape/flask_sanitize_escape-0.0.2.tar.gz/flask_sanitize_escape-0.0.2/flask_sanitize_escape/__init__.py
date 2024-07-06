# flask_sanitize_escape/__init__.py

import re
from flask import g, request, jsonify


class SanitizeEscapeExtension:
    def __init__(self, app=None, sanitize_quotes=True, custom_characters=None):
        self.sanitize_quotes = sanitize_quotes
        self.custom_characters = custom_characters or []
        if app is not None:
            self.init_app(app)

    def sanitize_string(self, value):
        # Remove all tags and attributes:
        value = re.sub(r"<[^>]+>", "", value, flags=re.IGNORECASE)

        if self.sanitize_quotes:
            # Escape quotes:
            value = value.replace("'", "''").replace('"', '""')

        # Escape custom characters
        for char in self.custom_characters:
            value = value.replace(char, "\\" + char)

        # Remove suspicious keywords and patterns (RCE):
        value = re.sub(
            r"exec|eval|system|import|open|os\.", "", value, flags=re.IGNORECASE
        )

        return value

    def sanitize_int(self, value):
        # Allow only digits and an optional leading minus sign
        value = re.sub(r"[^\d-]", "", value)

        # Prevent very large integers
        try:
            value = int(value)
            if abs(value) > 2147483647:
                raise ValueError("Integer value too large")
        except ValueError:
            value = 0

        return value

    def init_app(self, app):
        @app.before_request
        def _sanitize_request_data():
            # Sanitize query parameters
            sanitized_args = {}
            for key, values in request.args.lists():
                sanitized_values = [self.sanitize_string(value) for value in values]
                sanitized_args[key] = (
                    sanitized_values[0]
                    if len(sanitized_values) == 1
                    else sanitized_values
                )
            g.sanitized_args = sanitized_args

            # Sanitize form data
            sanitized_form = {}
            for key, values in request.form.lists():
                sanitized_values = [self.sanitize_string(value) for value in values]
                sanitized_form[key] = (
                    sanitized_values[0]
                    if len(sanitized_values) == 1
                    else sanitized_values
                )
            g.sanitized_form = sanitized_form

            # Sanitize JSON data
            if request.is_json:
                json_data = request.get_json()
                sanitized_json = {}
                for key, value in json_data.items():
                    if isinstance(value, str):
                        sanitized_json[key] = self.sanitize_string(value)
                    elif isinstance(value, int):
                        sanitized_json[key] = self.sanitize_int(value)

                g.sanitized_json = sanitized_json

        @app.after_request
        def _restore_json(response):
            if getattr(g, "sanitized_json", None):
                # Restore the original JSON data before sending the response
                response.data = jsonify(g.sanitized_json).data
                response.content_type = "application/json"
            return response
