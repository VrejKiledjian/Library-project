import os
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from peewee import DoesNotExist
from werkzeug.utils import secure_filename

import models
from form import CreateUserForm, LoginForm, AddBookForm, SearchForm, AdminForm, AdminLoginForm
from models import Student, Books, database, Admin, BooksCopy, BorrowedBook
import uuid
# from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

# from login import login_required

# from flask import render_template

app = Flask(__name__,
            static_url_path='/static')

app.config.from_object("config.AppConfig")
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# admin = Admin(app)
# admin.add_views(ModelView(Books), ModelView(Student))


# This is the key to enter website
def inject_dict() -> dict:
    language = request.cookies.get("language", "en")
    user_id = session.get("user")
    user = None
    admin = None  # Add this line
    if user_id:
        user = Student.get(user_id)
        # Fetch admin if the user is an admin (You need to implement this logic)
        if user.roll == "admin":
            admin = Admin.get(user_id)

    return {
        "language": language,
        "user": user,
        "admin": admin,  # Add this line
    }


@login_manager.user_loader
def load_user(id):
    roll = session.get('roll')
    if roll == 'admin':
        user = Admin.get(id=id)
    elif roll is None:
        user = Student.get(id=id)
    else:
        user = None
    return user
    # return user.roll is None:
    #     return student

    # admin = Admin.get_or_none(Admin.id == user_id)
    # if admin:
    #     return admin


@app.route("/")
def home():
    return render_template("home.html")


# @app.route("/login/admin", methods=["GET", "POST"])
# def login_admin():
#     form = AdminLoginForm()
#     if form.validate_on_submit():
#         try:
#             user = Admin.get(full_name_admin=form.full_name_admin.data)
#             hashed_password = Admin.hash_password(form.full_name_admin.data, form.password.data)
#             if user.password != hashed_password:
#                 form.full_name_admin.errors.append("Invalid credentials")
#                 return render_template("login_admin.html", form=form)
#
#             # Check if the user is an admin
#             if user.roll == "admin":
#                 login_user(user)
#                 return redirect("/")
#             else:
#                 form.full_name_admin.errors.append("You do not have admin privileges.")
#                 return render_template("login_admin.html", form=form)
#         except Admin.DoesNotExist:
#             form.full_name_admin.errors.append("Account does not exist")
#             return render_template("login_admin.html", form=form)
#
#     return render_template("login_admin.html", form=form)


@app.route("/login/admin", methods=["GET", "POST"])
def login_admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.get(full_name_admin=form.full_name_admin.data)
        hashed_password = Admin.hash_password(form.full_name_admin.data, form.password.data)
        session["roll"] = "admin"
        if not user or user.password != hashed_password:
            form.full_name_admin.errors.append("Invalid credentials")
            return render_template("login_admin.html", form=form)
        login_user(user)
        # session["user"] = user.id
        return redirect("/")

    return render_template("login_admin.html", form=form)


@app.route("/admin/new", methods=["GET", "POST"])
def new_admin():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.from_admin_registration_form(form)
        admin.save()
        return redirect("/")
    return render_template("admin.html", form=form)


@app.route("/profile/<int:student_id>")
def profile(student_id):
    student = load_user(student_id)
    if student is None:
        return render_template("404.html")

    # Continue processing and render the student's profile
    return render_template("profile.html", student=student)


@app.route("/dashbored/<int:admin_id>")
def dashbored(admin_id):
    admin = load_user(admin_id)
    if admin is None:
        return render_template("404.html")
    return render_template("admin_dashbord.html", admin=admin)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/students")
@login_required
def students():
    student = Student.select()
    return render_template("students.html", students=student)


@app.route("/students/new", methods=["GET", "POST"])
@login_required
def new_student():
    form = CreateUserForm()
    if form.validate_on_submit():
        add_student_form = Student.from_student_add_form(form)
        add_student_form.save()
        return redirect("/")
    return render_template("register.html", form=form)

    # if create_student_form.validate_on_submit():
    #     student = Student(
    #         full_name=create_student_form.full_name.data,
    #         grade=create_student_form.grade.data,
    #     )
    #     student.save()
    #     return redirect("/students")
    # return render_template("new-student.html", form=create_student_form)


@app.route("/students/<int:student_id>")  # Dynamic routing
@login_required
def student_details(student_id):
    try:
        student = Student.get(id=student_id)
        return render_template("student_details.html", student=student)
    except Student.DoesNotExist:
        return render_template("404.html"), 404


@app.route("/students/delete/<int:students_id>", methods=["GET", "POST"])
@login_required
def delete_student(students_id):
    try:
        student = Student.get_by_id(students_id)
        student.delete_instance()
        flash("Students deleted successfully", "success")
    except Student.DoesNotExist:
        flash("Students Not Found", "danger")
    return redirect("/students")


@app.route("/login/student", methods=["GET", "POST"])
def login_student():
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.get(full_name=form.full_name.data)
        hashed_password = Student.hash_password(form.full_name.data, form.password.data)
        session["roll"] = None
        if not user or user.password != hashed_password:
            form.full_name.errors.append("Invalid credentials")
            return render_template("login_student.html", form=form)
        login_user(user)
        # session["user"] = user.id
        return redirect("/")

    return render_template("login_student.html", form=form)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    searched = form.searched.data

    # Query your database to check if the searched book exists
    book = Books.select().filter(Books.title.ilike(f'%{searched}%')).first()

    # Fetch all books for displaying search results
    books_cont = Books.select().filter(Books.title.ilike(f'%{searched}%'))

    return render_template("search.html", form=form, searched=searched, book=book, books_cont=books_cont.execute())


@app.route("/books")
def books():
    book = Books.select()
    return render_template("books.html", books=book)


