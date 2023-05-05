from .core_text import Text
from ..constants import EMAIL_RECIPIENT, EMAIL_RECIPIENT_CC

import logging
logger = logging.getLogger('gryphon')


def report_bug():
    import webbrowser
    import urllib.parse

    subject = 'Bug report'

    url_data = urllib.parse.urlencode(
        dict(
            to=EMAIL_RECIPIENT,
            cc=EMAIL_RECIPIENT_CC,
            subject=subject,
            body=Text.bug_report_email_template.replace("{traceback}", "")
        ),
        quote_via=urllib.parse.quote
    )
    
    webbrowser.open(f"mailto:?{url_data}".replace("+","%20"), new=0)
