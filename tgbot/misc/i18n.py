from tgbot.config import I18N_DOMAIN, LOCALES_DIR
from tgbot.middlewares.language_middleware import ACLMiddleware


i18ns = ACLMiddleware(domain=I18N_DOMAIN, path=LOCALES_DIR, default="uz")