def generate_unique_serial_number():
    # Generate a UUID (Universally Unique Identifier)
    unique_id = uuid.uuid4()

    # Convert the UUID to a string and remove hyphens to create a serial number
    serial_number = str(unique_id).replace("-", "")

    return serial_number


UPLOAD_FOLDER = os.path.join(app.static_folder, 'book_covers')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/books/new", methods=["GET", "POST"])
@login_required
def new_book():
    book_copy = BooksCopy()
    add_book_form = AddBookForm()
    if request.method == "POST":
        image_path = request.files["image_path"]
        image_path.save(f"{app.static_folder}/book_covers/{image_path.filename}")
    if add_book_form.validate_on_submit():
        book = Books(
            title=add_book_form.title.data,
            author=add_book_form.author.data,
            publish_year=add_book_form.publish_year.data,
            ISBN=add_book_form.ISBN.data,
            summary=add_book_form.summary.data,
            image_path=image_path.filename
        )
        book.save()
        num_copies = 10
        for _ in range(num_copies):
            serial_number = generate_unique_serial_number()
            new_book_copy = book_copy.create(book=book, copy_number=serial_number, is_available=True, title=book.title)
            new_book_copy.save()
        return redirect("/books")
    return render_template("new-book.html", form=add_book_form)


# @app.route("/books/new", methods=["GET", "POST"])
# @login_required
# def new_book():
#     book_copy = BooksCopy()
#     add_book_form = AddBookForm()
#     if request.method == "POST":
#         photo = request.files["photo"]
#         photo.save(os.path.join(app.static_folder, photo.filename))
#         if add_book_form.validate_on_submit():
#             book = Books(
#                 title=add_book_form.title.data,
#                 author=add_book_form.author.data,
#                 publish_year=add_book_form.publish_year.data,
#                 ISBN=add_book_form.ISBN.data,
#                 summary=add_book_form.summary.data,
#             )
#             book.save()
#             num_copies = 10
#             for _ in range(num_copies):
#                 serial_number = generate_unique_serial_number()
#                 new_book_copy = book_copy.create(book=book, copy_number=serial_number, is_available=True)
#                 new_book_copy.save()
#             return redirect("/books")
#     return render_template("new-book.html", form=add_book_form)


@app.route("/books/<int:book_id>")  # Dynamic routing
def book_details(book_id):
    try:
        book = Books.get(id=book_id)
        return render_template("book-derails.html", book=book)
    except Books.DoesNotExist:
        return render_template("404.html"), 404


@app.route("/books/delete/<int:book_id>", methods=["GET", "POST"])
@login_required
def delete_book(book_id):
    try:
        book = Books.get_by_id(book_id)
        book.delete_instance()
        flash("Book deleted successfully", "success")
    except Books.DoesNotExist:
        flash("Book not found", "danger")
    return redirect("/books")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = Student.from_registration_form(form)
        user.save()
        return redirect("/")
    return render_template("register.html", form=form)


@app.route("/borrow/<int:book_id>", methods=["GET", "POST"])
@login_required
def borrow(book_id):
    book = Books.get_or_none(Books.id == book_id)  # Get the Book by its ID

    if current_user.book_limit > 0 and book:
        available_copy = book.copies.where(BooksCopy.is_available == True).first()

        if available_copy:
            borrow_date = datetime.now()

            # Create a new entry in the borrowing table
            borrowing = BorrowedBook.create(student_id=current_user.id, book_copy_id=available_copy.id,
                                            borrow_date=borrow_date)

            # Update the book copy status to mark it as borrowed
            available_copy.is_available = False
            available_copy.save()

            # Update the user's book limit
            current_user.book_limit -= 1
            current_user.borrowed_book += book.title
            if current_user.borrowed_book:
                current_user.borrowed_book += ","
            current_user.save()

            flash("You have successfully borrowed the book", "success")
        else:
            flash("Sorry, all copies of this book are already borrowed")
    else:
        return render_template("404.html")
    borrowed_books = BorrowedBook.select().where(BorrowedBook.student_id == current_user.id)
    return redirect(url_for("profile", student_id=current_user.id, borrowed_books=borrowed_books))


@app.route("/return", methods=["GET", "POST"])
@login_required
def return_book():
    # Get a list of book copy IDs to be returned from the form submission
    book_copy_ids_to_return = request.form.getlist("book_copy_ids")

    # Check if the user has selected any books to return
    if not book_copy_ids_to_return:
        flash("Please select at least one book to return", "error")
        return redirect(url_for("profile", student_id=current_user.id))

    # Iterate through the selected book copy IDs and process each one
    for book_copy_id in book_copy_ids_to_return:
        # Check if the book copy exists and is borrowed by the current user
        borrowed_book = BorrowedBook.get_or_none(
            BorrowedBook.book_copy_id == book_copy_id,
            BorrowedBook.student_id == current_user.id
        )

        if borrowed_book:
            # Update the return date for the borrowed book
            borrowed_book.return_date = datetime.now()
            borrowed_book.save()

            # Get the associated book copy and mark it as available
            book_copy = borrowed_book.book_copy
            book_copy.is_available = True
            book_copy.save()

            # Find and delete the specific borrowed book instance by book_copy_id
            matching_borrowed_book = current_user.borrowed_books.filter(
                BorrowedBook.book_copy_id == book_copy.id).first()
            if matching_borrowed_book:
                matching_borrowed_book.delete_instance()

            # Increase the user's book_limit (if needed)
            current_user.book_limit += 1
            current_user.save()
            database.commit()
    flash("You have successfully returned the selected books", "success")
    return redirect(url_for("profile", student_id=current_user.id))


if __name__ == "__main__":
    app.run(debug=True, port=8001)
