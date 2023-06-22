from django.db.models import F, Case, When
from your_app.models import gdata

def update_fields_with_conversion():
    field_mapping = {
        'security_review_rating': {
            'grade_range': [(1.0, 2.0, 'A'), (2.0, 3.0, 'B'), (3.0, 4.0, 'C'), (4.0, 5.0, 'D'), (5.0, 6.0, 'E')],
        },
        'field2': {
            'grade_range': [(0.0, 1.0, 'X'), (1.0, 2.0, 'Y'), (2.0, 3.0, 'Z')],
        },
        # Add more fields and their grade ranges here
    }

    for field_name, field_info in field_mapping.items():
        grade_ranges = field_info['grade_range']
        cases = []

        for min_value, max_value, grade in grade_ranges:
            cases.append(When(**{
                field_name + '__gte': min_value,
                field_name + '__lt': max_value,
                'then': grade,
            }))

        gdata.objects.update(
            **{field_name: Case(*cases, default=F(field_name))}
        )
