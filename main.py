from flask import Flask, render_template, request, url_for, redirect, session
from bs4 import BeautifulSoup
import requests
from flask_mysqldb import MySQL
import MySQLdb.cursors

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
           "Accept-Encoding": "gzip, deflate",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
           "Connection": "close", "Upgrade-Insecure-Requests": "1"}

web = Flask(__name__)

web.secret_key = 'Prabhat'

web.config['MYSQL_USER'] = 'root'
web.config['MYSQL_PASSWORD'] = ''
web.config['MYSQL_DB'] = 'movies2watch'
web.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(web)

@web.route('/')
def Home():

    def Output():
        output = []
        mname = []
        names = []
        mimg = []
        mdesc = []

        msource = "https://www.metacritic.com/browse/movies/score/metascore/all/filtered?sort=desc"
        mreq = requests.get(msource, headers=headers)
        msoup = BeautifulSoup(mreq.content, features="lxml")

        for img in msoup.findAll('img'):
            mname.append(img.get('src'))


        for i in msoup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in msoup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i,j,k in zip(mimg,names,mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        # print(output)
        return output
    output = Output()

    if 'LoggedIn' in session:
        sess = session['Id']
        sess = str(sess)
        cur = mysql.connection.cursor()
        cur.execute("SELECT Genre FROM fav WHERE Id = '" + sess + "'")
        gdata = cur.fetchone()

        def Genre():
            out = []
            ageggen = []
            gimg = []
            gname = []
            name = []
            gdesc = []

            # g = str(gdata)
            if gdata == None:
                AgeGroup = session['AgeGroup']

                cur.execute("SELECT Id FROM users WHERE AgeGroup='" + AgeGroup + "'")
                Idlist = cur.fetchall()

                a = []

                for i in Idlist:
                    for j in i:
                        a.append(j)

                k = str(a)

                cur.execute("SELECT Genre FROM fav WHERE Id IN "+ k.replace("[","(").replace("]",")") + "")
                Gen = cur.fetchall()

                Agegen = []

                for i in Gen:
                    for j in i:
                        Agegen.append(j)

                agegenre = max(Agegen, key=Agegen.count)
                print(agegenre)

                age = agegenre.lower()
                link = "https://www.metacritic.com/browse/movies/genre/metascore/"+age+"?view=detailed"
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, features="lxml")

                for img in soup.findAll('img'):
                    gname.append(img.get('src'))
                # print(gname)

                for i in soup.find_all('a', class_="title"):
                    string = i.text
                    name.append(string.strip())
                # print(name)

                gname1 = gname[29:]
                for j in (gname1):
                    if j == '/images/icons/mc-mustsee-sm.svg':
                        pass
                    else:
                        gimg.append(j)
                # print(gimg)

                for i in soup.find_all('div', class_="summary"):
                    string = i.text
                    gdesc.append(string.strip())
                # print(gdesc)

                for i, j, k in zip(gimg, name, gdesc):
                    ageggen.append(i)
                    ageggen.append(j)
                    ageggen.append(k)
                print(ageggen)
                return ageggen

            else:
                g = gdata[0]
                genre = g.lower()
                link = "https://www.metacritic.com/browse/movies/genre/metascore/"+genre+"?view=detailed"
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, features="lxml")

                for img in soup.findAll('img'):
                    gname.append(img.get('src'))
                # print(gname)

                for i in soup.find_all('a', class_="title"):
                    string = i.text
                    name.append(string.strip())
                # print(name)

                gname1 = gname[29:]
                for j in (gname1):
                    if j == '/images/icons/mc-mustsee-sm.svg':
                        pass
                    else:
                        gimg.append(j)
                # print(gimg)

                for i in soup.find_all('div', class_="summary"):
                    string = i.text
                    gdesc.append(string.strip())
                # print(gdesc)

                for i, j, k in zip(gimg, name, gdesc):
                    out.append(i)
                    out.append(j)
                    out.append(k)
                print(out)
            return out

        out = Genre()
        agegen = Genre()

        if gdata == None:
            return render_template('Home.html', gdata = gdata, agegen = agegen)
        elif gdata:
            return render_template('Home.html', out = out)
        else:
            return render_template('Home.html', output = output)
    else:
        return render_template('Home.html', output = output)

    return render_template('Home.html')

