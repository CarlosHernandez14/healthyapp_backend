from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("registros", "0002_add_nutrition_fields"),
        ("citas", "0003_rename_psico_to_nutricion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registrodiario",
            name="cita",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="registros",
                to="citas.cita",
            ),
        ),
    ]
