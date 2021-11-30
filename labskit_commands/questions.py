
add = [
    dict(
        type='input',
        name='library_name',
        message='Type the python library you want to install:'
    )
]


def main_questions(options):
    return [
            dict(
                type='list',
                name='command',
                message='Choose witch action to perform',
                choices=options
            )
        ]


def generate_1(metadata):
    return [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:',
            choices=metadata.keys()
        )
    ]


def generate_2(metadata):
    return [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in metadata.get("arguments", [])
    ]


def init_1(options):
    return [
        dict(
            type='list',
            name='template',
            message='Choose the desired template:',
            choices=options
        ),
        dict(
            type='input',
            name='location',
            message='Path to render the template (absolute or relative to the current folder):',
        )
    ]


def init_2(arguments):
    return [
        dict(
            type='input',
            name=field['name'],
            message=field['help']
        )
        for field in arguments
    ]
