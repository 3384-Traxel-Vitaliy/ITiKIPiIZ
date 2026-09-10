class SyntaxError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

        super().__init__(
            f"{message}. "
            f"Токен: '{token.value}', "
            f"позиция: {token.position}"
        )

    def __str__(self):
        return (
            f"{self.message}\n"
            f"Токен: '{self.token.value}'\n"
            f"Позиция: {self.token.position}"
        )