import sqlite3
from typing import List, Dict, Union


class MolDB:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS compounds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                smiles TEXT
            )
        ''')
        self.conn.commit()

    def add_field(self, field_name: str, field_type: str):
        self.cursor.execute("PRAGMA table_info(compounds)")
        existing_fields = [info[1] for info in self.cursor.fetchall()]
        if field_name in existing_fields:
            print(f"The field '{field_name}' already exists.")
            return

        try:
            self.cursor.execute(f'ALTER TABLE compounds ADD COLUMN {
                                field_name} {field_type}')
            self.conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Failed to add field: {e}")

    def add_compound(self, name: str, smiles: str = None, **kwargs) -> int:
        fields = ['name', 'smiles'] + list(kwargs.keys())
        values = [name, smiles] + list(kwargs.values())
        placeholders = ', '.join(['?'] * len(fields))
        self.cursor.execute(
            f'INSERT INTO compounds ({", ".join(fields)}) VALUES ({placeholders})', values)
        self.conn.commit()
        return self.cursor.lastrowid

    def delete_compound(self, **kwargs) -> int:
        conditions = []
        params = []
        for key, value in kwargs.items():
            conditions.append(f"{key} = ?")
            params.append(value)

        sql_query = f'DELETE FROM compounds WHERE {" AND ".join(conditions)}'
        self.cursor.execute(sql_query, params)
        self.conn.commit()
        return self.cursor.rowcount

    def update_compound_property(self, name: str = None, smiles: str = None, compound_id: int = None, **kwargs):
        if not any([name, smiles, compound_id]):
            raise ValueError(
                "At least one identifier must be provided.")

        set_clauses = []
        where_clauses = []
        params = []

        for key, value in kwargs.items():
            set_clauses.append(f"{key} = ?")
            params.append(value)

        if name is not None:
            where_clauses.append("name = ?")
            params.append(name)
        if smiles is not None:
            where_clauses.append("smiles = ?")
            params.append(smiles)
        if compound_id is not None:
            where_clauses.append("id = ?")
            params.append(compound_id)

        update_query = f'UPDATE compounds SET {", ".join(set_clauses)} WHERE {
            " AND ".join(where_clauses)}'

        self.cursor.execute(update_query, params)
        self.conn.commit()

    def search_compounds(self, query: Dict[str, Union[str, int, float, bool]]) -> List[Dict[str, Union[str, int, float, bool]]]:
        conditions = []
        params = []
        for key, value in query.items():
            if isinstance(value, tuple):  # Range query
                conditions.append(f"{key} BETWEEN ? AND ?")
                params.extend(value)
            else:
                conditions.append(f"{key} = ?")
                params.append(value)

        sql_query = f'SELECT * FROM compounds WHERE {" AND ".join(conditions)}'
        self.cursor.execute(sql_query, params)
        results = self.cursor.fetchall()
        return [dict(zip([column[0] for column in self.cursor.description], row)) for row in results]

    def close(self):
        self.conn.close()
