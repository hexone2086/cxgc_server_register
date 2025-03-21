import toml
import os

# 加载 TOML 配置文件
config_path = os.path.join(os.path.dirname(__file__), 'config.toml')
config_data = toml.load(config_path)

class Config:
    SECRET_KEY = config_data['default']['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = config_data['default']['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = config_data['default']['SQLALCHEMY_TRACK_MODIFICATIONS']

    MAIL_SERVER = config_data['default']['MAIL_SERVER']
    MAIL_PORT = config_data['default']['MAIL_PORT']
    MAIL_USE_TLS = config_data['default']['MAIL_USE_TLS']
    MAIL_USERNAME = config_data['default']['MAIL_USERNAME']
    MAIL_PASSWORD = config_data['default']['MAIL_PASSWORD']
    
    # admin 配置
    ADMIN_USERNAME = config_data['admin']['username']
    ADMIN_PASSWORD = config_data['admin']['password']
    
    # CAPTCHA 配置
    CAPTCHA_LENGTH = config_data['captcha']['length']
    CAPTCHA_DIGITS = config_data['captcha']['digits']
    CAPTCHA_EXPIRE = config_data['captcha']['expire']
    SECRET_CAPTCHA_KEY = config_data['captcha']['secret_key']
    EXCLUDE_VISUALLY_SIMILAR = config_data['captcha']['exclude_visually_similar']
    BACKGROUND_COLOR = tuple(config_data['captcha']['background_color'])
    CAPTCHA_LOG = config_data['captcha']['log']