@web.route('/SortMovie', methods=['POST', 'GET'])
def SortMovie():
    if 'LoggedIn' in session:
        sess = session['Id']
        sess = str(sess)
        cur = mysql.connection.cursor()
        cur.execute("SELECT Genre FROM fav WHERE Id = '" + sess + "'")
        gdata = cur.fetchone()

        if request.method == 'POST':
            srtname = request.form['customRadio']

        def Genre():
            out = []
            gimg = []
            gname = []
            name = []
            gdesc = []

            # g = str(gdata)
            if gdata == None:
                pass
            else:
                g = gdata[0]
                genre = g.lower()
                link = "https://www.metacritic.com/browse/movies/genre/"+ srtname +"/" + genre + "?view=detailed"
                req = requests.get(link, headers=headers)
                soup = BeautifulSoup(req.content, features="lxml")

                for img in soup.findAll('img'):
                    gname.append(img.get('src'))
                # print(gname)

                for i in soup.find_all('a', class_="title"):
                    string = i.text
                    name.append(string.strip())
                # print(name)

                gname1 = gname[30:]
                for j in (gname1):
                    if j == '/images/icons/mc-mustsee-sm.svg':
                        pass
                    else:
                        gimg.append(j)
                # print(gimg)

                for i in soup.find_all('div', class_="summary"):
                    string = i.text
                    gdesc.append(string.strip())
                # print(gdesc)

                for i, j, k in zip(gimg, name, gdesc):
                    out.append(i)
                    out.append(j)
                    out.append(k)
                print(out)
            return out
        out = Genre()
    return render_template('SortMovie.html', out = out)

@web.route('/Genreform', methods=['POST', 'GET'])
def Genreform():
    if request.method == 'POST':
        if 'LoggedIn' in session:
            GenreData = request.form['customRadio']
            sess = session['Id']
            sess = str(sess)
            cur = mysql.connection.cursor()
            cur.execute("SELECT Genre FROM fav WHERE Id = '" + sess + "'")
            gdata = cur.fetchone()
            if gdata == None:
                cur.execute("INSERT INTO fav (Id, Genre) VALUES (%s, %s)", (sess, GenreData))
                mysql.connection.commit()
                return redirect(url_for('Home'))
            else:
                cur.execute("UPDATE fav SET Genre = '" + GenreData + "'WHERE Id = '" + sess + "'")
                mysql.connection.commit()
                return redirect(url_for('Home'))
    return redirect(url_for('Home'))

@web.route('/Register', methods=['POST', 'GET'])
def Register():
    if request.method == 'POST':
        Fname = request.form['RegisterInputFirstName']
        Lname = request.form['RegisterInputLastName']
        Email = request.form['RegisterInputEmail']
        Paswd = request.form['RegisterInputPassword']
        Phone = request.form['RegisterInputPhoneNo']
        AgeGroup = request.form['AgeGroup']

        cur = mysql.connection.cursor()
        cur.execute("SELECT Email FROM USERS WHERE Email ='" + Email + "'")
        Email_Exist = cur.fetchone()

        cur.execute("SELECT Phone FROM USERS WHERE Phone ='" + Phone + "'")
        Phone_Exist = cur.fetchone()

        if Email_Exist:
            ErMessage = 'User Already Exist!!'
            return render_template('Register.html', ErMessage = ErMessage)
        elif Phone_Exist:
            ErMessage = 'Phone No. Already Exist!!'
            return render_template('Register.html', ErMessage = ErMessage)
        else:
            cur.execute("INSERT INTO USERS (Fname, Lname, Email, Paswd, Phone, AgeGroup) VALUES (%s, %s, %s, %s, %s, %s)", (Fname, Lname, Email, Paswd, Phone, AgeGroup))
            mysql.connection.commit()
            return render_template('Login.html')

    return render_template('Register.html')

