# Enable Flask Application debugging features.


class Config(object):
    """
    Common configurations
    """
    # Configurations that are common to all environment
    DEBUG = False


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True


class TestingConfig(Config):
    """Testing configurations"""
    TESTING = True


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
