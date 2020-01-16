from pyArango.connection import *

conn = Connection()

db = conn.createDatabase(name="school")
db = conn["school"]
print(db)

studentsCollection = db.createCollection(name="Students")
print(db["Students"])

doc = studentsCollection.createDocument()
doc["name"] = "John Smith"
print(doc)

doc2 = studentsCollection.createDocument()
doc2["firstname"] = "Emily"
doc2["lastname"] = "Bronte"
print(doc2)

doc._key = "johnsmith"
doc.save()

students = [('Oscar', 'Wilde', 3.5), ('Thomas', 'Hobbes', 3.2),
            ('Mark', 'Twain', 3.0), ('Kate', 'Chopin', 3.8), ('Fyodor', 'Dostoevsky', 3.1),
            ('Jane', 'Austen', 3.4), ('Mary', 'Wollstonecraft', 3.7), ('Percy', 'Shelley', 3.5),
            ('William', 'Faulkner', 3.8), ('Charlotte', 'Bronte', 3.0)]

for (first, last, gpa) in students:
    doc = studentsCollection.createDocument()
    doc['name'] = "%s %s" % (first, last)
    doc['gpa'] = gpa
    doc['year'] = 2019
    doc._key = ''.join([first, last]).lower()
    doc.save()


def select_all(col):
    for student in col.fetchAll():
        print("%s: %s" % (student['name'], student['gpa']))


def report_gpa(document):
    print("Student: %s" % document['name'])
    print("GPA: %s" % document['gpa'])


kate = studentsCollection['katechopin']
report_gpa(kate)


def update_gpa(key, new_gpa):
    doc = studentsCollection[key]
    doc["gpa"] = new_gpa
    doc.save()


update_gpa(kate, 3.4)
kate = studentsCollection['katechopin']
report_gpa(kate)


def top_scores(col, gpa):
    print("Top scores:")
    for student in col.fetchAll():
        if student['gpa'] >= gpa:
            print("- %s" % student['name'])


top_scores(studentsCollection, 3.5)


john = studentsCollection['johnsmith']
john.delete()

# Select with AQL (doesn't work)
aql = "FOR x IN Students RETURN x._key"
results = db.AQLQuery(aql, rawResults=False, batchSize=100)

for key in results:
    print(key)

# Insert with AQL
newDocument = {
    '_key': 'denisdiderot',
    'name': 'Denis Diderot',
    'gpa': 3.7
}
bind = {"doc": newDocument}
aql = "INSERT @doc INTO Students LET newDoc = NEW RETURN newDoc"
queryResult = db.AQLQuery(aql, bindVars=bind)
print(queryResult[0])

print(db["Students"]["katechopin"])
