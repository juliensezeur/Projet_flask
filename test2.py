from flask import Flask, request, redirect, url_for, render_template, session
import time
import mysql.connector

app = Flask(__name__)
app.secret_key = "ADMIN"

db = mysql.connector.connect(
        user='julien-sezeur_1',
        password='Ty;!509hyr',
        database='julien-sezeur_test',
        host='mysql-julien-sezeur.alwaysdata.net'
    )
@app.route("/", methods=["GET", "POST"])
def connexion():
    erreur = ""
    if request.method == "POST":
        username = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            erreur = "Merci de remplir tous les champs."
        else:
            ma_bdd = db.cursor()
            verif = f"SELECT `username`, `password` FROM `user` WHERE username = '{username}'"
            ma_bdd.execute(verif)
            verif = ma_bdd.fetchall()
            if verif == []:
                erreur = "Identifiants invalides."
            else :
                if username == verif[0][0] and password == verif[0][1]:
                    erreur = "réussit"
                    session["username"] = verif[0][0]
                    return redirect(url_for("accueil"))
                else:
                    erreur = "Identifiants invalides."
    return render_template('connexion.html', erreur=erreur)

@app.route("/accueil", methods=["GET", "POST"])
def accueil():
    if "username" not in session:
        return redirect(url_for("connexion"))
    erreur_1 = ""
    erreur_2 = ""
    erreur_3 = ""
    username = session["username"]
    if request.method == "POST":
        appli_log = request.form.get("appli_log", "").strip()
        username_log = request.form.get("login_log", "").strip()
        ma_bdd = db.cursor()
        if not username_log or not appli_log:
            appli_add = request.form.get("appli_add", "").strip()
            username_add = request.form.get("login_add", "").strip()
            password_add = request.form.get("password_add", "")
            if not username_add or not password_add or not appli_add:
                appli_del = request.form.get("appli_del", "").strip()
                username_del = request.form.get("login_del", "").strip()
                if not username_del or not appli_del:
                    erreur_1 = "véuiller remplir convenablement tout les champs de une des 2 option"
                    erreur_2 = erreur_1
                    erreur_3 = erreur_1
                else :
                    suprimé = f"DELETE FROM `mot_de_passe_{username}` WHERE appli = '{appli_del}' AND login = '{username_del}'"
                    ma_bdd.execute(suprimé)
                    db.commit()
                    verif = f"SELECT `appli`, `login` FROM `mot_de_passe_{username}` WHERE login = '{username_del}' AND appli ='{appli_del}'"
                    ma_bdd.execute(verif)
                    verif = ma_bdd.fetchall()
                    if verif ==[]:
                        erreur_3 = "suppréssion réussit"
                    else :
                        erreur_3 = "échec de la supréssion"
            else:
                verif = f"SELECT `appli`, `login` FROM `mot_de_passe_{username}` WHERE login = '{username_add}' AND appli ='{appli_add}'"
                ma_bdd.execute(verif)
                verif = ma_bdd.fetchall()
                if verif == []:
                    insert = f"INSERT INTO `mot_de_passe_{username}`(`appli`, `login`, `password`) VALUES ('{appli_add}','{username_add}','{password_add}')"
                    ma_bdd.execute(insert)
                    db.commit()
                    verif = f"SELECT `appli`, `login`, `password` FROM `mot_de_passe_{username}` WHERE login = '{username_add}' AND appli ='{appli_add}'"
                    ma_bdd.execute(verif)
                    verif = ma_bdd.fetchall()
                    if appli_add == verif[0][0] and username_add == verif[0][1] and password_add == verif[0][2]:
                        erreur_2 = "inscription réussit"
                    else:
                        erreur_2 = "problème d'enregistrement"
                else:
                    erreur_2 = "un mot de passe est déja enregistrer pour cette appli et ce login"
        else:
            password = f"SELECT `password` FROM `mot_de_passe_{username}` WHERE login = '{username_log}' AND appli ='{appli_log}'"
            ma_bdd.execute(password)
            password = ma_bdd.fetchall()
            if password == []:
                erreur_1 = "pas de mot de passe enregistrer pour cette identifiant sur cette application"
            else:
                erreur_1 = password[0][0]
    return render_template("accueil.html", username = session["username"], erreur_1 = erreur_1, erreur_2 = erreur_2, erreur_3 = erreur_3)

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    erreur = ""
    if request.method == "POST":
        username = request.form.get("login", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            erreur = "Merci de remplir tous les champs."
        else:
            ma_bdd = db.cursor()
            verif = f"SELECT `username` FROM `user` WHERE username = '{username}'"
            ma_bdd.execute(verif)
            verif = ma_bdd.fetchall()
            if verif == []:
                insert = f"INSERT INTO `user` (`username`, `password`) VALUES ('{username}','{password}')"
                ma_bdd.execute(insert)
                db.commit()
                create = f"CREATE TABLE `mot_de_passe_{username}` (`id` int PRIMARY KEY NOT NULL AUTO_INCREMENT, `appli` text NOT NULL, `login` text NOT NULL, `password` text NOT NULL)"
                ma_bdd.execute(create)
                db.commit()
                verif = f"SELECT `username`, `password` FROM `user` WHERE username = '{username}'"
                ma_bdd.execute(verif)
                verif = ma_bdd.fetchall()
                if username == verif[0][0] and password == verif[0][1]:
                    erreur = "inscription réussit"
                    session["username"] = verif[0][0]
                    return redirect(url_for("accueil"))
                else:
                    erreur = "problème lors de l'inscription ou de la vérification d'inscription"
            else:
                erreur = "Identifiants déja prit, choisissez en un autre"
    return render_template("inscription.html", erreur=erreur)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("connexion"))

if __name__ == '__main__':
    app.run()