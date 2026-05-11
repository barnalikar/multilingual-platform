from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session

from extensions import db

from models import User

from otp_utils import generate_otp

from translations import translations

language_bp = Blueprint(
    "language",
    __name__
)


# DASHBOARD
@language_bp.route(
    "/dashboard",
    methods=["GET", "POST"]
)
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    user = User.query.get(
        session["user_id"]
    )

    # SAFE TRANSLATION
    translated_text = translations.get(
        user.language,
        translations["English"]
    )["welcome"]

    # LANGUAGE CHANGE
    if request.method == "POST":

        selected_language = request.form["language"]

        otp = generate_otp()

        print("\n====================")
        print("OTP GENERATED:", otp)
        print("====================\n")

        user.otp = otp

        db.session.commit()

        session["selected_language"] = selected_language

        # FRENCH -> EMAIL
        if selected_language == "French":

            print("EMAIL VERIFICATION REQUIRED")

        else:

            print("MOBILE VERIFICATION REQUIRED")

        return redirect("/verify-otp")

    return render_template(
        "dashboard.html",
        user=user,
        translated_text=translated_text
    )


# VERIFY OTP
@language_bp.route(
    "/verify-otp",
    methods=["GET", "POST"]
)
def verify_otp():

    if "user_id" not in session:
        return redirect("/")

    user = User.query.get(
        session["user_id"]
    )

    if request.method == "POST":

        entered_otp = request.form["otp"]

        print("Entered OTP:", entered_otp)
        print("Stored OTP:", user.otp)

        if entered_otp == user.otp:

            user.language = session[
                "selected_language"
            ]

            user.otp = None

            db.session.commit()

            return redirect("/dashboard")

        else:

            return "Wrong OTP"

    return render_template(
        "verify_otp.html"
    )