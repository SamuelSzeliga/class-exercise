import logging
import sqlite3
from pathlib import Path

logging.basicConfig(
level=logging.DEBUG,
format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
datefmt="%H:%M:%S"
)

logger = logging.getLogger(__name__)

class BookStorage:
    def __init__(self, db_path="data/books.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                price REAL NOT NULL
            )
            """
            connection.execute(sql_statement)
            connection.commit()
            logger.debug(f"Database ready: {self.db_path}")
        finally:
            connection.close()


    def add_book(self, title, price):
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            cursor = connection.execute(sql_statement, ("Book A", 12.5))
            book_id = cursor.lastrowid
            connection.commit()
            logger.debug(f"New id: {book_id}")
            return book_id
        except sqlite3.Error:
            #For a failed write, `rollback()` cancels uncommitted changes and `raise` passes the error to the caller.
            connection.rollback()
            raise
        finally:
            # Always close the connection, whether the operation succeeds or fails.
            connection.close()


    def get_book(self, book_id):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
            row = connection.execute(sql_statement, (book_id,)).fetchone()
            if row:
                logger.debug(f"ID: {book_id}, row found:{row}")
                return dict(row)
            else:
                logger.debug(f"ID: {book_id}, row not found")
                return None
        finally:
            connection.close()


    def list_books(self, min_price=0, limit=100):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            input = """
                SELECT id, title, price
                FROM books
                WHERE price >= ?
                ORDER BY price DESC, id ASC
                LIMIT ?
            """
            cursor = connection.execute(input, (min_price, limit))
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            logger.debug(f"{len(result)} rows returned")
            return result
        finally:
            connection.close()

    def search_books(self, min_price, max_price):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            sql_statement = "Select * from books WHERE price >= ? AND price <= ?"
            connection.execute(sql_statement, (min_price,max_price)).fetchall()
            rows = [dict(row) for row in rows]
            logger.debug(f"{len(rows)} found")
            return rows    
        finally:
            connection.close()

    def replace_books(self, books):
        connection = sqlite3.connect(self.db_path)
        try:
            sql_statement = "DELETE FROM books"
            connection.execute(sql_statement)
            sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
            connection.executemany(sql_statement, books)
            connection.commit()
            logger.debug(f"Replaced books: rows={len(books)}")
        except sqlite3.Error:
            connection.rollback()
            raise
        finally:
            connection.close()

storage = BookStorage()

def main():
    path = Path("data") / "books.db"
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row

    sql_statement = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        price REAL NOT NULL
    )
    """
    connection.execute(sql_statement)
    connection.execute("DELETE FROM books")
    connection.commit()


    sql_statement = "INSERT INTO books (title, price) VALUES (?, ?)"
    cursor = connection.execute(sql_statement, ("Book A", 12.5))
    book_id = cursor.lastrowid
    connection.commit()

    # Retrieve one book 
    sql_statement = "SELECT id, title, price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(dict(row))

    # Preview the first n
    sql_statement = "SELECT * FROM books ORDER BY id LIMIT ?"
    rows = connection.execute(sql_statement, (5,)).fetchall()
    print([dict(row) for row in rows])

    # Filter and Sort
    sql_statement = """
    SELECT title, price FROM books
    WHERE price >= ? ORDER BY price DESC LIMIT ?
    """
    rows = connection.execute(sql_statement, (15, 2)).fetchall()
    print([dict(row) for row in rows])

    #Total count
    sql_statement = "SELECT COUNT(*) AS total FROM books"
    row = connection.execute(sql_statement).fetchone()
    print(row["total"])

    #Update
    sql_statement = "UPDATE books SET price = ? WHERE id = ?"
    connection.execute(sql_statement, (13.0, book_id))
    connection.commit()

    #Check
    sql_statement = "SELECT price FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(row["price"])  # 13.0

    #Delete
    sql_statement = "DELETE FROM books WHERE id = ?"
    connection.execute(sql_statement, (book_id,))
    connection.commit()
    
    #Check
    sql_statement = "SELECT * FROM books WHERE id = ?"
    row = connection.execute(sql_statement, (book_id,)).fetchone()
    print(row)  # None

    connection.close()

    try:
       storage.replace_books([("New Book", 20.0), (None, 10.0)])
    except sqlite3.IntegrityError:
       print("Replacement failed; original books kept.")


if __name__ == "__main__":
    main()