TOO_SHORT = "VALIDATION_FAILED_TOO_SHORT"
OUT_OF_RANGE = "VALIDATION_FAILED_OUT_OF_RANGE"
TYPE_NOT_COLOR = "VALIDATION_FAILED_NOT_HEX"

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_SUPPORTED_SUBMIT_METHODS = []


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
