from flask import Flask, render_template, redirect, request, url_for, abort, session,json
import datetime

app = Flask(__name__)
app.secret_key = "this place will be random"
#add ckeditor

#Sessionla ilgili doğrulamayı yapıyoruz
def get_current_username():
    username = " "
    login_auth = False
    if "username" in session:
        username = session["username"]
        login_auth = True
    return username, login_auth

def id_creater():
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        data_sum = len(read_data["topic"])+1
        return data_sum

@app.route("/post/<url>")
def post_devami(url):
    sayac = -1
    username, login_auth = get_current_username()
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        text_data = read_data["topic"]
        img = "<a src='static/img_1.jpg'>b</a>"
        for i in range(len(read_data["topic"])):
            sayac += 1
            post = text_data[sayac][0]["title"]["text"]
            title = text_data[sayac][0]["title"]["title"].replace(' ','-')
            title_real = text_data[sayac][0]["title"]["title"]
            if title == url:
                deney=title.replace(' ','-')
                print(deney)
                return render_template("post_view.html",img=img, post=post,title=title_real, username=username, login_auth=login_auth,deney=deney)


@app.route('/login', methods=["POST", "GET"])
def login():  # put application's code here
    if request.method == "POST":
        if request.form:
            if "username" in request.form and "password" in request.form:
                username = request.form["username"]
                password = request.form["password"]
                if username == "Berkehan_Göktürk" and password == "ABC123":
                    session["username"] = username
                    return redirect(url_for("home"))
                elif username =="Batuhan Unal" and password=="abc123":
                    session["username"] = username
                    return redirect(url_for("home"))
                elif username =="İsmail Bilici" and password=="abc123":
                    session["username"] = username
                    return redirect(url_for("home"))
                elif username == "Recep Üçes" and password == "abc123":
                    session["username"] = username
                    return redirect(url_for("home"))

                else:
                    return redirect(url_for("login"))
        abort(400)
    username, login_auth = get_current_username()
    return render_template("login.html", username=username, login_auth=login_auth)


@app.route('/')
def home():
    username, login_auth = get_current_username()
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        sayac = -1
        href = "http://127.0.0.1:5000/"
        data_sum = len(read_data["topic"])
        print(data_sum)
        title_data = (read_data["topic"][sayac][0]["title"]["title"])
        text_data = read_data["topic"]

    return render_template("home.html", username=username, login_auth=login_auth, title_data=title_data,
                           text_data=text_data, data_sum=data_sum,href=href)


@app.route('/contact')
def contact():
    username, login_auth = get_current_username()

    return render_template("contact.html", username=username, login_auth=login_auth)


@app.route('/about')
def about():
    username, login_auth = get_current_username()

    return render_template("about.html", username=username, login_auth=login_auth)


@app.route('/logout')
def logout():
    if "username" in session:
        del session["username"]
    return redirect(url_for("home"))


@app.route('/Software')
def deneme():
    username, login_auth = get_current_username()
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        text_data = read_data["topic"]
        data_sum = len(read_data["topic"])

        b = []
        sayac = -1

        for x in range(data_sum):
            sayac +=1
            if text_data[x][0]["title"]["category"] =="Software":

                c = len(b)
                b.append(x)
                # print(x)
                # print(data_sum)
                # print(sayac)
                # print(c)
                # print(b[c])
                # print(text_data[b[c]][0]["title"]["text"])

        d = c+1
        #print(b)
        #print(len(b))

    return render_template("Software.html", username=username, login_auth=login_auth,text_data=text_data,data_sum=data_sum,b=b,d=d)
@app.route('/admin_advice')
def admin_advice():
    username, login_auth = get_current_username()
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        text_data = read_data["topic"]
        data_sum = len(read_data["topic"])

        b = []
        sayac = -1

        for x in range(data_sum):
            sayac +=1
            if text_data[x][0]["title"]["category"] =="Admin_advice":

                c = len(b)
                b.append(x)
                # print(x)
                # print(data_sum)
                # print(sayac)
                # print(c)
                # print(b[c])
                # print(text_data[b[c]][0]["title"]["text"])

        d = c+1
        #print(b)
        #print(len(b))

    return render_template("admin_advice.html", username=username, login_auth=login_auth,text_data=text_data,data_sum=data_sum,b=b,d=d)



@app.route('/posts', methods=["GET", "POST"])
def posts():
    username, login_auth = get_current_username()
    if request.method == "POST":
        try:
            if session["username"] == username:
                title = request.form["title"]
                category = request.form["category_id"]
                text = request.form["text-alani"]

                if len(title) < 2 and len(text) < 4:
                    return "hata "

                else:
                    an = datetime.datetime.now()
                    paylasma_tarihi = datetime.datetime.ctime(an)
                    new_data = [{"title": {
                        "id":id_creater(),
                        "author": session["username"],
                        "title": title,
                        "category": category,
                        "text": text,
                        "time": paylasma_tarihi}}]

                    with open('package.json', 'r+') as json_yaz:
                        file_data = json.load(json_yaz)
                        file_data["topic"].insert(0,new_data)
                        json_yaz.seek(0)
                        json.dump(file_data, json_yaz, ensure_ascii=False, indent=6)

        except KeyError:
            return redirect(url_for("login"))

    return render_template("posts.html", username=username, login_auth=login_auth)

@app.route('/admin-page')
def admin_page():
    username, login_auth = get_current_username()
    with open("package.json", "r") as json_read:
        read_data = json.load(json_read)
        sayac = -1
        data_sum = len(read_data["topic"])
        print(data_sum)
        title_data = (read_data["topic"][sayac][0]["title"]["title"])
        text_data = read_data["topic"]

    return render_template("admin-page.html", username=username, login_auth=login_auth, title_data=title_data,
                           text_data=text_data, data_sum=data_sum)

def admin_page_delete():
    if request.method =="POST":
        a = request.form['{{  text_data[x][0]["title"]["id"] }}']
        print(a)
        with open("package.json", "r+") as json_delete:
            delete_data = json.load(json_delete)
            delete_data["topic"].seek(0)
            sayac = -1

            data_sum = len(delete_data["topic"])
            print(data_sum)
            title_data = (delete_data["topic"][sayac][0]["title"]["title"])
            text_data = delete_data["topic"]
def admin_page_edit():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return "Sayfa yok", 404


if __name__ == '__main__':
    app.run(debug=True)
