from flask import Flask,render_template,request,url_for,redirect
import requests
from flask_sqlalchemy import SQLAlchemy


api_key = "82b89db7b606a9d2b46f5edfda00f555"
url = "http://data.fixer.io/api/latest?access_key=" + api_key
base_url ="https://api.github.com/users/"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/akyildiz\Desktop/MixFlaskApp/todo.db"
db = SQLAlchemy(app)


# TODO APP
class Todo(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    TITLE = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

@app.route("/",methods=["POST","GET"])
def main():
    todo = Todo.query.all()
    if request.method == "POST":

        # FIXERIO
        amoun = request.form.get("amount")
        if amoun != None:
            firstcurrency = request.form.get("firstCurrency") # USD
            secondcurrency = request.form.get("secondCurrency") # TRY
            amount = request.form.get("amount")

            response = requests.get(url)
            app.logger.info(response)
            infos = response.json()
            app.logger.info(infos)

            firstvalue = infos["rates"][firstcurrency] # 1.18582
            secondvalue = infos["rates"][secondcurrency] # 9.290177
            result = (secondvalue/firstvalue)*float(amount)

            currencyinfo = {
                "firstcurrency":firstcurrency,
                "secondcurrency":secondcurrency,
                "amount":amount,
                "result":result
            }   
            return render_template('main_index.html',info=currencyinfo,todo=todo)

        # TODO APP
        add = request.form.get("inp")
        if add != None:
            add = request.form.get("inp")
            newTodo = Todo(TITLE=add,complete=False)
            db.session.add(newTodo)
            db.session.commit()
            todo = Todo.query.all()
            return redirect(url_for('main'))

        # GITHUB
        user = request.form.get("githubname")
        if user != None:
            githubname = request.form.get("githubname")
            response = requests.get(base_url + githubname)
            repos = requests.get (base_url + githubname + "/repos")
            repos_info = repos.json()
            response_info = response.json()
            if "message" in response_info:
                return render_template ('main_index.html', error = "Kontrol ederek lütfen tekrar deneyiniz...",todo=todo)
            return render_template('main_index.html',user=response_info,repos=repos_info,todo=todo)
        else:
            return render_template('main_index.html',todo=todo)


    else:
        return render_template("main_index.html",todo=todo)


@app.route("/update/<string:id>")
def update_status(id):
    tod = Todo.query.filter_by(ID=id).first()
    """if tod.complete:
        tod.complete = False
    else: 
        tod.complete = True"""
    tod.complete = not tod.complete
    db.session.commit()
    return redirect(url_for('main'))
    
@app.route("/delete/<string:id>")
def delete_list(id):
    tod = Todo.query.filter_by(ID=id).first()
    db.session.delete(tod)
    db.session.commit()
    return redirect(url_for('main'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)


