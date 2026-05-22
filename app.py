from flask import Flask, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder="static")

DB_PATH = os.path.join(os.path.dirname(__file__), "jardin.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db_if_needed():
    if not os.path.exists(DB_PATH):
        import init_db
        conn = init_db.crear_base_datos()
        init_db.insertar_plantas(conn)
        init_db.insertar_usuarios(conn)
        init_db.insertar_relaciones(conn)
        conn.close()


@app.route("/api/plantas")
def get_plantas():
    conn = get_db()
    rows = conn.execute("SELECT * FROM plantas ORDER BY nombre_comun").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/api/plantas/<int:pid>")
def get_planta(pid):
    conn = get_db()
    row = conn.execute("SELECT * FROM plantas WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "No encontrada"}), 404
    return jsonify(dict(row))


@app.route("/api/usuarios")
def get_usuarios():
    conn = get_db()
    usuarios = conn.execute("SELECT * FROM usuarios ORDER BY nombre").fetchall()
    result = []
    for u in usuarios:
        u_dict = dict(u)
        plantas = conn.execute("""
            SELECT up.apodo, up.ubicacion_casa, up.estado, up.notas_personales,
                   p.id as planta_id, p.nombre_comun, p.nombre_cientifico,
                   p.luz, p.cuidado_nivel, p.temp_ideal_c, p.humedad_ideal_pct
            FROM usuario_plantas up
            JOIN plantas p ON p.id = up.planta_id
            WHERE up.usuario_id = ?
        """, (u["id"],)).fetchall()
        u_dict["plantas"] = [dict(p) for p in plantas]
        result.append(u_dict)
    conn.close()
    return jsonify(result)


@app.route("/api/stats")
def get_stats():
    conn = get_db()
    stats = {
        "total_plantas":    conn.execute("SELECT COUNT(*) FROM plantas").fetchone()[0],
        "total_usuarios":   conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
        "total_relaciones": conn.execute("SELECT COUNT(*) FROM usuario_plantas").fetchone()[0],
        "por_luz":          {r[0]: r[1] for r in conn.execute(
                                "SELECT luz, COUNT(*) FROM plantas GROUP BY luz")},
        "por_nivel":        {r[0]: r[1] for r in conn.execute(
                                "SELECT cuidado_nivel, COUNT(*) FROM plantas GROUP BY cuidado_nivel")},
        "por_tipo":         {r[0]: r[1] for r in conn.execute(
                                "SELECT tipo, COUNT(*) FROM plantas GROUP BY tipo")},
        "comestibles":      conn.execute("SELECT COUNT(*) FROM plantas WHERE comestible=1").fetchone()[0],
        "toxicas":          conn.execute("SELECT COUNT(*) FROM plantas WHERE toxica_mascotas=1").fetchone()[0],
    }
    conn.close()
    return jsonify(stats)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("static", path)


if __name__ == "__main__":
    init_db_if_needed()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
