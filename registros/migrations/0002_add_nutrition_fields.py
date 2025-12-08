from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registros", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="registrodiario",
            name="calorias",
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="registrodiario",
            name="agua_ml",
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="registrodiario",
            name="actividad_min",
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name="registrodiario",
            name="peso_kg",
            field=models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True),
        ),
        migrations.AddField(
            model_name="registrodiario",
            name="adherencia",
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
