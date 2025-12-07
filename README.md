# HealtyApp - Proyecto base Django (DRF + JWT + CORS)

Proyecto base para desarrollo de aplicaciones móviles de salud: médicos, nutriólogos, psicólogos y entrenadores.

## Endpoints
- `POST /auth/login/` -> devuelve tokens JWT (`access`, `refresh`).

## Requisitos previos
- Python 3.12.x
- pip actualizado

## Pasos rápidos (Windows)
```bash
# 1) Crear y activar entorno virtual (opcional)
python -m venv venv
venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Migraciones
python manage.py migrate

# 4) Crear usuario admin (admin/admin123)
python manage.py init_admin

# 5) Ejecutar servidor
python manage.py runserver
```

## Prueba de login
POST a `http://127.0.0.1:8000/auth/login/`
```json
{
  "username": "admin",
  "password": "admin123"
}
```

## Notas
- CORS abierto para desarrollo.
- Base de datos: SQLite (`db.sqlite3`).
