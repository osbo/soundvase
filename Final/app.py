from flask import *
from flask_mysqldb import MySQL
import numpy as np
import soundfile as sf
from stl import mesh
import math
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy.fft import rfft,rfftfreq
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'mysql.2223.lakeside-cs.org'
app.config['MYSQL_USER'] = 'student2223'
app.config['MYSQL_PASSWORD'] = 'm545CS42223'
app.config['MYSQL_DB'] = '2223project_1'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.secret_key = "store name" #session variable

mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def makesoundvase(name, userid, filename, autofreq, definefreq, height, radius, layerheight, perrevolution, depth):
    if filename == "Blank":
        data, samplerate = sf.read("/Users/carlosborne/Downloads/Final/static/sounds/" + filename + ".wav")
    else:
        data, samplerate = sf.read("/Users/carlosborne/Downloads/Final/static/sounds/" + name + "_" + filename + ".wav")

    y = rfft(data/data.max()*32767)
    xf = rfftfreq(data.size, 1/samplerate)
    if autofreq:
        largest = 0
        largestfreq = 0
        for i in range(np.abs(y)[:10000].size):
            if np.abs(y)[i] > largest:
                largest = np.abs(y)[i]
                largestfreq = xf[i]
    else:
        largestfreq=definefreq

    resolution = samplerate/largestfreq
    angles = np.arange(0,height*2*math.pi,2*math.pi/resolution/perrevolution)
    sine= np.sin(angles)
    cosine = np.cos(angles)

    increment = samplerate/largestfreq/resolution
    waveincrement = samplerate/largestfreq
    texture = np.zeros(math.floor(height*perrevolution*resolution))
    appendi = 0
    for layer in range(height): #layer is integer layer of height
        #print("0."+str(layer))
        startindex = math.floor(layer*waveincrement)
        for section in range(perrevolution):
            for i in range(math.floor(resolution)):
                texture[appendi] = np.average(data[startindex+math.floor(i*increment):startindex+math.floor(i*increment+increment)])
                appendi = appendi + 1
    texture = texture*depth

    bigresolution = resolution*perrevolution

    vertices = np.zeros((math.floor(height*bigresolution)+2,3))
    appendi = 0
    for r in range(height):
        #print("1."+str(r))
        for c in range(math.floor(bigresolution)):
            vertices[appendi] = [sine[c]*(radius+texture[r*math.floor(bigresolution)+c]),cosine[c]*(radius+texture[r*math.floor(bigresolution)+c]),r*layerheight]
            appendi += 1
    vertices[appendi] = [0,0,0]
    appendi += 1
    vertices[appendi] = [0,0,height*layerheight-1]

    faces = np.zeros(((height-1)*((math.floor(bigresolution)-1)*2+2)+(math.floor(bigresolution)-1)*2+2,3), dtype=int)
    appendi = 0
    for r in range(height-1):
        #print("2."+str(r))
        for c in range(math.floor(bigresolution)-1):
            faces[appendi] = [r*math.floor(bigresolution)+c,r*math.floor(bigresolution)+c+1,(r+1)*math.floor(bigresolution)+c]
            appendi += 1
            faces[appendi] = [r*math.floor(bigresolution)+c+1,(r+1)*math.floor(bigresolution)+c,(r+1)*math.floor(bigresolution)+c+1]
            appendi += 1
        faces[appendi] = [(r+1)*math.floor(bigresolution)-1,r*math.floor(bigresolution),(r+2)*math.floor(bigresolution)-1]
        appendi += 1
        faces[appendi] = [r*math.floor(bigresolution),(r+2)*math.floor(bigresolution)-1,(r+1)*math.floor(bigresolution)]
        appendi += 1
    for c in range(math.floor(bigresolution)-1):
        faces[appendi] = [math.floor(bigresolution)*height,c,c+1]
        appendi += 1
        faces[appendi] = [math.floor(bigresolution)*height+1,(height-1)*math.floor(bigresolution)+c,(height-1)*math.floor(bigresolution)+c+1]
        appendi += 1
    faces[appendi] = [math.floor(bigresolution)*height,math.floor(bigresolution)-1,0]
    appendi += 1
    faces[appendi] = [math.floor(bigresolution)*height+1,height*math.floor(bigresolution)-1,(height-1)*math.floor(bigresolution)]

    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    plt.plot(xf[np.absolute(xf-0).argmin():np.absolute(xf-20000).argmin()],np.abs(y)[np.absolute(xf-0).argmin():np.absolute(xf-20000).argmin()])
    plt.savefig("/Users/carlosborne/Downloads/Final/static/fftbig/" + name + "_" + filename + ".png", transparent=False, bbox_inches='tight')
    plt.clf()
    plt.plot(xf[np.absolute(xf-0).argmin():np.absolute(xf-500).argmin()],np.abs(y)[np.absolute(xf-0).argmin():np.absolute(xf-500).argmin()]) #change 0 and 500 later
    plt.savefig("/Users/carlosborne/Downloads/Final/static/fftsmall/" + name + "_" + filename + ".png", transparent=False, bbox_inches='tight')
    plt.clf()
    plt.plot(texture) #maybe change so its the whole waveform
    plt.savefig("/Users/carlosborne/Downloads/Final/static/waveformbig/" + name + "_" + filename + ".png", transparent=False, bbox_inches='tight')
    plt.clf()
    plt.plot(texture[0:math.floor(resolution)]) #maybe change so its the whole waveform
    plt.savefig("/Users/carlosborne/Downloads/Final/static/waveformsmall/" + name + "_" + filename + ".png", transparent=False, bbox_inches='tight')
    plt.clf()

    cube.save("/Users/carlosborne/Downloads/Final/static/stls/" + name + "_" + filename + ".stl")
    cursor = mysql.connection.cursor()
    query = "SELECT 1 FROM `carlosborne_sculptures` WHERE `filename` = %s and `userid` = %s"
    queryVars = (filename, userid)
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    rows = cursor.fetchall()
    if len(rows) == 0:
        query = "INSERT INTO `carlosborne_sculptures`(`userid`, `filename`, `autofreq`, `frequency`, `height`, `radius`, `layerheight`, `perrevolution`, `depth`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s)"
        queryVars = (userid, filename, autofreq, largestfreq, height, radius, layerheight, perrevolution, depth)
    else:
        query = "UPDATE `carlosborne_sculptures` SET `autofreq`=%s,`frequency`=%s,`height`=%s,`radius`=%s,`layerheight`=%s,`perrevolution`=%s,`depth`=%s WHERE `filename` = %s AND `userid` = %s"
        queryVars = (autofreq, largestfreq, height, radius, layerheight, perrevolution, depth, filename, userid)
    cursor.execute(query, queryVars)
    mysql.connection.commit()

    return largestfreq

