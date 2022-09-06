from .core_text import Text
from ..constants import EMAIL_RECIPIENT


def report_bug():
    import webbrowser
    import urllib.parse

    subject = 'Bug report'

    url_data = urllib.parse.urlencode(
        dict(
            to=EMAIL_RECIPIENT,
            subject=subject,
            body=Text.bug_report_email_template.replace("{traceback}", "")
        )
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)
