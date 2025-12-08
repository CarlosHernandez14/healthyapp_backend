from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("citas", "0002_cita_enfoque_terapeutico_cita_objetivo_terapeutico_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="cita",
            old_name="objetivo_terapeutico",
            new_name="objetivo_nutricional",
        ),
        migrations.RenameField(
            model_name="cita",
            old_name="enfoque_terapeutico",
            new_name="enfoque_nutricional",
        ),
        migrations.RenameField(
            model_name="cita",
            old_name="plan_intervencion",
            new_name="plan_alimentacion",
        ),
        migrations.RenameField(
            model_name="cita",
            old_name="tareas_iniciales",
            new_name="recomendaciones",
        ),
    ]
