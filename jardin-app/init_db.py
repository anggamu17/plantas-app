import sqlite3
import os

DB_PATH = "/home/claude/jardin.db"

def crear_base_datos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # ── Tabla: plantas ──────────────────────────────────────────────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS plantas (
        id                  INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_comun        TEXT NOT NULL,
        nombre_cientifico   TEXT NOT NULL,
        tipo                TEXT NOT NULL,          -- herbácea, arbusto, árbol, suculenta, trepadora, acuática
        luz                 TEXT NOT NULL,          -- sombra, semisombra, sol directo
        temp_min_c          REAL NOT NULL,
        temp_max_c          REAL NOT NULL,
        temp_ideal_c        REAL NOT NULL,
        humedad_min_pct     INTEGER NOT NULL,
        humedad_max_pct     INTEGER NOT NULL,
        humedad_ideal_pct   INTEGER NOT NULL,
        riego               TEXT NOT NULL,          -- escaso, moderado, frecuente, muy frecuente
        frecuencia_riego_dias INTEGER,              -- cada cuántos días regar aprox.
        sustrato            TEXT,
        toxica_mascotas     INTEGER NOT NULL DEFAULT 0,  -- 0/1
        comestible          INTEGER NOT NULL DEFAULT 0,  -- 0/1
        floracion           TEXT,                   -- primavera, verano, otoño, invierno, todo el año, ninguna
        altura_max_cm       INTEGER,
        origen              TEXT,
        cuidado_nivel       TEXT NOT NULL,          -- fácil, intermedio, difícil
        notas               TEXT
    )
    """)

    # ── Tabla: usuarios ─────────────────────────────────────────────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre          TEXT NOT NULL,
        apellido        TEXT NOT NULL,
        correo          TEXT UNIQUE NOT NULL,
        telefono        TEXT,
        ciudad          TEXT,
        pais            TEXT DEFAULT 'México',
        experiencia     TEXT NOT NULL,              -- principiante, intermedio, experto
        tipo_espacio    TEXT,                       -- interior, exterior, balcón, jardín, invernadero
        fecha_registro  TEXT DEFAULT (date('now'))
    )
    """)

    # ── Tabla relación usuarios↔plantas ─────────────────────────────────────────
    c.execute("""
    CREATE TABLE IF NOT EXISTS usuario_plantas (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id      INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
        planta_id       INTEGER NOT NULL REFERENCES plantas(id)  ON DELETE CASCADE,
        apodo           TEXT,                       -- nombre personal que el usuario le da
        fecha_adquisicion TEXT DEFAULT (date('now')),
        ubicacion_casa  TEXT,                       -- sala, patio, terraza, recámara…
        estado          TEXT DEFAULT 'sana',        -- sana, enferma, en tratamiento, muerta
        notas_personales TEXT
    )
    """)

    conn.commit()
    return conn


