from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# PoliceOfficer class
class PoliceOfficer:
    def __init__(self, badgeNumber, name, rank, contactNumber):
        self.badgeNumber = int(badgeNumber)
        self.name = name
        self.rank = rank
        self.contactNumber = contactNumber

# Data storage
policeOfficers = []


# ---------------- FILE HANDLING ----------------

def load_data():
    """Load data from police_records.txt"""
    policeOfficers.clear()
    try:
        with open("police_records.txt", "r") as file:
            for line in file:
                if line.strip():
                    badgeNumber, name, rank, contactNumber = line.strip().split(",")
                    policeOfficers.append(PoliceOfficer(badgeNumber, name, rank, contactNumber))
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No existing records found. A new file will be created.")


def save_data():
    """Save all officers to police_records.txt"""
    with open("police_records.txt", "w") as file:
        for officer in policeOfficers:
            file.write(f"{officer.badgeNumber},{officer.name},{officer.rank},{officer.contactNumber}\n")
    print("Data saved successfully.")


# ---------------- CRUD OPERATIONS ----------------

def find_officer(badgeNumber):
    for officer in policeOfficers:
        if officer.badgeNumber == int(badgeNumber):
            return officer
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['POST'])
def add():
    badgeNumber = request.form['badgeNumber']
    name = request.form['name']
    rank = request.form['rank']
    contactNumber = request.form['contactNumber']

    if find_officer(badgeNumber):
        return "Officer already exists with this badge number!"

    new_officer = PoliceOfficer(badgeNumber, name, rank, contactNumber)
    policeOfficers.append(new_officer)
    save_data()
    return redirect(url_for('index'))


@app.route('/search', methods=['POST'])
def search():
    badgeNumber = request.form['badgeNumber']
    officer = find_officer(badgeNumber)
    return render_template('result.html', officer=officer)


@app.route('/update', methods=['POST'])
def update():
    badgeNumber = request.form['badgeNumber']
    name = request.form['name']
    rank = request.form['rank']
    contactNumber = request.form['contactNumber']

    officer = find_officer(badgeNumber)
    if officer:
        officer.name = name
        officer.rank = rank
        officer.contactNumber = contactNumber
        save_data()
        return redirect(url_for('index'))
    else:
        return "Officer not found!"


@app.route('/delete', methods=['POST'])
def delete():
    badgeNumber = request.form['badgeNumber']
    officer = find_officer(badgeNumber)
    if officer:
        policeOfficers.remove(officer)
        save_data()
        return redirect(url_for('index'))
    else:
        return "Officer not found!"


@app.route('/list')
def list_all():
    return render_template('list.html', officers=policeOfficers)


if __name__ == '__main__':
    load_data()
    app.run(debug=True)
