import pymysql as database
import pymysql.cursors
from config import Config

class Connection:
    #   Get database connection
    @staticmethod
    def connect():
        return database.connect(
            host = Config.dbHost,
            user = Config.dbUser,
            password = Config.dbPassword,
            db = Config.dbName,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor
        )

    #   Get resident data using id
    @staticmethod
    def getResidentById(code):
        if code == None:
            return None
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT * FROM Resident WHERE id = %s'
                if(Config.debug):
                    print(query)
                cursor.execute(query, (code))
                result = cursor.fetchone()
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result

    #   Get resident data using name
    @staticmethod
    def getResidentByName(name):
        if name == None:
            return None
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT * FROM Resident WHERE '
                name = name.split()
                x = len(name)
                for i in range(x):
                    _name = connection.escape(name[i])[1:-1]
                    query += '(name LIKE \'%' + _name + '%\' OR surname LIKE \'%' + _name + '%\')'
                    if(i+1 < x):
                        query += " AND "
                if(Config.debug):
                    print(query)
                cursor.execute(query)
                result = cursor.fetchall()
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result

    #   Get residents of a room
    @staticmethod
    def getRoomResidents(room):
        if room == None:
            return None
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT * FROM Resident WHERE room LIKE %s'
                if(Config.debug):
                    print(query)
                    print("^ values: " + room)
                cursor.execute(query, ('%' + room + '%'))
                result = cursor.fetchall()
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result

    #   Get employees of a job
    @staticmethod
    def getEmployees(job):
        if job == None:
            return None
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = (
                    'SELECT Resident.name, Resident.surname, Job.name, (Job.manager = Resident.id) as manager FROM Resident'
                    ' INNER JOIN Employment ON Resident.id = Employment.residentId'
                    ' INNER JOIN Job ON Employment.jobId = Job.id'
                    ' WHERE Job.name = %s'
                )
                if(Config.debug):
                    print(query)
                    print("^ values: " + job)
                cursor.execute(query, ('%' + job + '%'))
                result = cursor.fetchall()
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result

    #   Get all jobs name
    @staticmethod
    def getJobs():
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT name FROM Job ORDER BY name ASC'
                if(Config.debug):
                    print(query)
                cursor.execute(query)
                result = [item['name'] for item in cursor.fetchall()]
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result

    #   Get all rooms name
    @staticmethod
    def getRooms():
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT DISTINCT room FROM Resident ORDER BY room ASC'
                if(Config.debug):
                    print(query)
                cursor.execute(query)
                result = [item['room'] for item in cursor.fetchall()]
                if(Config.debug):
                    print(result)
        finally:
            connection.close()
        return result
