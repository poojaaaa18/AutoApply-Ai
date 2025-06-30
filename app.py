# app.py
from flask import Flask
# from routes.apply import apply_bp
from routes.resume import resume_bp
from routes.jobs import jobs_bp

app = Flask(__name__)
# app.register_blueprint(apply_bp)
app.register_blueprint(resume_bp)
app.register_blueprint(jobs_bp)

if __name__ == "__main__":
    app.run(debug=True)
