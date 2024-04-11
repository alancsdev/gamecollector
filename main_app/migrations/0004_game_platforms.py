
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_platform_alter_playing_options_alter_playing_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='platforms',
            field=models.ManyToManyField(to='main_app.platform'),
        ),
    ]
