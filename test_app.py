import pytest
from app import app, db, Student

@pytest.fixture
def client():
    """Setup the Flask test client and initialize an empty database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Clear the database
            db.create_all()  # Recreate the database schema
        yield client

def test_main_page(client):
    """Test that the main page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200  # Check that the page loads successfully
    assert b"<title>" in response.data  # Check if the response contains a title tag

def test_add_page(client):
    """Test that the add page loads successfully."""
    response = client.get('/add')
    assert response.status_code == 200  # Check that the page loads successfully
    assert b"<form" in response.data  # Check if the response contains a form

def test_add_student_submission(client):
    """Test adding a student through the form."""
    response = client.post('/add', data={
        'name': 'John Doe',
        'age': 20,
        'email': 'john@example.com'
    })
    assert response.status_code == 302  # Ensure the form redirects after submission
    
    # Check that the student was added to the database
    with app.app_context():
        students = Student.query.all()
        assert len(students) == 1
        assert students[0].name == 'John Doe'
        assert students[0].age == 20
        assert students[0].email == 'john@example.com'

def test_edit_student(client):
    """Test editing a student's details."""
    with app.app_context():
        # Add a test student
        student = Student(name='Jane Doe', age=22, email='jane@example.com')
        db.session.add(student)
        db.session.commit()
        student_id = student.id  # Store the ID before exiting the context

    # Edit the student's details
    response = client.post(f'/edit/{student_id}', data={
        'name': 'Jane Smith',
        'age': 23,
        'email': 'jane.smith@example.com'
    })
    assert response.status_code == 302  # Ensure redirect after submission

    # Verify the changes
    with app.app_context():
        updated_student = db.session.get(Student, student_id)
        assert updated_student.name == 'Jane Smith'
        assert updated_student.age == 23
        assert updated_student.email == 'jane.smith@example.com'


def test_delete_student(client):
    """Test deleting a student."""
    with app.app_context():
        # Add a test student
        student = Student(name='Jake Doe', age=21, email='jake@example.com')
        db.session.add(student)
        db.session.commit()
        student_id = student.id  # Store the ID before exiting the context

    # Delete the student
    response = client.post(f'/delete/{student_id}')
    assert response.status_code == 302  # Ensure redirect after deletion

    # Verify the student is deleted
    with app.app_context():
        deleted_student = db.session.get(Student, student_id)
        assert deleted_student is None
