"""
student api. 
basic CRUD and Query functionality 
Database starts with sqlite 
"""
from flask import Flask, jsonify, g, request
from database import get_db

app = Flask(__name__)

#-- LIST OF ALL STUDENTS FOM THE DATABASE
@app.route("/students", methods=["GET"])
def all_records():
	#-- connecting to the database 
	db = get_db()
	#-- General query from database 
	all_records_cur = db.execute("select * from students")
	all_records = all_records_cur.fetchall()

	#-- creat an empty list to hold all the records 
	return_records = []

	#-- Loop over database and create an dict from each record
	for record in all_records:
		record_dict = {}
		record_dict["student_id"] = record["student_id"]
		record_dict["first_name"] = record["first_name"]
		record_dict["last_name"] = record["last_name"]
		record_dict["addr"] = record["addr"]
		record_dict["phone"] = record["phone"]
		#-- append all results for each record to return_records
		return_records.append(record_dict)


	return jsonify({"Message": "All records", "Students": return_records})

#-- REQUEST FRO SINGLE STUDENT RECORD FROM DATABASE
@app.route("/student/<int:student_id>", methods=["GET"])
def get_record(student_id):
	db = get_db()

	record_cur = db.execute("select * from students where student_id = ?", [student_id])
	record = record_cur.fetchone()
	#-- data check if record doesnt exists 
	if record == None:
		return jsonify({"Message": "No record found!"}), 404
	else:
		return jsonify({"Message": "Single record by Student_id", "student_id": record["student_id"], "first name": record["first_name"], "last name": record["last_name"], "addr": record["addr"], "phone": record["phone"]})


#-- ADD A NEW RECORD TO THE DATABASE
@app.route("/student", methods=["POST"])
def add_record():
	#-- connecting to the database 
	db = get_db()
	
	#-- getting Values with request as a dict 
	new_record_data = request.get_json()

	student_id = new_record_data["student_id"]
	first_name = new_record_data["first_name"]
	last_name  = new_record_data["last_name"]
	addr 	   = new_record_data["addr"]
	phone      = new_record_data["phone"]
	
	#-- Daata check if record is already exists
	data_check_cur = db.execute("select * from students where student_id = ?", [student_id])
	check_record = data_check_cur.fetchone()
	if check_record == None:
		db.execute("insert into students (student_id, first_name, last_name, addr, phone) values(?,?,?,?,?)",[student_id, first_name, last_name, addr, phone])
		db.commit()
		return jsonify({"Message": "New record inserted into the database "})

	return jsonify({"Message": "Record already exists"})


#-- DELETE A RECORD FROM DATABASE
@app.route("/student/<int:student_id>", methods=["DELETE"])
def delete_record(student_id):
	#-- connecting to the database
	db = get_db()
	#-- Daata check if record is exists
	data_check_cur = db.execute("select * from students where student_id = ?", [student_id])
	check_record = data_check_cur.fetchone()
	if check_record == None:
		return jsonify({"Message": "No record found"}), 404
	
	else:
		db.execute("delete from students where student_id = ?", [student_id])
		db.commit()
		return jsonify({"message": "Record has been deleted!"})




#-- UPDATE A SINGLE RECORD IN STUDENT DATABASE
@app.route("/student/<int:student_id>", methods=["PUT","PATCH"])
def update_record(student_id):
	#-- connecting to the database
	db = get_db()
	#-- Daata check if record is exists
	data_check_cur = db.execute("select * from students where student_id = ?", [student_id])
	check_record = data_check_cur.fetchone()
	if check_record == None:
		return jsonify({"Message": "No record found"}), 404
	
	else:
		#-- getting Values with request as a dict 
		edited_record = request.get_json()

		student_id = edited_record["student_id"]
		first_name = edited_record["first_name"]
		last_name  = edited_record["last_name"]
		addr 	   = edited_record["addr"]
		phone      = edited_record["phone"]	
		db.execute("update students set student_id=?, first_name=?, last_name=?, addr=?, phone=? where student_id=?",[student_id, first_name, last_name, addr, phone, student_id])
		db.commit()
	return jsonify({"Message": "Record has been Updated"})




if __name__ == "__main__":
	app.run(debug=True)