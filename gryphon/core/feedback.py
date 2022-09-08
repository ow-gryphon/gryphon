from .core_text import Text
from ..constants import EMAIL_RECIPIENT


def feedback():
    import webbrowser
    import urllib.parse

    subject = 'Feedback'

    url_data = urllib.parse.urlencode(
        dict(
            to=EMAIL_RECIPIENT,
            subject=subject,
            body=Text.feedback_email_template
        ),
        quote_via=urllib.parse.quote
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)

