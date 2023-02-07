from flask import Flask, request, jsonify
import json
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("persons.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn


@app.route("/persons", methods=["GET", "POST"])
def persons():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM person")
        persons = [
            dict(id=row[0], firstName=row[1], lastName=row[2])
            for row in cursor.fetchall()
        ]
        if persons is not None:
            return jsonify(persons)

    if request.method == "POST":
        new_firstName = request.form["firstName"]
        new_lastName = request.form["lastName"]
        sql = """INSERT INTO person (firstName, lastName)
                 VALUES (?, ?)"""
        cursor = cursor.execute(sql, (new_firstName, new_lastName))
        conn.commit()
        return f"person with the id: 0 created successfully", 201


@app.route("/person/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_person(id):
    conn = db_connection()
    cursor = conn.cursor()
    person = None
    if request.method == "GET":
        cursor.execute("SELECT * FROM person WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            person = r
        if person is not None:
            return jsonify(person), 200
        else:
            return "Something wrong", 404

    if request.method == "PUT":
        sql = """UPDATE person
                SET firstName=?,
                    lastName=?
                WHERE id=? """

        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        updated_person = {
            "id": id,
            "firstName": firstName,
            "lastName": lastName,
        }
        conn.execute(sql, (firstName, lastName,id))
        conn.commit()
        return jsonify(updated_person)

    if request.method == "DELETE":
        sql = """ DELETE FROM person WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The person with id: {} has been ddeleted.".format(id), 200


if __name__ == "__main__":
    app.run(debug=True)