from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_landingcontent_character_created_by_world_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='studio_meta',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AddField(
            model_name='world',
            name='studio_meta',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
