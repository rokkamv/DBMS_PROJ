from flask import Flask, render_template, redirect, request, session, url_for
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='vaibhav99'
app.config['MYSQL_DB']='cabrides'
app.secret_key = '%jsdj!@'
mysql=MySQL(app)
afname = "Vaibhav"
acontact = "7587708800"

@app.route('/')
def main():
    if request.method == "POST":
        if 'contact' in session:
            if session['contact'] == acontact:
                return redirect('/adminPage')
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/index', methods=['GET'])
def index():
    if 'contact' in session:
        con = mysql.connection
        cur = con.cursor()
        contact=session['contact']
        cur.execute("select RiderId from RIDERS where Contact=(%s)",(contact,))
        riderid = cur.fetchall()
        cur.execute("select RideId,DriverId,DateTime_start,DateTime_end,Pickup_loc,Drop_loc,Type,Fare from RIDES where RiderId=(%s)",(riderid[0],))
        rows=cur.fetchall()
        return render_template('index.html',rows=rows)
    else:
        return redirect(url_for('login'))

@app.route('/rider')
def rider():
    if 'contact' in session:
        con=mysql.connection
        cur=con.cursor()
        contact=session['contact']
        if session['contact']==acontact:
            cur.execute('select * from RIDERS where Contact=%s',(acontact,))
            row=cur.fetchall()
            return render_template('admin.html',rows=row)
        cur.execute('select * from RIDERS where Contact=%s',(contact,))
        row=cur.fetchall()
        return render_template('rider.html',rows=row)
    return render_template('login.html')

@app.route('/adminPage')
def adminPage():
    if (session['contact'] == acontact):
        con = mysql.connection
        cur = con.cursor()
        cur.execute("select * from RIDES")
        rows = cur.fetchall()
        cur.execute("select * from DRIVERS")
        rows1=cur.fetchall()
        cur.execute("select * from RIDERS")
        rows2=cur.fetchall()
        cur.execute("select * from VEHICLE")
        rows3=cur.fetchall()
        cur.execute("select * from CANCELLED_RIDES")
        rows4=cur.fetchall()
        return render_template('adminPage.html',rows=rows, rows1=rows1, rows2=rows2, rows3=rows3, rows4=rows4)
    return redirect('/index')

