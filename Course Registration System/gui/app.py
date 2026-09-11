import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "main") not in sys.path:
    sys.path.insert(0, str(ROOT / "main"))

from core import services
from user import Student, Teacher


NAVY = "#0f172a"
SLATE = "#1e293b"
CARD = "#273449"
ACCENT = "#38bdf8"
ACCENT_DARK = "#0ea5e9"
TEXT = "#4480c9"
MUTED = "#94a3b8"
SUCCESS = "#34d399"
DANGER = "#f87171"
ROW_ALT = "#334155"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Course Registration System")
        self.geometry("980x640")
        self.minsize(860, 560)
        self.configure(bg=NAVY)
        self.role_class = None
        self.current_user = None
        self._build_style()
        self.container = tk.Frame(self, bg=NAVY)
        self.container.pack(fill="both", expand=True)
        self.show_home()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "Treeview",
            background=SLATE,
            foreground=TEXT,
            fieldbackground=SLATE,
            borderwidth=0,
            rowheight=28,
            font=("Helvetica", 11),
        )
        style.configure(
            "Treeview.Heading",
            background=CARD,
            foreground=TEXT,
            font=("Helvetica", 11, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", ACCENT_DARK)])

    def clear(self):
        for child in self.container.winfo_children():
            child.destroy()

    def show_home(self):
        self.clear()
        self.role_class = None
        self.current_user = None
        frame = tk.Frame(self.container, bg=NAVY)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Course Registration System",
            bg=NAVY,
            fg=TEXT,
            font=("Helvetica", 28, "bold"),
        ).pack(pady=(80, 8))
        tk.Label(
            frame,
            text="Choose how you want to continue",
            bg=NAVY,
            fg=MUTED,
            font=("Helvetica", 13),
        ).pack(pady=(0, 36))

        buttons = tk.Frame(frame, bg=NAVY)
        buttons.pack()
        self._role_card(buttons, "Student", "Register and manage your courses", Student).pack(
            side="left", padx=16
        )
        self._role_card(buttons, "Teacher", "Create courses and view enrollments", Teacher).pack(
            side="left", padx=16
        )

    def _role_card(self, parent, title, subtitle, role_class):
        card = tk.Frame(parent, bg=SLATE, padx=28, pady=24, width=280, height=180)
        card.pack_propagate(False)
        tk.Label(card, text=title, bg=SLATE, fg=TEXT, font=("Helvetica", 20, "bold")).pack(
            anchor="w"
        )
        tk.Label(card, text=subtitle, bg=SLATE, fg=MUTED, font=("Helvetica", 11), wraplength=220).pack(
            anchor="w", pady=(6, 18)
        )
        tk.Button(
            card,
            text=f"Continue as {title}",
            command=lambda: self.show_auth(role_class),
            bg=ACCENT,
            fg=NAVY,
            activebackground=ACCENT_DARK,
            activeforeground=NAVY,
            font=("Helvetica", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8,
        ).pack(anchor="w")
        return card

    def show_auth(self, role_class):
        self.clear()
        self.role_class = role_class
        role = role_class.get_name()

        header = tk.Frame(self.container, bg=NAVY)
        header.pack(fill="x", padx=28, pady=(20, 8))
        tk.Button(
            header,
            text="← Back",
            command=self.show_home,
            bg=NAVY,
            fg=ACCENT,
            relief="flat",
            font=("Helvetica", 11),
            cursor="hand2",
        ).pack(side="left")
        tk.Label(
            header,
            text=f"{role} Portal",
            bg=NAVY,
            fg=TEXT,
            font=("Helvetica", 22, "bold"),
        ).pack(side="left", padx=16)

        notebook = ttk.Notebook(self.container)
        notebook.pack(fill="both", expand=True, padx=40, pady=16)

        login_tab = tk.Frame(notebook, bg=SLATE, padx=32, pady=28)
        register_tab = tk.Frame(notebook, bg=SLATE, padx=32, pady=28)
        notebook.add(login_tab, text="Login")
        notebook.add(register_tab, text="Register")
        self._build_login_form(login_tab, role_class)
        self._build_register_form(register_tab, role_class)

    def _labeled_entry(self, parent, label, show=None):
        tk.Label(parent, text=label, bg=SLATE, fg=MUTED, font=("Helvetica", 11)).pack(anchor="w", pady=(10, 2))
        entry = tk.Entry(
            parent,
            bg=CARD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Helvetica", 12),
            show=show or "",
        )
        entry.pack(fill="x", ipady=7)
        return entry

    def _action_button(self, parent, text, command, bg=ACCENT, fg=NAVY):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=ACCENT_DARK,
            relief="flat",
            font=("Helvetica", 12, "bold"),
            cursor="hand2",
            pady=8,
        )

    def _build_login_form(self, parent, role_class):
        username = self._labeled_entry(parent, "Username")
        password = self._labeled_entry(parent, "Password", show="•")
        status = tk.Label(parent, text="", bg=SLATE, fg=DANGER, font=("Helvetica", 11))
        status.pack(anchor="w", pady=(12, 0))

        def submit():
            user, message = services.login_user(role_class, username.get(), password.get())
            if user is None:
                status.config(text=message, fg=DANGER)
                return
            self.current_user = user
            if role_class.get_name() == "Student":
                self.show_student_dashboard()
            else:
                self.show_teacher_dashboard()

        self._action_button(parent, "Log in", submit).pack(fill="x", pady=(18, 0))

    def _build_register_form(self, parent, role_class):
        full_name = self._labeled_entry(parent, "Full name")
        username = self._labeled_entry(parent, "Username")
        email = self._labeled_entry(parent, "Email (@gmail.com)")
        password = self._labeled_entry(parent, "Password", show="•")
        confirm = self._labeled_entry(parent, "Confirm password", show="•")
        tk.Label(
            parent,
            text=services.PASSWORD_RULES_TEXT,
            bg=SLATE,
            fg=MUTED,
            wraplength=520,
            justify="left",
            font=("Helvetica", 10),
        ).pack(anchor="w", pady=(10, 0))
        status = tk.Label(parent, text="", bg=SLATE, fg=DANGER, font=("Helvetica", 11))
        status.pack(anchor="w", pady=(8, 0))

        def submit():
            ok, message = services.register_user(
                role_class,
                full_name.get(),
                username.get(),
                email.get(),
                password.get(),
                confirm.get(),
            )
            status.config(text=message, fg=SUCCESS if ok else DANGER)
            if ok:
                full_name.delete(0, "end")
                username.delete(0, "end")
                email.delete(0, "end")
                password.delete(0, "end")
                confirm.delete(0, "end")

        self._action_button(parent, "Create account", submit).pack(fill="x", pady=(16, 0))

    def _dashboard_shell(self, title):
        self.clear()
        header = tk.Frame(self.container, bg=SLATE)
        header.pack(fill="x")
        tk.Label(header, text=title, bg=SLATE, fg=TEXT, font=("Helvetica", 20, "bold")).pack(
            side="left", padx=24, pady=16
        )
        tk.Label(
            header,
            text=self.current_user.full_name,
            bg=SLATE,
            fg=MUTED,
            font=("Helvetica", 12),
        ).pack(side="left")
        tk.Button(
            header,
            text="Log out",
            command=lambda: self.show_auth(self.role_class),
            bg=CARD,
            fg=TEXT,
            relief="flat",
            cursor="hand2",
            font=("Helvetica", 11),
            padx=12,
            pady=6,
        ).pack(side="right", padx=20)
        body = tk.Frame(self.container, bg=NAVY)
        body.pack(fill="both", expand=True, padx=20, pady=16)
        return body

    def _tree(self, parent, columns, headings, height=8):
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=height)
        for col, heading, width in zip(columns, headings, [220, 220, 220, 220][: len(columns)]):
            tree.heading(col, text=heading)
            tree.column(col, width=width, anchor="w")
        tree.tag_configure("odd", background=SLATE)
        tree.tag_configure("even", background=ROW_ALT)
        tree.pack(fill="both", expand=True)
        return tree

    def _fill_tree(self, tree, rows):
        tree.delete(*tree.get_children())
        for index, row in enumerate(rows):
            tree.insert("", "end", values=row, tags=("even" if index % 2 else "odd",))

    def show_student_dashboard(self):
        body = self._dashboard_shell("Student Dashboard")
        left = tk.Frame(body, bg=NAVY)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(body, bg=SLATE, padx=16, pady=16, width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(left, text="My courses", bg=NAVY, fg=TEXT, font=("Helvetica", 14, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        tree = self._tree(left, ("name", "teacher", "id"), ("Course", "Teacher", "Course ID"))

        tk.Label(right, text="Register for a course", bg=SLATE, fg=TEXT, font=("Helvetica", 13, "bold")).pack(
            anchor="w"
        )
        course_var = tk.StringVar()
        course_menu = ttk.Combobox(right, textvariable=course_var, state="readonly")
        course_menu.pack(fill="x", pady=(8, 10))
        available = []

        def refresh():
            nonlocal available
            enrolled = services.student_enrollments(self.current_user)
            self._fill_tree(
                tree,
                [(item["course_name"], item["teacher_name"], item["course_id"]) for item in enrolled],
            )
            available = services.available_courses_for_student(self.current_user)
            labels = [f"{item['course_name']} — {item['teacher_name']}" for item in available]
            course_menu["values"] = labels
            course_var.set(labels[0] if labels else "")

        def selected_available():
            labels = list(course_menu["values"])
            if course_var.get() not in labels:
                return None
            return available[labels.index(course_var.get())]

        def add_course():
            course = selected_available()
            if not course:
                messagebox.showinfo("Courses", "Select a course to register.")
                return
            ok, message = services.register_student_course(self.current_user, course["course_id"])
            messagebox.showinfo("Register", message) if ok else messagebox.showerror("Register", message)
            refresh()

        def drop_course():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Drop course", "Select a course in your list first.")
                return
            course_id = tree.item(selected[0], "values")[2]
            if not messagebox.askyesno("Drop course", "Drop the selected course?"):
                return
            ok, message = services.drop_student_course(self.current_user, course_id)
            messagebox.showinfo("Drop course", message) if ok else messagebox.showerror("Drop course", message)
            refresh()

        self._action_button(right, "Register", add_course).pack(fill="x")
        tk.Button(
            right,
            text="Drop selected course",
            command=drop_course,
            bg=CARD,
            fg=TEXT,
            relief="flat",
            cursor="hand2",
            pady=8,
        ).pack(fill="x", pady=(10, 18))

        self._password_panel(right, Student)
        refresh()

    def show_teacher_dashboard(self):
        body = self._dashboard_shell("Teacher Dashboard")
        left = tk.Frame(body, bg=NAVY)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))
        right = tk.Frame(body, bg=SLATE, padx=16, pady=16, width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(left, text="My courses", bg=NAVY, fg=TEXT, font=("Helvetica", 14, "bold")).pack(
            anchor="w", pady=(0, 8)
        )
        tree = self._tree(left, ("name", "id"), ("Course", "Course ID"), height=7)

        tk.Label(left, text="Students in selected course", bg=NAVY, fg=TEXT, font=("Helvetica", 14, "bold")).pack(
            anchor="w", pady=(12, 8)
        )
        students_tree = self._tree(left, ("name", "username", "email"), ("Name", "Username", "Email"), height=6)

        tk.Label(right, text="Create a course", bg=SLATE, fg=TEXT, font=("Helvetica", 13, "bold")).pack(
            anchor="w"
        )
        name_entry = tk.Entry(right, bg=CARD, fg=TEXT, insertbackground=TEXT, relief="flat", font=("Helvetica", 12))
        name_entry.pack(fill="x", ipady=7, pady=(8, 10))

        def refresh_courses():
            courses = services.teacher_courses(self.current_user)
            self._fill_tree(tree, [(item["course_name"], item["course_id"]) for item in courses])
            students_tree.delete(*students_tree.get_children())

        def create():
            ok, message = services.create_course(self.current_user, name_entry.get())
            messagebox.showinfo("New course", message) if ok else messagebox.showerror("New course", message)
            if ok:
                name_entry.delete(0, "end")
                refresh_courses()

        def drop():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Drop course", "Select a course first.")
                return
            course_id = tree.item(selected[0], "values")[1]
            if not messagebox.askyesno("Drop course", "Drop this course and its enrollments?"):
                return
            ok, message = services.drop_teacher_course(self.current_user, course_id)
            messagebox.showinfo("Drop course", message) if ok else messagebox.showerror("Drop course", message)
            refresh_courses()

        def show_students(_event=None):
            selected = tree.selection()
            if not selected:
                return
            course_id = tree.item(selected[0], "values")[1]
            rows = [
                (item["full_name"], item["username"], item["email"])
                for item in services.students_in_course(course_id)
            ]
            self._fill_tree(students_tree, rows)

        tree.bind("<<TreeviewSelect>>", show_students)
        self._action_button(right, "Create course", create).pack(fill="x")
        tk.Button(
            right,
            text="Drop selected course",
            command=drop,
            bg=CARD,
            fg=TEXT,
            relief="flat",
            cursor="hand2",
            pady=8,
        ).pack(fill="x", pady=(10, 18))
        self._password_panel(right, Teacher)
        refresh_courses()

    def _password_panel(self, parent, role_class):
        tk.Label(parent, text="Change password", bg=SLATE, fg=TEXT, font=("Helvetica", 13, "bold")).pack(
            anchor="w", pady=(8, 4)
        )
        current = self._labeled_entry(parent, "Current password", show="•")
        current.configure(bg=CARD)
        new = self._labeled_entry(parent, "New password", show="•")
        confirm = self._labeled_entry(parent, "Confirm new password", show="•")

        def submit():
            ok, message = services.change_password(
                role_class,
                self.current_user,
                current.get(),
                new.get(),
                confirm.get(),
            )
            messagebox.showinfo("Password", message) if ok else messagebox.showerror("Password", message)
            if ok:
                current.delete(0, "end")
                new.delete(0, "end")
                confirm.delete(0, "end")

        tk.Button(
            parent,
            text="Update password",
            command=submit,
            bg=CARD,
            fg=TEXT,
            relief="flat",
            cursor="hand2",
            pady=8,
        ).pack(fill="x", pady=(12, 0))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
