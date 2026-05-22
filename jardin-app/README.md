# 🌿 Jardín DB

Base de datos de plantas con Flask + SQLite, lista para desplegar en Railway.

## Estructura del proyecto

```
jardin-app/
├── app.py            ← Servidor Flask (API + frontend)
├── init_db.py        ← Script que crea e inicializa la BD
├── jardin.db         ← Base de datos SQLite (55 plantas, 10 usuarios)
├── requirements.txt  ← Dependencias Python
├── Procfile          ← Comando de arranque para Railway
├── .gitignore        ← Archivos a ignorar en Git
└── static/
    └── index.html    ← Aplicación web completa
```

## Cómo subir a Railway (paso a paso)

### 1. Instalar Git (si no lo tienes)
Descárgalo en https://git-scm.com y sigue el instalador.

### 2. Crear cuenta en Railway
Ve a https://railway.app y regístrate con tu cuenta de GitHub.

### 3. Preparar el proyecto con Git
Abre una terminal en la carpeta `jardin-app` y ejecuta:

```bash
git init
git add .
git commit -m "primer commit"
```

### 4. Subir a GitHub
- Ve a https://github.com/new y crea un repositorio vacío llamado `jardin-app`
- Copia los comandos que GitHub te muestra (push existing repository) y ejecútalos:

```bash
git remote add origin https://github.com/TU_USUARIO/jardin-app.git
git branch -M main
git push -u origin main
```

### 5. Crear proyecto en Railway
1. Entra a https://railway.app/dashboard
2. Clic en **New Project**
3. Elige **Deploy from GitHub repo**
4. Selecciona `jardin-app`
5. Railway detecta el `Procfile` automáticamente y comienza el despliegue

### 6. Obtener tu URL pública
1. En tu proyecto Railway, ve a **Settings → Domains**
2. Clic en **Generate Domain**
3. ¡Listo! Tendrás una URL tipo `jardin-app.up.railway.app`

## API endpoints disponibles

| Endpoint | Descripción |
|---|---|
| `GET /` | Aplicación web |
| `GET /api/plantas` | Lista todas las plantas |
| `GET /api/plantas/:id` | Detalle de una planta |
| `GET /api/usuarios` | Usuarios con sus plantas |
| `GET /api/stats` | Estadísticas generales |

## Desarrollo local

```bash
pip install flask gunicorn
python app.py
# Abre http://localhost:5000
```
