from django.db.models import F, Case, When, Value
from django.db.models.fields import CharField
from your_app.models import Model1, Model2

def update_fields_with_conversion():
    grade_mapping = {
        1.0: 'A',
        2.0: 'B',
        3.0: 'C',
        4.0: 'D',
        5.0: 'E',
    }

    field_mapping_model1 = {
        'security_review_rating': grade_mapping,
        'field2': grade_mapping,
        # Add more fields for Model1 here
    }

    field_mapping_model2 = {
        'field3': grade_mapping,
        'field4': grade_mapping,
        # Add more fields for Model2 here
    }

    # Update fields for Model1
    for field_name, grade_mapping in field_mapping_model1.items():
        cases = []

        for value, grade in grade_mapping.items():
            cases.append(When(**{
                field_name + '__exact': value,
                'then': Value(grade, output_field=CharField()),
            }))

        Model1.objects.update(
            **{field_name: Case(*cases, default=F(field_name), output_field=CharField())}
        )

    # Update fields for Model2
    for field_name, grade_mapping in field_mapping_model2.items():
        cases = []

        for value, grade in grade_mapping.items():
            cases.append(When(**{
                field_name + '__exact': value,
                'then': Value(grade, output_field=CharField()),
            }))

        Model2.objects.update(
            **{field_name: Case(*cases, default=F(field_name), output_field=CharField())}
        )
