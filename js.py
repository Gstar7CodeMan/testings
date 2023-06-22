from django.db.models import F, Case, When
from your_app.models import gdata

def update_fields_with_conversion():
    grade_mapping = {
        1.0: 'A',
        2.0: 'B',
        3.0: 'C',
        4.0: 'D',
        5.0: 'E',
    }

    field_mapping = {
        'security_review_rating': grade_mapping,
        'field2': grade_mapping,
        # Add more fields here with the same grade mapping
    }

    for field_name, grade_mapping in field_mapping.items():
        cases = []

        for value, grade in grade_mapping.items():
            cases.append(When(**{
                field_name: value,
                'then': grade,
            }))

        gdata.objects.update(
            **{field_name: Case(*cases, default=F(field_name))}
        )
