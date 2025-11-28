# Generated migration to add Basic plan

from django.db import migrations
from django.apps.registry import apps


class Migration(migrations.Migration):

    dependencies = [
        ("membership", "0008_auto_20201107_1700"),
    ]

    def create_basic_plan(self, schema_editor):
        Plan = apps.get_model("membership", "Plan")
        Plan.objects.create(
            name="Basic",
            description="Basic plan with 5 staff and 5 branches",
            price=5.00,
            duration_days=30,
            max_staff=5,
            max_branch=5,
        )

    operations = [
        migrations.RunPython(create_basic_plan, migrations.RunPython.noop),
    ]
