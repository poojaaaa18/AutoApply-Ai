from flask import Blueprint, request, jsonify
import fitz  # PyMuPDF
from services.scarper import scrape_indeed_jobs
jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs-fetched', methods=['POST'])
def get_jobs():
    try:
        if request.method == "POST":
            filter_ = request.get_json('filter')
            fetched_jobs = scrape_indeed_jobs(filter_)  # filter should  be { 't':title,'l':location }
            return jsonify({'jobs': fetched_jobs}), 200

    except Exception as e:
        
        return jsonify({'error': str(e)}), 500
