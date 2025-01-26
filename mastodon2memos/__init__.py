import os
import locale
import gettext

#################
### CONSTANTS ###
#################
"""
Tag used to identify memos created by this script.
"""
MASTODON2MEMOS_TAG = 'mastodon2memos'

##########################
### TRANSLATION SETUP ###
##########################

# Infer the current LOCALE
current_locale, encoding = locale.getdefaultlocale()

# Uncomment the following lines to test different locales
#current_locale, encoding = "fr_FR", "UTF-8"
#current_locale, encoding = "en_US", "UTF-8"
#current_locale, encoding = "cs_CZ", "UTF-8"
#current_locale, encoding = "de_DE", "UTF-8"
#current_locale, encoding = "es_ES", "UTF-8"
#current_locale, encoding = "it_IT", "UTF-8"
#current_locale, encoding = "nl_NL", "UTF-8"
#current_locale, encoding = "pl_PL", "UTF-8"
#current_locale, encoding = "pt_PT", "UTF-8"
#current_locale, encoding = "ru_RU", "UTF-8"
#current_locale, encoding = "zh_CN", "UTF-8"
#current_locale, encoding = "zh_TW", "UTF-8"
#current_locale, encoding = "ja_JP", "UTF-8"
#current_locale, encoding = "ko_KR", "UTF-8"

# print(f"Current locale: {current_locale}, Encoding: {encoding}")

# Extract the language code (e.g., 'fr' from 'fr_FR')
language_code = current_locale.split('_')[0] if current_locale else None
# print(f"Language code: {language_code}")

# Set up the locale directory
locale_dir = os.path.join(os.path.dirname(__file__), '../', 'locale')
# print(f"Locale directory: {locale_dir}")

# Attempt to set up the translation using the full locale first (e.g., 'fr_FR')
try:
    lang = gettext.translation('messages', localedir=locale_dir, languages=[current_locale])
    # Install the language
    lang.install()
    # Alias the gettext function
    _ = lang.gettext
    # print(_("Translation setup complete with full locale."))

except FileNotFoundError:
    # print(f"Translation file not found for locale: {current_locale}")
    
    # Attempt to set up the translation using the language code (e.g., 'fr')
    try:
        lang = gettext.translation('messages', localedir=locale_dir, languages=[language_code])
        # Install the language
        lang.install()
        # Alias the gettext function
        _ = lang.gettext
        # print(_("Translation setup complete with language code."))

    except FileNotFoundError:
        # print(f"Translation file not found for language: {language_code}")
        
        # Fallback to default gettext, if no translation is available (i.e., English)
        gettext.install('messages', localedir=locale_dir)
        _ = gettext.gettext
