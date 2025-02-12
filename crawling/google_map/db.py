import pymysql

def connect_db():
    return pymysql.connect(
        host="labdb.coded2.fun",
        user="sophia",
        password="123456dv107",
        db="SOPHIA"
    )

def insert_data(reviews):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS google_map (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(10),
            store_name VARCHAR(10),
            rating tinyint,
            content TEXT
        )
    """)

    for review in reviews:
        sql = """
            INSERT INTO google_map (brand, store_name, rating, content)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(sql, (
            review['brand'],
            review['store_name'],
            review['rating'],
            review['content']
        ))

    conn.commit()
    conn.close()

def show_data():
    try:
        conn = pymysql.connect(
            host="labdb.coded2.fun",
            user="sophia",
            password="123456dv107",
            db="SOPHIA"
        )
        cur = conn.cursor()

        cur.execute("SELECT * FROM google_map LIMIT 5")
        results = cur.fetchall()

        for row in results:
            print(f"ID: {row[0]}")
            print(f"Brand: {row[1]}")
            print(f"Store name: {row[2]}")
            print(f"Rating: {row[3]}")
            print(f"Content: {row[4]}")
            print("---")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()