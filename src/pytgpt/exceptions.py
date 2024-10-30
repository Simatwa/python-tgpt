class FailedToGenerateResponseError(Exception):
    """Provider failed to fetch response"""


class UnsupportedModelError(Exception):
    """Model passed is not supported by the provider"""
