from .wizard_text import Text


def feedback(_, __):
    import webbrowser
    import urllib.parse

    recipient = 'vittor@blueorange.digital'
    subject = 'Feedback'

    url_data = urllib.parse.urlencode(
        dict(
            to=recipient,
            subject=subject,
            body=Text.feedback_email_template
        )
    )

    webbrowser.open(f"mailto:?{url_data}", new=0)
