from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Task

task_bp = Blueprint("tasks", __name__)

@task_bp.route("/")
@login_required
def tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template("tasks.html", tasks=tasks)

@task_bp.route("/add", methods=["POST"])
@login_required
def add_task():
    task = Task(title=request.form["title"], user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    return "Task Added"

# REST API
@task_bp.route("/api/tasks")
@login_required
def api_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": t.id, "title": t.title} for t in tasks])
