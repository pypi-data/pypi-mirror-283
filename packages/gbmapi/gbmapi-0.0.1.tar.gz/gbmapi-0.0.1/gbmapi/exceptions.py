class ResponseError(Exception):
    """
    Request Response Error
    """

    def __init__(self, response):
        self.response = response
        super().__init__(response)
