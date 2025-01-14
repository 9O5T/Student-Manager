import sqlite3

def database_build():
    # Veritabanı bağlantısı oluştur
    conn = sqlite3.connect('nabla_database.db')
    cursor = conn.cursor()

    # exam_class_one tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS exam_class_one (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        save_time DATETIME,
                        student_key VARCHAR(15) NOT NULL,
                        matematik FLOAT NOT NULL,
                        fen FLOAT NOT NULL,
                        turkce FLOAT NOT NULL,
                        sosyal FLOAT NOT NULL,
                        total_question INTEGER NOT NULL,
                        answered_question INTEGER NOT NULL,
                        answered_true INTEGER NOT NULL,
                        answered_false INTEGER NOT NULL,
                        total_net INTEGER NOT NULL,
                        score FLOAT NOT NULL
                    )''')

    # exam_class_two tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS exam_class_two (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        save_time DATETIME,
                        student_key VARCHAR(15) NOT NULL,
                        matematik FLOAT NOT NULL,
                        turkce FLOAT NOT NULL,
                        fen FLOAT NOT NULL,
                        sosyal FLOAT NOT NULL,
                        ingilizce FLOAT NOT NULL,
                        region FLOAT NOT NULL,
                        total_question INTEGER NOT NULL,
                        answered_question INTEGER NOT NULL,
                        answered_true INTEGER NOT NULL,
                        answered_false INTEGER NOT NULL,
                        total_net INTEGER NOT NULL,
                        score FLOAT NOT NULL
                    )''')

    # exam_class_three tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS exam_class_three (
                        save_time DATETIME,
                        student_key VARCHAR(15) PRIMARY KEY NOT NULL,
                        type VARCHAR(15) NOT NULL,
                        sequence VARCHAR(50) NOT NULL,
                        score FLOAT NOT NULL
                    )''')

    # kurum tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS kurum (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(50) NOT NULL,
                        owner VARCHAR(50) NOT NULL,
                        mudur VARCHAR(50) NOT NULL,
                        capacity VARCHAR(50) NOT NULL
                    )''')

    # note tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS note (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time DATETIME,
                        student_key VARCHAR(15) NOT NULL,
                        topic VARCHAR(20) NOT NULL,
                        note VARCHAR(400) NOT NULL
                    )''')

    # payment_student tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS paymet_student (
                        student_key VARCHAR(15) PRIMARY KEY NOT NULL,
                        payment_day INTEGER NOT NULL,
                        payment_coast INTEGER NOT NULL,
                        first_month INTEGER NOT NULL,
                        month1 VARCHAR(15) DEFAULT 'ödenmedi',
                        month2 VARCHAR(15) DEFAULT 'ödenmedi',
                        month3 VARCHAR(15) DEFAULT 'ödenmedi',
                        month4 VARCHAR(15) DEFAULT 'ödenmedi',
                        month5 VARCHAR(15) DEFAULT 'ödenmedi',
                        month6 VARCHAR(15) DEFAULT 'ödenmedi',
                        month7 VARCHAR(15) DEFAULT 'ödenmedi',
                        month8 VARCHAR(15) DEFAULT 'ödenmedi',
                        month9 VARCHAR(15) DEFAULT 'ödenmedi',
                        month10 VARCHAR(15) DEFAULT 'ödenmedi',
                        month11 VARCHAR(15) DEFAULT 'ödenmedi',
                        month12 VARCHAR(15) DEFAULT 'ödenmedi'
                    )''')

    # quiz tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS quiz (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        time DATETIME,
                        student_key VARCHAR(15) NOT NULL,
                        lesson VARCHAR(20) NOT NULL,
                        total_question INTEGER NOT NULL,
                        answered_true INTEGER NOT NULL,
                        answered_false INTEGER NOT NULL,
                        score INTEGER NOT NULL
                    )''')

    # special_lesson tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS special_lesson (
                        teacher_key VARCHAR(30) PRIMARY KEY NOT NULL,
                        teacher_name VARCHAR(45) NOT NULL,
                        teacher_surname VARCHAR(45) NOT NULL,
                        student_key VARCHAR(20) NOT NULL,
                        student_name VARCHAR(45) NOT NULL,
                        student_surname VARCHAR(45) NOT NULL,
                        major VARCHAR(30) NOT NULL,
                        date VARCHAR(20) NOT NULL,
                        time VARCHAR(5) NOT NULL,
                        cost VARCHAR(20) NOT NULL
                    )''')

    # student tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS student (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(30) NOT NULL,
                        surname VARCHAR(30) NOT NULL,
                        personal_id VARCHAR(30) NOT NULL,
                        mother_name VARCHAR(30) NOT NULL,
                        father_name VARCHAR(30) NOT NULL,
                        class INTEGER NOT NULL,
                        school VARCHAR(100) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        adres VARCHAR(200) NOT NULL,
                        parent_tel VARCHAR(30) NOT NULL,
                        student_tel VARCHAR(30) NOT NULL,
                        student_key VARCHAR(15) UNIQUE
                    )''')

    # taxes tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS taxes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        month VARCHAR(5) NOT NULL,
                        year VARCHAR(5) NOT NULL,
                        type VARCHAR(200) NOT NULL,
                        gider VARCHAR(200) NOT NULL,
                        coast VARCHAR(20) NOT NULL,
                        label VARCHAR(20) NOT NULL
                    )''')

    # teacher tablosunu oluştur
    cursor.execute('''CREATE TABLE IF NOT EXISTS teacher (
                        name VARCHAR(30) NOT NULL,
                        surname VARCHAR(30) NOT NULL,
                        personal_id VARCHAR(30) PRIMARY KEY NOT NULL,
                        major VARCHAR(30) NOT NULL,
                        email VARCHAR(100) NOT NULL,
                        adres VARCHAR(200) NOT NULL,
                        tel VARCHAR(30) NOT NULL,
                        teacher_key VARCHAR(15) UNIQUE NOT NULL,
                        salary VARCHAR(20) NOT NULL
                    )''')

    # Veritabanı değişikliklerini kaydet
    conn.commit()

    # Veritabanı bağlantısını kapat
    conn.close()
