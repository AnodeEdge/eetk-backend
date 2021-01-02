class Config(object):
    DEBUG = True
    TESTING = False


class DevelopmentConfig(Config):
    # Development Configuration
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    # Production Configuration
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
