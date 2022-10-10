import sqlite3, logging

class Cache:
    def __init__(self, dbpath:str, approach:str):
        self.db = sqlite3.connect(dbpath)
        self.approach = approach
        try:
            self.createTable()
        except sqlite3.OperationalError as ex:
            pass
        
    def createTable(self):
        self.db.execute('''CREATE TABLE {}_cache
        (subject TEXT NOT NULL,
        predicate TEXT NOT NULL,
        object TEXT NOT NULL,
        score REAL NOT NULL,
        PRIMARY KEY (subject, predicate, object)
        );'''.format(self.approach))
        
    def close(self):
        self.db.close()
        
    def insert(self, sub:str, pred:str, obj:str, score:float):
        input = [(sub), (pred), (obj), (score)]
        self.db.execute("INSERT INTO {}_cache (subject, predicate, object, score) VALUES (?, ?, ?, ?)".format(self.approach), input)
        self.db.commit()
        
    def update(self, sub:str, pred:str, obj:str, score:float):
        input = [(score), (sub), (pred), (obj)]
        self.db.execute("UPDATE {}_cache SET score=? WHERE subject=? AND predicate=? AND object=?".format(self.approach), input)
        self.db.commit()
    
    def getScore(self, sub:str, pred:str, obj:str):
        input = [(sub), (pred), (obj)]
        cursor = self.db.execute('SELECT score FROM {}_cache WHERE subject=? AND predicate=? AND object=?'.format(self.approach), input)
        for row in cursor:
            return row[0]
        
    def getAll(self):
        cursor = self.db.execute('SELECT * FROM {}_cache'.format(self.approach))
        rows = []
        for row in cursor:
            rows.append(row)
        return rows
            