from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


# Render the homepage for the root directory
@app.route('/')
def home():
    return render_template('index.html')


# Renders the addReview html
@app.route('/addReview')
def new_student():
    return render_template('addReview.html')


# When form at addReview submited
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            # Organize all the inputs from the forms
            nm = request.form['Name']
            rst = request.form['Restaurant']
            fd = request.form['Food']
            srv = request.form['Service']
            amb = request.form['Ambience']
            prc = request.form['Price']
            ovr = request.form['Overall']
            rvw = request.form['Review']

            with sql.connect("reviewData.db") as con:
                cur = con.cursor()
                # Insert data from the forms into their respective tables
                cur.execute("INSERT INTO Reviews (Username,Restaurant,ReviewTime,Rating,Review) VALUES (?,?,datetime('now','localtime'),?,?)", (nm, rst, ovr, rvw))
                cur.execute("INSERT INTO Ratings (Restaurant,Food,Service,Ambience,Price,Overall) VALUES (?,?,?,?,?,?)", (rst, fd, srv, amb, prc, ovr))

                con.commit()
        except:
            con.rollback()

        finally:
            return render_template("addReview.html")
            con.close()


# Renders getReviews html
@app.route('/getReviews')
def getReviews():
    return render_template('getReviews.html')


# When form submitted at getReviews
@app.route('/getrv', methods=['POST', 'GET'])
def getrv():
    if request.method == 'POST':
        # Receive information of the form and sends it to showReview
        rst = request.form['Restaurant']
        return showReviews(rst)


# Renders showReviews html with the data selected from the form
@app.route('/showReviews')
def showReviews(rest):
    con = sql.connect("reviewData.db")
    con.row_factory = sql.Row

    value = "select * from Reviews where Restaurant='" + rest + "'"

    cur = con.cursor()
    cur.execute(value)

    rows = cur.fetchall()
    return render_template("showReviews.html", rows=rows, rest=rest)


# Renders showReport html with the top 10 restaurants
@app.route('/showReport')
def showReport():
    con = sql.connect("reviewData.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    # Groups them by the restaurant name, then takes the average of all their categories rounded by 1 decimal and
    # are first ordered by their overall rating and then alphabetically, limited to the top 10
    cur.execute("select Restaurant, ROUND(avg(Food), 1), ROUND(avg(Service), 1), ROUND(avg(Ambience), 1), ROUND(avg(Price), 1), ROUND(avg(Overall), 1) from Ratings Group By Restaurant Order By avg(Overall) DESC, Restaurant ASC LIMIT 10")

    rows = cur.fetchall()
    return render_template("showReport.html", rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
