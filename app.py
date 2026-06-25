from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = "dev_key_change_this_later"

USER_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

registered_users = load_users()

TRAITS = ["analytical", "creative", "social", "leadership", "technical", "business"]

SCORE_MAP = {
    "q1_a": {"analytical": 2, "technical": 1},
    "q1_b": {"creative": 2},
    "q1_c": {"social": 2},
    "q1_d": {"leadership": 2, "business": 1},
    "q1_e": {"technical": 2},

    "q2_a": {"analytical": 2},
    "q2_b": {"creative": 2},
    "q2_c": {"social": 2},
    "q2_d": {"technical": 2},
    "q2_e": {"creative": 1, "technical": 1},

    "q3_a": {"technical": 2, "analytical": 1},
    "q3_b": {"creative": 2},
    "q3_c": {"social": 2},
    "q3_d": {"business": 2},
    "q3_e": {"technical": 2},

    "q4_a": {"analytical": 2},
    "q4_b": {"creative": 2},
    "q4_c": {"social": 2},
    "q4_d": {"business": 2},
    "q4_e": {"technical": 2},

    "q5_a": {"analytical": 2},
    "q5_b": {"creative": 2},
    "q5_c": {"social": 2},
    "q5_d": {"leadership": 2},
    "q5_e": {"technical": 2},

    "q6_a": {"analytical": 2},
    "q6_b": {"creative": 2},
    "q6_c": {"social": 2},
    "q6_d": {"business": 2},
    "q6_e": {"technical": 2},

    "q7_a": {"analytical": 1, "technical": 1},
    "q7_b": {"creative": 2},
    "q7_c": {"social": 2},
    "q7_d": {"business": 2},
    "q7_e": {"technical": 2},

    "q8_a": {"technical": 2},
    "q8_b": {"creative": 2},
    "q8_c": {"social": 2},
    "q8_d": {"business": 2},
    "q8_e": {"technical": 2},

    "q9_a": {"analytical": 2},
    "q9_b": {"creative": 2},
    "q9_c": {"social": 2},
    "q9_d": {"leadership": 2},
    "q9_e": {"technical": 2},

    "q10_a": {"analytical": 2},
    "q10_b": {"creative": 2},
    "q10_c": {"social": 2},
    "q10_d": {"business": 2},
    "q10_e": {"technical": 2},

    "q11_a": {"technical": 2, "analytical": 1},
    "q11_b": {"creative": 2},
    "q11_c": {"social": 2},
    "q11_d": {"business": 2},
    "q11_e": {"technical": 2},

    "q12_a": {"analytical": 2},
    "q12_b": {"creative": 2},
    "q12_c": {"social": 2},
    "q12_d": {"business": 2},
    "q12_e": {"technical": 2},

    "q13_a": {"technical": 2},
    "q13_b": {"creative": 2},
    "q13_c": {"social": 2},
    "q13_d": {"business": 2},
    "q13_e": {"technical": 2},

    "q14_a": {"analytical": 2},
    "q14_b": {"creative": 2},
    "q14_c": {"social": 2},
    "q14_d": {"business": 2},
    "q14_e": {"technical": 2},

    "q15_a": {"analytical": 2, "technical": 1},
    "q15_b": {"creative": 2},
    "q15_c": {"social": 2},
    "q15_d": {"business": 2},
    "q15_e": {"technical": 2},
}

CAREERS = {
    "Software Engineer": {"analytical": 8, "technical": 10},
    "Data Scientist": {"analytical": 10, "technical": 8},
    "Cyber Security Analyst": {"technical": 9, "analytical": 8},
    "UI/UX Designer": {"creative": 9, "technical": 5},
    "Graphic Designer": {"creative": 10},
    "Psychologist": {"social": 10},
    "Teacher": {"social": 9},
    "Business Analyst": {"business": 9, "analytical": 7},
    "Marketing Manager": {"business": 10, "creative": 7},
    "Mechanical Engineer": {"technical": 10},
    "Civil Engineer": {"technical": 10}
}

def calculate_traits(answers):
    traits = {t: 0 for t in TRAITS}

    for ans in answers:
        print("CHECKING:", ans)

        if ans in SCORE_MAP:
            for trait, score in SCORE_MAP[ans].items():
                traits[trait] += score
        else:
            print("NOT FOUND:", ans)

    return traits


def match_careers(user_traits):
    results = []

    for career, req in CAREERS.items():
        score = 0
        max_score = 0

        for trait, weight in req.items():
            user_val = user_traits.get(trait, 0)
            score += min(user_val, weight)
            max_score += weight

        percent = (score / max_score) * 100 if max_score else 0

        results.append({
            "name": career,
            "score": round(percent, 2)
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


# =========================
# LOGIN (FIXED - SINGLE ROUTE)
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")

        if email not in registered_users:
            flash("Account not found.")
            return redirect(url_for("login"))

        if registered_users[email] != password:
            flash("Wrong password.")
            return redirect(url_for("login"))

        session["user"] = email
        session.permanent = True if remember else False

        return redirect(url_for("dashboard"))

    return render_template("login.html")


# =========================
# REGISTER (UNCHANGED LOGIC)
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        registered_users[email] = password
        save_users(registered_users)

        flash("Registered successfully.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("Dashboard.html")


@app.route("/assessment")
def assessment():
    return render_template("assessment.html")


@app.route("/result", methods=["POST"])
def result():
    answers = []

    for i in range(1, 16):
        val = request.form.get(f"q{i}")

        if val is None:
            print("MISSING:", f"q{i}")
            continue

        answers.append(val)

    print("FINAL ANSWERS:", answers)

    user_traits = calculate_traits(answers)
    print("TRAITS:", user_traits)

    results = match_careers(user_traits)

    return render_template("result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)

   