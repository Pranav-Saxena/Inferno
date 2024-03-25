class CodeRunError(Exception):
    """The base exception type for all CodeRunner related errors."""
    pass

class CodeRunNoOutput(CodeRunError):
    """Exception raised when no output was received from the API"""
    pass

class CodeRunInvalidStatus(CodeRunError):
    """Exception raised when the API request returns a non 200 status"""
    pass

class CodeRunInvalidContentType(CodeRunError):
    """Exception raised when the API request returns a non JSON content type"""
    pass