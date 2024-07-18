from flask import *
import random,base64,os,datetime
from flask_mysqldb import MySQL
import smtplib
from email.message import EmailMessage

ob=Flask(__name__)

ob.secret_key="fsdfegdsfgd$@&g2342342"

ob.config['MYSQL_USER']='root'
ob.config['MYSQL_PASSWORD']=''
ob.config['MYSQL_DB']='electroniXhub'

mysql=MySQL(ob)

@ob.route("/")
def index():
    return render_template('homepage.html')

@ob.route('/wishlist',methods=['POST','GET'] )
def wishlist():
    # error=''
    # if (request.args.get['show']):
    error=request.args.get('show')
    header="Confimation"
    mycur=mysql.connect.cursor()
    mycur.execute('select * from items')
    data=mycur.fetchall()
    products=[]
    if 'cart' in session:
        for item in data:
            for flag in session['cart']:
                if flag['sno']==item[0]:
                    products.append(item)
    return render_template("wishlist.html",products=products,error=error,header=header)


@ob.route('/category',methods=['GET'])
def product():
    n=request.args.get('category')
    mycur=mysql.connect.cursor()
    match n:
        case "mobile":
            mycur.execute('select * from items where category="Mobile"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case "smart tv":
            mycur.execute('select * from items where category="TV"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case "watch":
            mycur.execute('select * from items where category="Watch"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case "camera":
            mycur.execute('select * from items where category="camera"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case "laptop":
            mycur.execute('select * from items where category="laptop"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case "headphone":
            mycur.execute('select * from items where category="Headphone"')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        case _:
            mycur.execute('select * from items')
            data=mycur.fetchall()
            return render_template('product.html',data=data)
        
@ob.route('/addcart',methods=['POST'])
def addcart():
    mycur=mysql.connect.cursor()
    mycur.execute('select * from items')
    data=mycur.fetchall()

    sno=request.form.get('sno')
    flag=0
    for item in data:
        if int(sno)==item[0]:
            product={'sno':item[0],'qty':1}
    flag=0
    error=""
    header="Attention"
    if 'cart' in session:
        for item in session['cart']:
            if product['sno']==item['sno']:
                flag=1
                error="Already Added."
        
        if(flag==0):
                products=session['cart']
                products.append(product)
                session['cart']=products
                error="Added To Cart..."
    else:
        products=[]
        products.append(product)
        session['cart']=products
        error="Added To Cart..."
    
    return render_template('product.html',error=error,data=data,header=header)

@ob.route('/remove_from_cart',methods=['GET'])
def remove_from_cart():
    sno=request.args.get('sno')
    error=""
    header="Attention"
    if 'cart' in session:
        products=session['cart']
        for item in products:
            if sno == str(item['sno']):
                del products[products.index(item)]
                session['cart']=products
                error='removed from cart'
                return redirect('/wishlist?show=removed from cart')
    else:
        mycur=mysql.connect.cursor()
        mycur.execute('select * from items')
        data=mycur.fetchall()
        error="No Cart Added..."
        return render_template('product.html',data=data,header=header,error=error)

@ob.route('/doorder',methods=['POST'])
def doorder():
    sno=request.form.get('sno')
    sno=[sno]
    mycur=mysql.connect.cursor()
    mycur.execute('select * from items where sno=%s',sno)
    data=mycur.fetchall()
    if(data):
        session['order_data']={'name':data[0][1],'price':data[0][2],'qty':1}
        return render_template('info.html',data=data)
    
    else:
        return str("Server Down.....")


@ob.route('/doconfirm',methods=['POST'])
def confirm():
    sno=request.form.get('sno')
    name=request.form.get('name')
    email=request.form.get('email')
    num=request.form.get('num')
    address=request.form.get('address')
    city=request.form.get('city')
    state=request.form.get('state')
    pin=request.form.get('pin')
    random_number = str(random.randint(1000, 9999))
    current_datetime = datetime.datetime.now()
    info=[name,num,email,sno,random_number,current_datetime,address,city,state,pin]
    mycur=mysql.connect.cursor()
    mycur.execute('insert into orders(name,number,email,pro_no,product_otp,date,address,city,state,pin)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',info)
    error=name+" Your Order is Placed.The Product is Delivered within 7 days."
    msg="Hello "+name+"\n Thank You for using ElectroniX-hub...\n Your Product Otp is :"+random_number+"\nYour order is placed and delivered within 7 days.\nKeep Track Your product on official website of ElextroniX-hub"
    email_alert("ElectroniX-hub",msg,email)
    order_info=session['order_data']
    return render_template('reciept.html',info=info,order_info=order_info,error=error)


@ob.route('/login')
def login():
    if 'login' in session:
            error="Already Loged In"
            header="Confirmation"
            return render_template('homepage.html',error=error,header=header)
    return render_template('login.html')

@ob.route('/dologin',methods=['POST'])
def dologin():
    email=request.form.get('email')
    password=request.form.get('password')
    mail=[email]
    info=[email,password]
    mycur=mysql.connect.cursor()
    mycur.execute('select * from users where email=%s',mail)
    data=mycur.fetchall()
    if data:
        mycur.execute('select * from users where email=%s and password=%s',info)
        flag=mycur.fetchall()
        if flag:
            error="Loged in"
            header="Confirmation"
            session['login']=1
            session['user_id']=email
            session['user_nm']=flag[0][1]
            session['user_password']=password
            return render_template('homepage.html',error=error,header=header)
            
        else:
            error="Wrong Password"
            header="Error"
            return render_template('login.html',error=error,header=header)
    else:
        error="Email Not Found"
        header="Alert"
        return render_template('login.html',error=error,header=header)

@ob.route('/logout')
def logout():
    if 'login' in session:
        error="Loged out"
        header="Caution"
        del session['login']
        del session['user_id']
        del session['user_password']
    else:
        error="Already Loged out"
        header="Warning"
    return render_template('homepage.html',error=error,header=header)

@ob.route('/register')
def register():
    if 'login' in session:
            error="Already Loged In"
            header="Confirmation"
            return render_template('homepage.html',error=error,header=header)
    return render_template('signup.html')

@ob.route('/sendotp',methods=['POST'])
def sendotp():
    mail=request.form.get('mail')
    email=[mail]
    mycur=mysql.connect.cursor()
    mycur.execute('select * from users where email=%s',email)
    data=mycur.fetchall()
    if data:
        error="Your Account is already created"
        header="Warning"
        return render_template('login.html',error=error,header=header)
    else:
        random_number = str(random.randint(1000, 9999))
        email_alert("ElectroniX-hub","Your OTP : "+random_number,mail)
        return render_template('verify.html',random_number=random_number,email=mail)

@ob.route('/verify',methods=['POST'])
def verify():
    mail=request.form.get('email')
    num=request.form.get('random_number')
    otp=request.form.get('otp')
    if otp==str(num):
        return render_template('signup.html',email=mail,verified=1)
    else:
        msg="Please enter Correct otp"
        return render_template('verify.html',random_number=num,email=mail,msg=msg)

@ob.route('/doregister',methods=['POST'])
def doregister():
    info=request.form
    password=request.form.get('password')
    address1=request.form.get('address1')
    mail=[request.form.get('mail')]
    info1=[info['name'],info['number'],mail,password,info['address'],address1,info['city'],info['state'],info['pin'],info['alt_num']]
    mycur=mysql.connect.cursor()
    mycur.execute('select * from users where email=%s',mail)
    data=mycur.fetchall()
    if data:
        error="Your Account is already created"
        header="Warning"
        return render_template('homepage.html',error=error,header=header)
    else:    
        mycur.execute('insert into users(name,number,email,password,address,address1,city,state,pin,alternate_no) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',info1)
        error="Succesfully Registered and Loged in"
        header="Confirmation"
        email=info['mail']
        session['login']=1
        session['user_id']=info['mail']
        session['user_nm']=info['name']
        session['user_password']=password
        email_alert("ElectroniX-hub","You have Succesfully created your account on ElectroniX-hub.",email)
        return render_template('homepage.html',error=error,header=header)

@ob.route('/about')
def aboutus():
    return render_template('about.html')

@ob.route('/contact')
def contactus():
    return render_template('contact.html')

@ob.route('/account')
def account():
    if 'login' in session:
        user_id=[session['user_id']]
        user_info=[session['user_id'],session['user_password']]
        mycur=mysql.connect.cursor()
        mycur.execute('select * from users where email=%s and password=%s',user_info)
        user_data=mycur.fetchall()
        if user_data:
            mycur.execute('select * from orders where email=%s',user_id)
            user_orders=mycur.fetchall()
            if user_orders:
                product_no=[]
                for flag in user_orders:
                    product_no.append(flag[4])
                product_data=[]
                for flag in product_no:
                    temp=[flag]
                    mycur.execute('select name,price from items where sno=%s',temp)
                    product_data.append(list(mycur.fetchall()))
                order_info=[]
                for flag in user_orders:
                    li=[]
                    li.append(flag[5])
                    li.append(flag[6])
                    li.append(flag[11])
                    order_info.append(li)
                order_data=[x + y for x, y in zip(product_data,order_info)]
                return render_template('account.html',user_data=user_data,order_data=order_data)
            else:
                return render_template('account.html',user_data=user_data)
        else:
            return 'kuch to gadbad h daya!'
    else:
        error='Please Login first'
        return render_template('login.html',error=error)
    
@ob.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_base64 = data.get('image')
    image_data = base64.b64decode(image_base64)
    image_path = "static\\pic\\" + session['user_nm'] + ".jpg"
    try:
        with open(image_path, 'wb') as f:
            f.write(image_data)
    except Exception as e:
        return "Can't Save..."
    return jsonify({'message': 'Image received and saved successfully'})

   

@ob.route('/suggest',methods=["POST"])
def suggestion():
    query=request.form.get('suggestion')
    data=[query]
    mycur=mysql.connect.cursor()
    mycur.execute('insert into suggestion(suggestions) values(%s)',data)
    error='Thanks for your suggestion...'
    header="Thank You"
    return render_template('homepage.html',error=error,header=header)

@ob.route('/reciept')
def rec():
    return render_template("reciept.html")

# search bar

@ob.route('/search',methods=['POST'])
def search():
    ques=request.form.get('search')
    sen=ques.split()
    char=[]
    for flag in sen:
        char.append(flag[0])    
    query = "SELECT * FROM items WHERE category LIKE %s"
    mycur=mysql.connect.cursor()
    info=[]
    for item in char:
        data=[]
        mycur.execute(query, (item + '%',))
        data=mycur.fetchall()
        if data:
            info.append(data)
    if not info:
        error='Sorry,No Data Found Named : '+ques
        header="Warning"
        mycur.execute("select * from items")
        data=mycur.fetchall()
        return render_template('product.html',data=data,error=error,header=header)
    else:
        return render_template('searched.html',data=info)

def email_alert(subject,body,to):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['subject'] = subject
        msg['to'] = to

        user = "asuydv9433@gmail.com"
        msg['from'] = user
        password = "exypdawsevrwcnbg"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(user,password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        return str("Server Error...")

if __name__=='__main__':
    ob.run(debug=True,host="0.0.0.0",port=4525)

