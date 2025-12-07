from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea o actualiza el usuario admin con contraseña admin123"

    def handle(self, *args, **options):
        User = get_user_model()
        username = "admin"
        password = "admin123"
        email = "admin@example.com"
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        if created:
            self.stdout.write(self.style.SUCCESS("Usuario admin creado."))
        else:
            self.stdout.write("Usuario admin ya existía. Actualizando contraseña...")
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("Credenciales -> admin / admin123"))