def insertar_plantas(conn):
    c = conn.cursor()
    plantas = [
        # (nombre_comun, nombre_cientifico, tipo, luz,
        #  temp_min, temp_max, temp_ideal,
        #  hum_min, hum_max, hum_ideal,
        #  riego, freq_dias, sustrato,
        #  toxica, comestible, floracion, altura_cm, origen, nivel, notas)
        ("Pothos","Epipremnum aureum","trepadora","sombra",
         15,30,22, 40,70,55, "moderado",7,"universal",1,0,"ninguna",200,"Asia",
         "fácil","Purifica el aire; muy resistente al abandono."),

        ("Monstera","Monstera deliciosa","herbácea","semisombra",
         18,30,24, 50,80,65, "moderado",10,"universal+perlita",0,1,"verano",300,"México/C. América",
         "fácil","Frutas comestibles cuando madura completamente."),

        ("Suculenta echeveria","Echeveria elegans","suculenta","sol directo",
         5,35,22, 10,40,20, "escaso",21,"cactáceas",0,0,"primavera",15,"México",
         "fácil","Propagar por hojas o hijuelos."),

        ("Cactus saguaro","Carnegiea gigantea","suculenta","sol directo",
         -5,45,28, 5,30,15, "escaso",30,"cactáceas+arena",0,0,"primavera",1200,"México/EUA",
         "fácil","Puede vivir más de 150 años."),

        ("Lavanda","Lavandula angustifolia","arbusto","sol directo",
         -10,35,20, 30,60,40, "escaso",14,"arena+caliza",0,1,"verano",90,"Mediterráneo",
         "fácil","Repelente natural de mosquitos."),

        ("Helecho de Boston","Nephrolepis exaltata","herbácea","semisombra",
         10,28,20, 60,90,75, "frecuente",3,"turba+perlita",0,0,"ninguna",90,"América tropical",
         "intermedio","Necesita alta humedad; ideal para baños."),

        ("Paz lirio","Spathiphyllum wallisii","herbácea","sombra",
         15,30,22, 50,80,65, "moderado",7,"universal",1,0,"primavera",60,"Colombia",
         "fácil","Gran purificador de aire."),

        ("Aloe vera","Aloe barbadensis","suculenta","sol directo",
         10,40,26, 20,50,30, "escaso",14,"cactáceas",1,1,"verano",60,"África",
         "fácil","Gel medicinal en las hojas."),

        ("Rosa","Rosa spp.","arbusto","sol directo",
         -15,35,20, 40,70,55, "moderado",5,"arcilla+humus",0,0,"primavera",150,"Asia",
         "intermedio","Requiere poda regular."),

        ("Orquídea mariposa","Phalaenopsis spp.","herbácea","semisombra",
         16,30,23, 50,75,65, "moderado",7,"corteza de pino",0,0,"invierno",60,"Asia",
         "intermedio","No regar en exceso; raíces necesitan aireación."),

        ("Ficus benjamina","Ficus benjamina","árbol","semisombra",
         15,30,22, 50,70,60, "moderado",7,"universal",1,0,"ninguna",300,"Asia",
         "intermedio","Sensible a cambios de ubicación."),

        ("Begonia","Begonia semperflorens","herbácea","semisombra",
         10,28,20, 50,75,65, "moderado",5,"turba+perlita",1,0,"todo el año",40,"Brasil",
         "fácil","Floración continua."),

        ("Geranio","Pelargonium hortorum","herbácea","sol directo",
         5,30,20, 30,60,45, "moderado",5,"universal",0,0,"primavera",50,"Sudáfrica",
         "fácil","Perfumado; repele insectos."),

        ("Cinta","Chlorophytum comosum","herbácea","semisombra",
         10,30,20, 40,70,55, "moderado",7,"universal",0,0,"verano",40,"Sudáfrica",
         "fácil","Purifica benceno y monóxido."),

        ("Bambú de la suerte","Dracaena sanderiana","herbácea","semisombra",
         18,32,25, 50,80,65, "moderado",7,"agua o universal",1,0,"ninguna",100,"África",
         "fácil","Puede cultivarse en agua."),

        ("Tomate cherry","Solanum lycopersicum","herbácea","sol directo",
         10,35,24, 50,80,65, "frecuente",2,"sustrato rico",0,1,"verano",120,"Andes/México",
         "intermedio","Requiere tutores y poda de chupones."),

        ("Menta","Mentha spicata","herbácea","semisombra",
         5,28,18, 50,75,65, "frecuente",3,"universal",0,1,"verano",50,"Europa",
         "fácil","Invasiva; mejor en maceta."),

        ("Albahaca","Ocimum basilicum","herbácea","sol directo",
         15,35,24, 40,70,55, "frecuente",2,"universal rico",0,1,"verano",50,"India",
         "fácil","Picar flores para prolongar vida."),

        ("Suculenta haworthia","Haworthia fasciata","suculenta","semisombra",
         5,35,20, 10,40,25, "escaso",21,"cactáceas",0,0,"primavera",15,"Sudáfrica",
         "fácil","Ideal para escritorios sin mucha luz."),

        ("Calathea","Calathea ornata","herbácea","sombra",
         18,30,24, 60,90,75, "moderado",5,"turba+perlita",0,0,"ninguna",60,"Colombia",
         "difícil","Hojas se cierran de noche; sensible al cloro."),

        ("Palmera areca","Dypsis lutescens","árbol","semisombra",
         16,32,24, 50,80,65, "moderado",7,"universal+arena",0,0,"verano",200,"Madagascar",
         "intermedio","Humidificador natural."),

        ("Hortensia","Hydrangea macrophylla","arbusto","semisombra",
         -5,30,18, 60,80,70, "frecuente",3,"ácido",0,0,"verano",150,"China/Japón",
         "intermedio","Color depende del pH del suelo."),

        ("Bromelia","Bromelia pinguin","herbácea","semisombra",
         15,32,24, 50,80,65, "moderado",7,"bromeliáceas",0,1,"primavera",60,"América tropical",
         "intermedio","Agua en la copa central."),

        ("Hiedra","Hedera helix","trepadora","sombra",
         5,25,16, 40,70,55, "moderado",7,"universal",1,0,"otoño",300,"Europa",
         "fácil","Muy invasiva en exterior."),

        ("Zamioculca","Zamioculcas zamiifolia","herbácea","sombra",
         15,35,24, 30,60,45, "escaso",14,"arena+universal",1,0,"ninguna",100,"África",
         "fácil","Tolerante a poca luz y sequía."),

        ("Cactus de Navidad","Schlumbergera bridgesii","suculenta","semisombra",
         10,25,18, 50,70,60, "moderado",10,"cactáceas+humus",0,0,"invierno",30,"Brasil",
         "fácil","Floración espectacular en diciembre."),

        ("Peperomia","Peperomia obtusifolia","herbácea","semisombra",
         15,30,22, 40,70,55, "moderado",10,"universal liviano",0,0,"ninguna",30,"América tropical",
         "fácil","Muy versátil y resistente."),

        ("Jazmín","Jasminum officinale","trepadora","sol directo",
         5,35,22, 40,70,55, "moderado",7,"universal",0,1,"verano",400,"Asia",
         "intermedio","Intensamente perfumado."),

        ("Árbol de jade","Crassula ovata","suculenta","sol directo",
         10,35,22, 20,50,35, "escaso",14,"cactáceas",1,0,"invierno",120,"Sudáfrica",
         "fácil","Muy longevo; símbolo de buena suerte."),

        ("Violeta africana","Saintpaulia ionantha","herbácea","semisombra",
         16,26,22, 50,70,60, "moderado",7,"africanas",0,0,"todo el año",15,"Tanzania",
         "intermedio","No mojar las hojas."),

        ("Pasto de trigo","Triticum aestivum","herbácea","sol directo",
         5,30,20, 50,80,65, "frecuente",2,"universal rico",0,1,"ninguna",30,"Oriente Medio",
         "fácil","Se cosecha a los 7-10 días."),

        ("Dracena marginata","Dracaena marginata","árbol","semisombra",
         15,32,24, 40,70,55, "moderado",10,"universal",1,0,"primavera",300,"Madagascar",
         "fácil","Tolera bien la sequía."),

        ("Aeonium","Aeonium arboreum","suculenta","sol directo",
         5,30,18, 20,50,35, "escaso",14,"cactáceas+arena",0,0,"invierno",90,"Canarias",
         "fácil","Dormancia en verano."),

        ("Fuchsia","Fuchsia hybrida","arbusto","semisombra",
         5,25,16, 60,80,70, "frecuente",3,"universal",0,0,"verano",60,"América Central",
         "intermedio","Ideal para jardineras colgantes."),

        ("Hierbabuena","Mentha piperita","herbácea","semisombra",
         5,30,20, 50,75,65, "frecuente",3,"universal rico",0,1,"verano",50,"Europa",
         "fácil","Uso culinario y medicinal."),

        ("Árnica","Arnica montana","herbácea","sol directo",
         -10,25,15, 50,75,60, "moderado",7,"ácido pobre",0,0,"verano",60,"Europa",
         "difícil","Medicinal; tóxica ingerida."),

        ("Anturio","Anthurium andraeanum","herbácea","semisombra",
         18,32,25, 60,80,70, "moderado",7,"orquídeas+perlita",1,0,"todo el año",50,"Colombia",
         "intermedio","Espata colorida todo el año."),

        ("Cactus de órgano","Pachycereus marginatus","suculenta","sol directo",
         5,45,30, 5,30,15, "escaso",30,"cactáceas+arena",0,0,"primavera",700,"México",
         "fácil","Emblema del paisaje mexicano."),

        ("Lirio cala","Zantedeschia aethiopica","herbácea","semisombra",
         10,28,20, 60,85,75, "frecuente",3,"arcilla húmeda",1,0,"primavera",100,"Sudáfrica",
         "intermedio","Planta semiacuática."),

        ("Gardenia","Gardenia jasminoides","arbusto","semisombra",
         15,28,22, 60,80,70, "frecuente",4,"ácido",0,0,"verano",150,"China",
         "difícil","Muy perfumada; exigente."),

        ("Planta serpiente","Sansevieria trifasciata","herbácea","semisombra",
         15,35,24, 30,70,50, "escaso",14,"cactáceas+arena",1,0,"primavera",120,"África",
         "fácil","Purifica el aire; prácticamente indestructible."),

        ("Camelia","Camellia japonica","arbusto","semisombra",
         -5,25,16, 60,80,70, "moderado",7,"ácido",0,0,"invierno",300,"Asia",
         "difícil","Flores espectaculares; larga vida."),

        ("Cactus barril","Ferocactus wislizeni","suculenta","sol directo",
         -5,45,30, 5,30,15, "escaso",30,"cactáceas",0,0,"verano",120,"México/EUA",
         "fácil","Aguarda agua en su interior."),

        ("Romero","Salvia rosmarinus","arbusto","sol directo",
         -10,35,22, 30,60,45, "escaso",10,"arenoso pobre",0,1,"primavera",150,"Mediterráneo",
         "fácil","Culinario, medicinal y aromático."),

        ("Alocasia","Alocasia amazonica","herbácea","semisombra",
         18,30,25, 60,90,75, "moderado",7,"turba+perlita",1,0,"ninguna",90,"Híbrido",
         "difícil","Hojas dramáticas; alta humedad."),

        ("Agave","Agave americana","suculenta","sol directo",
         -5,45,28, 10,40,20, "escaso",30,"cactáceas+arena",0,1,"ninguna",200,"México",
         "fácil","Florece una sola vez al morir."),

        ("Bugambilia","Bougainvillea glabra","trepadora","sol directo",
         5,40,25, 30,60,45, "moderado",7,"arena+universal",0,0,"todo el año",600,"Brasil",
         "fácil","Icónica en México."),

        ("Coleo","Coleus scutellarioides","herbácea","semisombra",
         15,32,24, 50,80,65, "frecuente",3,"universal",0,0,"verano",60,"Asia",
         "fácil","Follaje multicolor llamativo."),

        ("Nopales","Opuntia ficus-indica","suculenta","sol directo",
         -5,45,28, 10,40,20, "escaso",21,"cactáceas",0,1,"primavera",200,"México",
         "fácil","Alimento tradicional mexicano."),

        ("Girasol","Helianthus annuus","herbácea","sol directo",
         5,35,24, 40,75,60, "moderado",3,"universal rico",0,1,"verano",300,"América del Norte",
         "fácil","Anual; semillas comestibles."),

        ("Planta de caucho","Ficus elastica","árbol","semisombra",
         15,30,22, 40,70,55, "moderado",10,"universal",1,0,"ninguna",300,"India/Malasia",
         "fácil","Hojas grandes y brillantes."),

        ("Lirio de tigre","Lilium lancifolium","herbácea","sol directo",
         -10,30,20, 50,75,65, "moderado",5,"universal rico",1,0,"verano",100,"Asia",
         "intermedio","Bulbosa; tóxica para gatos."),

        ("Pino de Navidad","Abies nordmanniana","árbol","sol directo",
         -20,25,12, 50,80,65, "moderado",14,"ácido forestal",0,0,"ninguna",2000,"Cáucaso",
         "difícil","Requiere frío; no apto climas cálidos."),

        ("Cilantro","Coriandrum sativum","herbácea","sol directo",
         5,30,20, 40,70,55, "moderado",4,"universal",0,1,"primavera",60,"Mediterráneo",
         "fácil","Anual; cosecha continua."),

        ("Flor de Pascua","Euphorbia pulcherrima","arbusto","semisombra",
         15,30,22, 40,70,55, "moderado",7,"universal",1,0,"invierno",120,"México",
         "fácil","Tóxica; icónica en Navidad."),
    ]

    c.executemany("""
        INSERT OR IGNORE INTO plantas
        (nombre_comun,nombre_cientifico,tipo,luz,
         temp_min_c,temp_max_c,temp_ideal_c,
         humedad_min_pct,humedad_max_pct,humedad_ideal_pct,
         riego,frecuencia_riego_dias,sustrato,
         toxica_mascotas,comestible,floracion,altura_max_cm,origen,cuidado_nivel,notas)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, plantas)
    conn.commit()
    print(f"✅ {c.rowcount} plantas insertadas (o ya existían).")


def insertar_usuarios(conn):
    c = conn.cursor()
    usuarios = [
        ("Ana","García","ana.garcia@email.com","5551001001","CDMX","México","principiante","balcón"),
        ("Carlos","Hernández","carlos.h@email.com","5551001002","Guadalajara","México","intermedio","jardín"),
        ("María","López","maria.lopez@email.com","5551001003","Monterrey","México","experto","invernadero"),
        ("José","Martínez","jose.m@email.com","5551001004","Puebla","México","principiante","interior"),
        ("Laura","Rodríguez","laura.r@email.com","5551001005","Mérida","México","intermedio","exterior"),
        ("Pedro","Sánchez","pedro.s@email.com","5551001006","Cancún","México","experto","jardín"),
        ("Sofía","Torres","sofia.t@email.com","5551001007","Querétaro","México","fácil","balcón"),
        ("Miguel","Ramírez","miguel.r@email.com","5551001008","Tijuana","México","intermedio","terraza"),
        ("Isabel","Flores","isabel.f@email.com","5551001009","San Luis Potosí","México","principiante","interior"),
        ("Roberto","Cruz","roberto.c@email.com","5551001010","Oaxaca","México","experto","jardín"),
    ]
    c.executemany("""
        INSERT OR IGNORE INTO usuarios
        (nombre,apellido,correo,telefono,ciudad,pais,experiencia,tipo_espacio)
        VALUES (?,?,?,?,?,?,?,?)
    """, usuarios)
    conn.commit()
    print(f"✅ {c.rowcount} usuarios insertados.")


def insertar_relaciones(conn):
    c = conn.cursor()
    relaciones = [
        # (usuario_id, planta_id, apodo, ubicacion, estado, notas)
        (1,1,"Mi Pothos","sala","sana","La riego los lunes"),
        (1,7,"Lirio paz","recámara","sana","Purifica el aire"),
        (1,14,"Cintas","balcón","sana",None),
        (1,25,"Zami","oficina","sana","Muy resistente"),
        (2,5,"Lavanda francesa","jardín","sana","Ya floró dos veces"),
        (2,9,"Rosa roja","jardín","sana","Poda en marzo"),
        (2,23,"Bromelia","patio","sana",None),
        (2,47,"Bugambilia","barda","sana","Crece muy rápido"),
        (3,10,"Orquídea","invernadero","sana","Sustrato especial"),
        (3,20,"Calathea","invernadero","sana","Humedad al 80%"),
        (3,30,"Violeta","invernadero","sana","Luz indirecta"),
        (3,40,"Gardenia","invernadero","sana","Exige mucho"),
        (3,44,"Camelia","invernadero","sana","Floreció en enero"),
        (4,1,"Pothos pequeño","baño","sana",None),
        (4,7,"Paz","sala","sana","Regalo de mi mamá"),
        (4,41,"Sansevieria","entrada","sana","No la riego seguido"),
        (5,5,"Lavanda","terraza","sana",None),
        (5,15,"Bambú","sala","sana","En agua"),
        (5,17,"Menta","cocina","sana","La uso en el té"),
        (5,18,"Albahaca","cocina","sana","Para pastas"),
        (6,37,"Anthurio","jardín","sana",None),
        (6,46,"Agave azul","jardín","sana","Muy viejo"),
        (6,48,"Coleo","jardín","sana","Muy colorido"),
        (6,49,"Nopal","jardín","sana","Cosecho tunas"),
        (7,3,"Echeveria","balcón","sana","La propago"),
        (7,27,"Jade","balcón","sana","10 años tengo"),
        (7,33,"Aeonium","balcón","sana",None),
        (7,43,"Barril","balcón","sana","Crece muy lento"),
        (8,2,"Monstera","sala","sana","Ya tiene 3 hojas nuevas"),
        (8,12,"Begonia","sala","sana","Siempre florece"),
        (8,21,"Palmera","sala","sana","Muy grande ya"),
        (9,1,"Pothos baño","baño","sana",None),
        (9,8,"Aloe","ventana","sana","Para quemaduras"),
        (9,54,"Cilantro","cocina","sana","Para cocinar"),
        (9,55,"Flor Pascua","sala","sana","Navideña"),
        (10,11,"Ficus","jardín","sana",None),
        (10,36,"Alocasia","jardín","sana","Muy dramática"),
        (10,50,"Girasol","jardín","sana","Recién sembré"),
        (10,51,"Caucho","jardín","sana","Ya tiene 2 m"),
    ]
    c.executemany("""
        INSERT OR IGNORE INTO usuario_plantas
        (usuario_id,planta_id,apodo,ubicacion_casa,estado,notas_personales)
        VALUES (?,?,?,?,?,?)
    """, relaciones)
    conn.commit()
    print(f"✅ {c.rowcount} relaciones usuario-planta insertadas.")


def mostrar_resumen(conn):
    c = conn.cursor()
    print("\n" + "="*60)
    print("  RESUMEN DE LA BASE DE DATOS")
    print("="*60)

    c.execute("SELECT COUNT(*) FROM plantas")
    print(f"  🌿 Plantas registradas : {c.fetchone()[0]}")

    c.execute("SELECT COUNT(*) FROM usuarios")
    print(f"  👤 Usuarios registrados: {c.fetchone()[0]}")

    c.execute("SELECT COUNT(*) FROM usuario_plantas")
    print(f"  🔗 Relaciones         : {c.fetchone()[0]}")

    print("\n  Plantas por nivel de cuidado:")
    for row in c.execute("SELECT cuidado_nivel, COUNT(*) FROM plantas GROUP BY cuidado_nivel"):
        print(f"    {row[0]:<12}: {row[1]}")

    print("\n  Plantas por luz requerida:")
    for row in c.execute("SELECT luz, COUNT(*) FROM plantas GROUP BY luz"):
        print(f"    {row[0]:<15}: {row[1]}")

    print("\n  Plantas de cada usuario:")
    for row in c.execute("""
        SELECT u.nombre||' '||u.apellido AS usuario, COUNT(up.id) AS total
        FROM usuarios u
        LEFT JOIN usuario_plantas up ON u.id = up.usuario_id
        GROUP BY u.id ORDER BY total DESC
    """):
        print(f"    {row[0]:<25}: {row[1]} plantas")

    print("="*60)


if __name__ == "__main__":
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = crear_base_datos()
    insertar_plantas(conn)
    insertar_usuarios(conn)
    insertar_relaciones(conn)
    mostrar_resumen(conn)
    conn.close()
    print(f"\n✅ Base de datos creada: {DB_PATH}\n")