def getmembers(): #gets the names of all of the members in the database
    cursor = mysql.connection.cursor()
    query = 'SELECT `email` FROM `carlosborne_users`'
    cursor.execute(query)
    mysql.connection.commit()
    data = cursor.fetchall()
    return data

def getid(name): #gets the id of a certain user
    cursor = mysql.connection.cursor()
    query = 'SELECT `id` FROM `carlosborne_users` WHERE `email` = %s;'
    queryVars = (name, )
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    data = cursor.fetchall()
    return list(data[0].values())[0] #this returns the id itself, taken from the tuple

def getpassword(name): #gets the id and password of a certain user
    cursor = mysql.connection.cursor()
    query = 'SELECT `password` FROM `carlosborne_users` WHERE `email` = %s;'
    queryVars = (name, )
    cursor.execute(query, queryVars)
    mysql.connection.commit()
    data = cursor.fetchall()
    return list(data[0].values())[0] #this returns the password itself, taken from the tuple

def addmember(name, password): #adds a new member to the database, recording the time which the account was created for records and future use
    cursor = mysql.connection.cursor()
    query = 'INSERT INTO `carlosborne_users`(`email`, `password`) VALUES (%s,%s)'
    queryVars = (name, generate_password_hash(password), )
    cursor.execute(query, queryVars)
    mysql.connection.commit()

