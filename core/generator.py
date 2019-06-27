from core.helpers import coverage_parser, remove_special_characters

TEMPLATE  = """
# {project_name}

{badges}

## :house: [Homepage]({project_homepage})
{project_description}


## Installation

    {install_command}
"""


def create_badge(md_tag, name, value, color):
    BASE = 'https://img.shields.io/badge/'
    return f'![{md_tag}]({BASE}{name}-{value}-{color}.svg)'


def create_badges(fields):
    def version():
        return create_badge('version',
            remove_special_characters(fields['project_name']),
            fields['project_version'],
            'brightgreen'
            )


    def coverage():
        if not fields.get('cov_output'):
            return ''
        
        color_cov = 'green'
        cov = coverage_parser(fields)
        if cov['percent'] <= 30:
            color_cov = 'yellow'
        elif cov['percent'] <= 70:
            color_cov = 'green'
        elif cov['percent'] <= 90:
            color_cov = 'brightgreen'

        return create_badge(
            'coverage',
            'coverage',
            str(cov['percent']) + '%',
            color_cov
        )
        
    def test_passing():
        tests = fields.get('test_passing')
        if tests == '':
            return ''
        
        res = 'passing' if tests else 'failing'
        color = 'green' if tests else 'red'
        return create_badge('tests', 'tests', res, color)

    return [
        version(),
        coverage(),
        test_passing()
    ]

def build_readme(fields):
    badges = ' '.join(create_badges(fields))

    template = TEMPLATE.format(**{
        'project_name': fields['project_name'],
        'badges': badges,
        'project_homepage': fields['project_homepage'],
        'project_description': fields['project_description'],
        'install_command': fields['install_command']
    })

    return template

    