
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_playing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
              
            ],
        ),
        migrations.AlterModelOptions(
            name='playing',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='playing',
            name='date',
            field=models.DateField(verbose_name='Playing Date'),
        ),
    ]
