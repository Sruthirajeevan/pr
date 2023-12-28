from flask import Flask,render_template,request,session,redirect,url_for
import mysql.connector

conn = mysql.connector.connect(host='localhost',user='root',password='root',database='task_managementsystem')
mycursor=conn.cursor()
#create the flask application
app = Flask(__name__)
app.secret_key="xyzsdfg"
#define a route and corresponding view
@app.route('/')
def hello():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login1.html')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/emp_home',methods=['GET','POST'])
def emp_home():
    if request.method=='POST':
        username=request.form['username']
        pwd=request.form['password']
        mycursor.execute(f"select username,password from user_register where username='{username}'")
         
        data=mycursor.fetchone()
        conn.commit()
        if data and pwd==data[1]:

            session['username']=data[0]
            return render_template('home.html')
    
    
        else:
            return render_template('login1.html',msg="invalid username password")
    return render_template('login1.html')
@app.route('/logout')
def logout():
    session.pop("username",None) 
    return render_template("index.html")   
        
    
        


    


@app.route('/register')
def register():
    return render_template('register.html') 
@app.route('/register',methods=['GET','POST'])
def registeruser():

    
    user_id=request.form['user_id']
    user_fname=request.form['user_fname']
    user_lname=request.form['user_lname']
    age=request.form['age'] 
    place=request.form['place']
    user_email=request.form['user_email']
    username=request.form['username']
    password=request.form['password']
    query="insert into user_register values(%s,%s,%s,%s,%s,%s,%s,%s)"
    data=(user_id,user_fname,user_lname,age,place,user_email,username,password)
    mycursor.execute(query,data)
    conn.commit()
    
    return render_template('register.html')

        
        

    
   
@app.route('/view',methods=['GET','POST'])
def view():
    user_id=session['username']
        
    mycursor.execute(f"SELECT task_id,project_name,category,description,start_date,deadline_date,status from adduser_task where user_id='{user_id}'")
                     
         
    data=mycursor.fetchall()

    if not data:
        message="no data found"
        return render_template('home.html',msg=message)
    
    
    else:
        return render_template('view.html',sqldata=data)
    



    
@app.route('/delete/<int:task_id>' ,methods=['get','post'])


def delete(task_id):
    
    
   
    mycursor.execute(f"delete from adduser_task where task_id='{task_id}'")
    
    conn.commit()
    return redirect(url_for('home'))
        
#run flask application

@app.route('/update')
def update():
    return render_template('update.html') 
@app.route('/update_task/<int:id>',methods=['get','post'])
def update_task(id):
    mycursor.execute(f"select * from adduser_task where task_id='{id}'")
    data=mycursor.fetchone()
    conn.commit()
    return render_template('update.html',update_data=data)  
   
@app.route('/update_task1/<int:id>' ,methods=['get','post'])


def update_task1(id):
    
    user_id=session['username']
    project_name=request.form['project_name']
    category=request.form['category']
    description=request.form['description']  
    start_date=request.form['start_date']                       
    deadline_date=request.form['deadline_date']
    status=request.form['status']
    

   
   
    mycursor.execute(f"update adduser_task set  project_name='{project_name}',category='{category}',description='{description}',start_date='{start_date}',deadline_date='{deadline_date}',status='{status}' where task_id='{id}' and  user_id='{user_id}'")
    
    
    data=conn.commit()
    return redirect(url_for('home'))
   
     



@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/searchresult',methods=['GET','POST'])
def searchresult():
    
    status=request.form['status']
    user_id=session['username']
    mycursor.execute(f"select * from adduser_task where status='{status}' and  user_id='{user_id}'")
    data=mycursor.fetchall()
    
    if not data:
        return render_template('search.html',msg='data not found')
    else:
         return render_template('view.html',sqldata=data)
@app.route('/add')
def add():
    return render_template('add.html')
@app.route('/addtask',methods=['GET','POST'])
def addtask(): 
    task_id=request.form['task_id']
    
    project_name=request.form['project_name'] 
    category=request.form['category'] 
    description=request.form['description']
    start_date=request.form['start_date']
    deadline_date=request.form['deadline_date']
    status=request.form['status']
    user_id=session['username']
    query="insert into adduser_task values(%s,%s,%s,%s,%s,%s,%s,%s)"
    data=(task_id,project_name,category,description,start_date,deadline_date,status,user_id)
    mycursor.execute(query,data)
    conn.commit()
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')



   



if __name__=='__main__':
    app.run(debug=True)