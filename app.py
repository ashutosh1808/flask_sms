from flask import Flask,render_template,request,url_for,redirect
from sqlite3 import *

app=Flask(__name__)

@app.route("/")
def home():
	con=None
	try:
		con=connect("studentms.db")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		return render_template("home.html",msg=data)
	except Exception as e:
		return render_template("home.html",msg=e)
	finally:
		if con is not None:
			con.close()
	return render_template("home.html")

@app.route("/create")
def create():
	if request.args.get("rn") and request.args.get("na") and request.args.get("marks"):
		rno=int(request.args.get("rn"))
		name=request.args.get("na")
		marks=int(request.args.get("marks"))
		con=None
		try:
			con=connect("studentms.db")
			cursor=con.cursor()
			sql="insert into student values('%d','%s','%d')"
			cursor.execute(sql%(rno,name,marks))
			con.commit()
			return render_template("create.html",msg="thanks for filling!")
		except Exception as e:
			con.rollback()
			return render_template("create.html",msg=e)
		finally:
			if con is not None:	con.close()
	else:
		return render_template("create.html")

@app.route("/delstu/<int:id>")
def delstu(id):
	con=None
	try:
		con=connect("studentms.db")
		cursor=con.cursor()
		sql="delete from student where rno='%d'"
		cursor.execute(sql%(id))
		con.commit()
		return redirect(url_for('home'))
	except Exception as e:
		con.rollback()
		return render_template("create.html",msg=e)
	finally:
		if con is not None:
			con.close()

if __name__=="__main__":
	app.run(debug=True,use_reloader=True)