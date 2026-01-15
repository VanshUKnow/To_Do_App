from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# File to store todos
TODOS_FILE = 'todos.json'

def load_todos():
    """Load todos from JSON file"""
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    """Save todos to JSON file"""
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/')
def index():
    """Display all todos"""
    todos = load_todos()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new todo"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority', 'medium')
        due_date = request.form.get('due_date')
        
        if not title:
            return redirect(url_for('add'))
        
        todos = load_todos()
        new_todo = {
            'id': max([t['id'] for t in todos], default=0) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        todos.append(new_todo)
        save_todos(todos)
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    """Edit an existing todo"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        todo['title'] = request.form.get('title', todo['title'])
        todo['description'] = request.form.get('description', todo['description'])
        todo['priority'] = request.form.get('priority', todo['priority'])
        todo['due_date'] = request.form.get('due_date', todo['due_date'])
        save_todos(todos)
        return redirect(url_for('index'))
    
    return render_template('edit.html', todo=todo)

@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    """Toggle todo completion status"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if todo:
        todo['completed'] = not todo['completed']
        save_todos(todos)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    """Delete a todo"""
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)
    return redirect(url_for('index'))

@app.route('/view/<int:todo_id>')
def view(todo_id):
    """View a single todo"""
    todos = load_todos()
    todo = next((t for t in todos if t['id'] == todo_id), None)
    
    if not todo:
        return redirect(url_for('index'))
    
    return render_template('view.html', todo=todo)

if __name__ == '__main__':
    app.run(debug=True)