@web.route('/Login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        Email = request.form['LoginInputEmail']
        Paswd = request.form['LoginInputPassword']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM USERS WHERE Email = '" + Email + "' AND Paswd = '" + Paswd + "'")
        AccDetails = cur.fetchone()

        if AccDetails:
            session['LoggedIn'] = True
            session['Id'] = AccDetails['Id']
            session['Fname'] = AccDetails['Fname']
            session['Lname'] = AccDetails['Lname']
            session['Email'] = AccDetails['Email']
            session['Phone'] = AccDetails['Phone']
            session['AgeGroup'] = AccDetails['AgeGroup']
            return redirect(url_for('Home'))
        else:
            ErMessage = 'Email Id or Password Invalid!!'
            return render_template('Login.html', ErMessage = ErMessage)

    return render_template('Login.html')

@web.route('/Logout')
def Logout():
    session.pop('LoggedIn', None)
    session.pop('Id', None)
    session.pop('Fname', None)
    session.pop('Lname', None)
    session.pop('Email', None)
    session.pop('Phone', None)
    return redirect(url_for('Home'))

@web.route('/NewPassword')
def NewPassword():
    return render_template('NewPassword.html')

@web.route('/UpdatePassword', methods=['POST', 'GET'])
def UpdatePassword():
    if request.method == 'POST':
        Email = request.form['NewPasswordInputEmail']
        Phone = request.form['NewPasswordInputPhoneNo']
        NewPaswd = request.form['NewPasswordInputPassword']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE USERS SET Paswd='" + NewPaswd + "' WHERE Email ='" + Email + "' OR Phone ='" + Phone + "'")
        mysql.connection.commit()

        ErMessage = "Your Password has successfully Changed. Now you can go Back and Login"

        return render_template('NewPassword.html', ErMessage = ErMessage)

    return render_template('NewPassword.html')

@web.route('/DeleteAccount/<string:Id>', methods=['POST', 'GET'])
def DeleteAccount(Id):
    if request.method == 'POST':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("DELETE FROM USERS WHERE Id = {0}".format(Id))
        mysql.connection.commit()

        return redirect(url_for('Logout'))

@web.route('/HelpMessage/<string:Id>', methods=['POST', 'GET'])
def HelpMessage(Id):
    if request.method == 'POST':
        Message = request.form['MsgTextarea']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE USERS SET Message ='" + Message + "' WHERE Id = {0}".format(Id))
        mysql.connection.commit()

        disp_msg = "Sorry for the problem you have faced. We have received your issue and try to solve as soon as possible... ✍(◔◡◔)"

        return render_template('Profile.html', disp_msg = disp_msg)

@web.route('/Profile')
def Profile():
    if 'LoggedIn' in session:
        sess = session['Id']
        sess = str(sess)
        cur = mysql.connection.cursor()
        cur.execute("SELECT Genre FROM fav WHERE Id = '" + sess + "'")
        gdata = cur.fetchone()
        if gdata == None:
            pass
        else:
            g = gdata[0]
            print(gdata)
            return render_template('Profile.html', gdata = g)
    return render_template('Profile.html')

@web.route('/MSearch',methods=['POST','GET'])
def MSearch():
    if request.method == 'POST':
        search = request.form['Search']
        s = search.replace(' ','%20')
        print(s)
        out = []
        sname = []
        names = []
        simg = []
        sdesc = []

        ssource = "https://www.metacritic.com/search/movie/"+s+"/results"
        sreq = requests.get(ssource, headers = headers)
        ssoup = BeautifulSoup(sreq.content, features = "lxml")


        for img in ssoup.findAll('img'):
            sname.append(img.get('alt'))

        for i in sname[28:]:
            if i != None:
                names.append(i[:-9])
            else:
                pass
        # print(names)

        ssimg = []
        seimg =[]
        for img in ssoup.findAll('img'):
            simg.append(img.get('src'))
        # for i in simg:
        #     # print(i)
        for j in simg:
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                ssimg.append(j)
        for i in ssimg[27:]:
            seimg.append(i)
        # print(seimg)

        for i in ssoup.find_all('p', class_="deck basic_stat"):
            string = i.text
            sdesc.append(string.strip())
        # print(sdesc)

        for i, j, k in zip(seimg, names, sdesc):
            out.append(i)
            out.append(j)
            out.append(k)
        print(out)

        return render_template("Search.html", out = out)

    return render_template("Search.html")

@web.route('/Genre')
def Genre():
    return render_template("Genre.html")

@web.route('/Sad', methods=['POST', 'GET'])
def Sad():

    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/comedy?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Sad.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/comedy?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Sad.html", output=output)
    return render_template("Sad.html")

@web.route('/Anger', methods=['POST', 'GET'])
def Anger():
    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/sci-fi?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Anger.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/sci-fi?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Anger.html", output=output)
    return render_template("Anger.html")

@web.route('/Disgust', methods=['POST', 'GET'])
def Disgust():
    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/drama?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Disgust.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/drama?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Disgust.html", output=output)
    return render_template("Disgust.html")

@web.route('/Horror', methods=['POST', 'GET'])
def Horror():
    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/horror?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Horror.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/horror?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Horror.html", output=output)
    return render_template("Horror.html")

@web.route('/Excitement', methods=['POST', 'GET'])
def Excitement():
    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/action?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Excitement.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/action?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Excitement.html", output=output)
    return render_template("Excitement.html")

@web.route('/Romantic', methods=['POST', 'GET'])
def Romantic():
    if request.method == 'POST':
        srtname = request.form['customRadio']
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/"+srtname+"/romance?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Romantic.html", output = output)
    else:
        output = []
        mimg = []
        mname = []
        names = []
        mdesc = []

        link = "https://www.metacritic.com/browse/movies/genre/metascore/romance?view=detailed"
        req = requests.get(link, headers=headers)
        soup = BeautifulSoup(req.content, features="lxml")

        for img in soup.findAll('img'):
            mname.append(img.get('src'))

        for i in soup.find_all('a', class_="title"):
            string = i.text
            names.append(string.strip())
        # print(names)

        mname1 = mname[30:]
        for j in (mname1):
            if j == '/images/icons/mc-mustsee-sm.svg':
                pass
            else:
                mimg.append(j)
        # print(mimg)

        for i in soup.find_all('div', class_="summary"):
            string = i.text
            mdesc.append(string.strip())
        # print(mdesc)

        for i, j, k in zip(mimg, names, mdesc):
            output.append(i)
            output.append(j)
            output.append(k)
        print(output)
        return render_template("Romantic.html", output=output)
    return render_template("Romantic.html")


if __name__ == '__main__':
    web.run(debug=True)