@app.route('/', methods=["GET","POST"]) #base page, redirected to and from post requests so takes get and post requests
def index():
    if request.method == "GET":
        return render_template('index.html.j2', title="Log In - Soundvase") #if get request, load base page, the title parameter goes to the head in the base jinja file
    elif "log in" in request.form.keys(): #if the button was pressed, log in will be in the form keys
        name = request.values.get("name") #get the name
        session['name'] = name #store as a session variable
        password = request.values.get("password") #get the password
        members = getmembers() #get the members
        if name == None or name == "":
            return render_template('wrongpassword.html.j2', title="Log In - Soundvase") #server validation, if no name go to wrong password
        if password == None or password == "":
            return render_template('wrongpassword.html.j2', title="Log In - Soundvase") #server validation, if no password go to wrong password
        elif {'email': name} in members: #if existing user
            userpassword = getpassword(name) #get id and password
            if check_password_hash(userpassword,password):
                session['filename'] = None
                return redirect('/home') #move on to the friends function
            else:
                return render_template('wrongpassword.html.j2', title="Log In - Soundvase") #wrong password? show the wrong password page
        else:
            addmember(name, password) #not existing user? make one with the provided password
            session['filename'] = None
            return redirect('/home') #move on to the friends function
    elif "guest" in request.form.keys():
        session['name'] = "Guest"
        session['filename'] = None
        return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == "GET": #if redirected to
        if 'name' in session: #if a name is in the system
            name = session['name'] #grab the user's name
            filename = session['filename']
            userid = getid(name) #get id
            if name == "Guest":
                rows = None
            else:
                cursor = mysql.connection.cursor()
                query = "SELECT `filename`, `autofreq`, `frequency`, `height`, `radius`, `layerheight`, `perrevolution`, `depth` FROM `carlosborne_sculptures` WHERE `userid` = %s;"
                queryVars = (userid, )
                cursor.execute(query, queryVars)
                mysql.connection.commit()
                rows = cursor.fetchall()
                if len(rows) == 0:
                    rows = None
            if filename == None:
                if rows == None:
                    session['filename'] = "Blank"
                    autofreq = ""
                    frequency = 100
                    height = 250
                    radius = 9.0
                    layerheight = 0.1
                    perrevolution = 3
                    depth = 12.0
                    frequency = makesoundvase(name, userid, "Blank", autofreq, frequency, height, radius, layerheight, perrevolution, depth)
                    #stltogltf(name,filename)
                    if name == "Guest":
                        session['autofreq'] = autofreq
                        session['frequency'] = frequency
                        session['height'] = height
                        session['radius'] = radius
                        session['layerheight'] = layerheight
                        session['perrevolution'] = perrevolution
                        session['depth'] = depth
                else:
                    session['filename'] = rows[len(rows)-1]['filename']
            else:
                if name == "Guest":
                    autofreq = session['autofreq']
                    if autofreq:
                        autofreq = " checked"
                    else:
                        autofreq = ""
                    frequency = session['frequency']
                    height = session['height']
                    radius = session['radius']
                    layerheight = session['layerheight']
                    perrevolution = session['perrevolution']
                    depth = session['depth']
            filename = session['filename']
            if rows != None:
                for row in rows:
                    if row['filename'] == filename:
                        break
                autofreq = row['autofreq']
                if autofreq:
                    autofreq = " checked"
                else:
                    autofreq = ""
                frequency = row['frequency']
                height = row['height']
                radius = row['radius']
                layerheight = row['layerheight']
                perrevolution = row['perrevolution']
                depth = row['depth']
            return render_template('home.html.j2', rows=rows, title="Home - Soundvase", name=name, filename=filename, autofreq=autofreq, frequency=frequency, height=height, radius=radius, layerheight=layerheight, perrevolution=perrevolution, depth=depth)
        else: #if the person just went to /friends immediately
            return redirect("/") #go home
    elif "makesoundvase" in request.form.keys():
        if 'name' in session:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(resquest.url)
            file = request.files['file']
            name = session['name'] #grab the user's name
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save("/Users/carlosborne/Downloads/Final/static/sounds/" + name + "_" + filename)
                filename = filename[:-4]
            else:
                filename = session['filename']
            userid = getid(name) #get id
            autofreq = request.values.get('autofreq')
            if autofreq == None:
                autofreq = False
            else:
                autofreq = True
            definefreq = float(request.values.get('frequency'))
            height = int(request.values.get('height'))
            radius = float(request.values.get('radius'))
            layerheight = float(request.values.get('layerheight'))
            perrevolution = int(request.values.get('perrevolution'))
            depth = float(request.values.get('depth'))
            if height != None and radius != None and layerheight != None and perrevolution != None and depth != None:
                frequency = makesoundvase(name, userid, filename, autofreq, definefreq, height, radius, layerheight, perrevolution, depth)
                session['filename'] = filename
                if name == "Guest":
                    session['autofreq'] = autofreq
                    session['frequency'] = frequency
                    session['height'] = height
                    session['radius'] = radius
                    session['layerheight'] = layerheight
                    session['perrevolution'] = perrevolution
                    session['depth'] = depth
            return redirect("/home")
        else: #if the person just went to /friends immediately
            return redirect("/") #go home
    elif "download" in request.form.keys():
        if 'name' in session:
            name = session['name'] #grab the user's name
            filename = session['filename']
            return send_file("/Users/carlosborne/Downloads/Final/static/stls/" + name + "_" + filename + ".stl", as_attachment=True)
        else: #if the person just went to /friends immediately
            return redirect("/") #go home
    elif "downloaddefaults" in request.form.keys():
        if 'name' in session:
            name = session['name'] #grab the user's name
            filename = session['filename']
            return send_file("/Users/carlosborne/Downloads/Final/static/sounds/default_sounds.zip", as_attachment=True)
        else: #if the person just went to /friends immediately
            return redirect("/") #go home
    elif "log out" in request.form.keys():
        if 'name' in session:
            return redirect("/logout") #redirect to log out function
        else: #if the person just went to /friends immediately
            return redirect("/") #go home
    elif "edit" in request.form.keys():
        if 'name' in session:
            session['filename'] = request.form.get("edit")
            return redirect("/home")
        else: #if the person just went to /friends immediately
            return redirect("/") #go home

@app.route('/logout', methods=['GET','POST']) #only redirected to
def logout():
    if session["name"] == "Guest":
        session.pop("autofreq")
        session.pop("frequency")
        session.pop("height")
        session.pop("radius")
        session.pop("layerheight")
        session.pop("perrevolution")
        session.pop("depth")
    session.pop("name", None) #remove the session variable
    session.pop("filename", None) #remove the session variable
    return render_template('logout.html.j2', title="Logging Out... - Soundvase", redirectlink="<meta http-equiv=\"Refresh\" content=\"0.5; url=.\"/>") #redirect home after half a second, in the meantime show a the logging out page