@app.route('/login', methods =['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        fname = request.form['first_name']
        contact = request.form['contact']
        validate = validate_user(fname,contact)
        if validate == False:
            error = 'Invalid credentials. Please try again!'
        else:
            session['contact'] = contact
            if(session['contact'] == acontact):
                session['contact']=acontact
                return redirect('/adminPage')
            return redirect('/index')
    if 'contact' in session:
        if session['contact']==acontact:
            return redirect('/adminPage')
        return redirect('/index')
    return render_template('login.html',error=error)

def validate_user(fname,contact):
    con = mysql.connection
    validate = False

    with con:
        cur = con.cursor()
        cur.execute('select First_Name, Contact from RIDERS')
        rows = cur.fetchall()
        for row in rows:
            dfname = row[0]
            dcontact = row[1]
            if(dfname == fname and dcontact == contact):
                validate = True
                break
    return validate


@app.route('/signup',methods=['GET','POST'])
def signup():
    con = mysql.connection
    cur = con.cursor()
    error = None
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        contact = request.form['contact']
        cur.execute('select RiderId,Contact from RIDERS')
        rows = cur.fetchall()
        for row in rows:
            if(row[0] == fname and row[1]==contact):
                error = 'Rider already exists!'
                return render_template('signup.html',error=error)
            elif(row[1]==contact):
                error = 'Contact already exists!'
                return render_template('signup.html',error=error)

        session['contact'] = contact
        cur.execute("insert into RIDERS(First_Name, Last_Name, Contact) values(%s,%s,%s)",(fname,lname,contact))
        con.commit()
        return redirect('/index')
    if 'contact' in session:
        return redirect('/index')
    return render_template('signup.html',error=error)

@app.route('/logout')
def logout():
    session.pop('contact', None)
    return redirect(url_for('login'))

#------------------------------------------ADMIN------------------------------------------
@app.route('/insert',methods=['GET','POST'])
def insert():
    if(session['contact']==acontact):
        con=mysql.connection
        cur=con.cursor()
        if(request.method=='POST'):
            if 'rideform' in request.form:
                #rideid=request.form['rideid']
                rdriverid=request.form['rdriverid']
                rriderid=request.form['rriderid']
                dtstart=request.form['dtstart']
                dtend=request.form['dtend']
                ploc=request.form['ploc']
                dloc=request.form['dloc']
                rtype=request.form['rtype']
                duplicate=duplicate_ride(dtstart,dtend)
                if duplicate==True:
                    return render_template('insert.html')
                cur.execute("insert into RIDES(DriverId,RiderId,DateTime_start,DateTime_end,Pickup_loc,Drop_loc,Type) values(%s,%s,%s,%s,%s,%s,%s)",(rdriverid,rriderid,dtstart,dtend,ploc,dloc,rtype))
                con.commit()
                return redirect('/adminPage')
            if 'driverform' in request.form:
                #driverid=request.form['driverid']
                dfname=request.form['dfname']
                dlname=request.form['dlname']
                dvno=request.form['dvno']
                dvname=request.form['dvname']
                duplicate=duplicate_driver(dfname,dlname,dvno)
                if duplicate==True:
                    return render_template('insert.html')
                cur.execute("insert into DRIVERS(First_Name,Last_Name,Vehicle_No,Vehicle) values(%s,%s,%s,%s)",(dfname,dlname,dvno,dvname))
                con.commit()
                return redirect('/adminPage')
            if 'riderform' in request.form:
                #riderid=request.form['riderid']
                rfname=request.form['rfname']
                rlname=request.form['rlname']
                contact=request.form['contact']
                duplicate=duplicate_rider(contact)
                if duplicate==True:
                    return render_template('insert.html')
                cur.execute("insert into RIDERS(First_Name,Last_Name,Contact) values(%s,%s,%s)",(rfname,rlname,contact))
                con.commit()
                return redirect('/adminPage')
            if 'vform' in request.form:
                vname=request.form['vname']
                vtype=request.form['vtype']
                make=request.form['make']
                cur.execute("insert into VEHICLE values(%s,%s,%s)",(vname,vtype,make))
                con.commit()
                return redirect('/adminPage')
            if 'crideform' in request.form:
                crideid=request.form['crideid']
                criderid=request.form['criderid']
                cdriverid=request.form['cdriverid']
                reason=request.form['reason']
                if duplicate==True:
                    return render_template('insert.html')
                cur.execute("insert into CANCELLED values(%s,%s,%s,%s)",(crideid,criderid,cdriverid,reason))
                con.commit()
                return redirect('/adminPage')
        return render_template('insert.html')
    return render_template('login.html')
def duplicate_ride(start,end):
    con = mysql.connection
    duplicate = False
    cur = con.cursor()
    cur.execute('select DateTime_start,DateTime_end from RIDES')
    rows = cur.fetchall()
    for row in rows:
        rs = str(row[0])
        re = str(row[1])
        if(rs==start and re==end):
            duplicate = True
            break
    return duplicate
def duplicate_driver(fname,lname,vno):
    con = mysql.connection
    duplicate = False
    cur = con.cursor()
    cur.execute('select First_Name,Last_Name,Vehicle_No from DRIVERS')
    rows = cur.fetchall()
    for row in rows:
        f = str(row[0])
        l = str(row[1])
        vn = str(row[2])
        if (f==fname and l==lname) or vn==vno:
            duplicate = True
            break
    return duplicate
def duplicate_rider(contact):
    con = mysql.connection
    duplicate = False
    cur = con.cursor()
    cur.execute('select Contact from RIDERS')
    rows = cur.fetchall()
    for row in rows:
        cno = str(row[0])
        if cno==contact:
            duplicate = True
            break
    return duplicate

@app.route('/delete',methods=['GET','POST'])
def delete():
    if session['contact']==acontact:
        con=mysql.connection
        cur=con.cursor()
        if(request.method=='POST'):
            if 'dcrideform' in request.form:
                crideid=request.form['crideid']
                cur.execute('delete from CANCELLED_RIDES where RideId=%s',(crideid))
                return redirect('/adminPage')
            if 'drideform' in request.form:
                rideid=request.form['rideid']
                cur.execute('delete from RIDES where RideId=%s',(rideid))
                return redirect('/adminPage')
            if 'ddriverform' in request.form:
                driverid=request.form['driverid']
                cur.execute('delete from DRIVERS where DriverId=%s',(driverid))
                return redirect('/adminPage')
            if 'driderform' in request.form:
                riderid=request.form['riderid']
                cur.execute('delete from RIDERS where RiderId=%s',(riderid))
                con.commit()
                return redirect('/adminPage')
            if 'dvform' in request.form:
                vname=request.form['vname']
                cur.execute('delete from VEHICLE where Vehicle_Name=%s',(vname))
                return redirect('/adminPage')
        return render_template('delete.html')
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
