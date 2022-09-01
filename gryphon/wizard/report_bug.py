from .wizard_text import Text


def report_bug(_, __):
    import webbrowser
    import urllib.parse

    recipient = 'vittor@blueorange.digital'
    subject = 'Bug report'

    url_data = urllib.parse.urlencode(
        dict(
            to=recipient,
            subject=subject,
            body=Text.bug_report_email_template
        )
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)
