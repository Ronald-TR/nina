from core.helpers import coverage_parser, remove_special_characters

TEMPLATE  = """
# {project_name}

{badges}


## 
"""

def create_badges(fields):
    BASE = 'https://img.shields.io/badge/'

    version = ''.join([
            '![version]',
            '(',
            BASE,
            remove_special_characters(fields['project_name']),
            '-' + fields['project_version'],
            '-brightgreen.svg',
            ')'
        ])
    
    color_cov = 'green'
    cov = coverage_parser(fields)
    if cov['percent'] <= 30:
        color_cov = 'yellow'
    elif cov['percent'] <= 70:
        color_cov = 'green'
    elif cov['percent'] <= 90:
        color_cov = 'brightgreen'

    coverage = ''.join([
        '![coverage]',
        '(',
        BASE,
        'coverage',
        '-' + str(cov['percent']) + '%',
        '-' + color_cov + '.svg',
        ')'
    ])

    return [
        version,
        coverage
    ]

def build_readme(fields):
    badges = '\n'.join(create_badges(fields))

    template = TEMPLATE.format(**{
        'project_name': fields['project_name'],
        'badges': badges})

    return template

    