from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import OperationalError, ProgrammingError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LoginForm, SignUpForm
from .models import Leaderboard, Quiz, QuizAttempt, Result


QUIZZES = [
    {
        "title": "Python Foundations",
        "slug": "python-foundations",
        "category": "Programming",
        "level": "Beginner",
        "questions": 20,
        "duration": 25,
        "rating": 4.9,
        "attempts": "12.4k",
        "color": "teal",
        "description": "Master variables, control flow, functions, and core Python thinking.",
    },
    {
        "title": "Django Web Basics",
        "slug": "django-web-basics",
        "category": "Web Development",
        "level": "Intermediate",
        "questions": 24,
        "duration": 30,
        "rating": 4.8,
        "attempts": "8.1k",
        "color": "indigo",
        "description": "Routes, templates, models, auth, and clean Django project structure.",
    },
    {
        "title": "Data Structures Sprint",
        "slug": "data-structures-sprint",
        "category": "Computer Science",
        "level": "Advanced",
        "questions": 30,
        "duration": 40,
        "rating": 4.7,
        "attempts": "6.7k",
        "color": "amber",
        "description": "Arrays, stacks, queues, trees, graphs, and complexity checkpoints.",
    },
]

QUESTIONS = [
    {
        "number": 1,
        "text": "Which Python type is immutable?",
        "options": ["list", "dict", "tuple", "set"],
        "answer": "tuple",
        "selected": "tuple",
        "state": "correct",
    },
    {
        "number": 2,
        "text": "Which Django file maps URL patterns to view functions?",
        "options": ["settings.py", "urls.py", "models.py", "apps.py"],
        "answer": "urls.py",
        "selected": "models.py",
        "state": "wrong",
    },
    {
        "number": 3,
        "text": "What does CSRF protection help prevent?",
        "options": ["Broken images", "Unauthorized form submissions", "Slow queries", "CSS errors"],
        "answer": "Unauthorized form submissions",
        "selected": "",
        "state": "missed",
    },
]

LEADERS = [
    {"rank": 1, "name": "Aarav Sharma", "score": 98, "quizzes": 42, "streak": 18},
    {"rank": 2, "name": "Maya Iyer", "score": 96, "quizzes": 39, "streak": 14},
    {"rank": 3, "name": "Rohan Mehta", "score": 94, "quizzes": 35, "streak": 11},
    {"rank": 4, "name": "Sneha Rao", "score": 91, "quizzes": 31, "streak": 9},
]

ACTIVITY = [
    "Completed Python Foundations with 92%",
    "Earned Django Starter certificate",
    "Moved into top 10% this week",
    "Reviewed 12 incorrect answers",
]


QUIZ_COLORS = ["teal", "indigo", "amber"]


def serialize_quiz(quiz, index=0):
    return {
        "title": quiz.title,
        "slug": quiz.slug,
        "category": quiz.category.name,
        "level": quiz.level,
        "questions": quiz.question_count,
        "duration": quiz.duration_minutes,
        "duration_seconds": quiz.duration_minutes * 60,
        "rating": 4.8,
        "attempts": quiz.attempts.count(),
        "color": QUIZ_COLORS[index % len(QUIZ_COLORS)],
        "description": quiz.description,
    }


def serialize_question(question, selected_choice_id=None):
    choices = list(question.choices.all())
    correct_choice = next((choice for choice in choices if choice.is_correct), None)
    selected_choice = next((choice for choice in choices if str(choice.id) == str(selected_choice_id)), None)
    if selected_choice is None:
        state = "missed"
    elif selected_choice.is_correct:
        state = "correct"
    else:
        state = "wrong"
    return {
        "id": question.id,
        "number": question.order,
        "text": question.text,
        "options": [choice.text for choice in choices],
        "choices": choices,
        "answer": correct_choice.text if correct_choice else "",
        "selected": selected_choice.text if selected_choice else "",
        "state": state,
        "explanation": question.explanation,
    }


def get_quiz_context():
    try:
        quizzes = list(
            Quiz.objects.filter(is_published=True)
            .select_related("category")
            .prefetch_related("questions", "attempts")
        )
    except (OperationalError, ProgrammingError):
        return QUIZZES, QUIZZES[0], QUESTIONS, LEADERS

    if not quizzes:
        return QUIZZES, QUIZZES[0], QUESTIONS, LEADERS

    serialized_quizzes = [serialize_quiz(quiz, index) for index, quiz in enumerate(quizzes)]
    default_questions = [serialize_question(question) for question in quizzes[0].questions.prefetch_related("choices")]
    leaders = []
    for rank, entry in enumerate(
        Leaderboard.objects.select_related("user", "quiz").order_by("-best_percentage", "-best_score")[:10],
        start=1,
    ):
        leaders.append(
            {
                "rank": rank,
                "name": entry.user.get_full_name() or entry.user.username,
                "score": int(entry.best_percentage),
                "quizzes": entry.attempts_count,
                "streak": entry.attempts_count,
            }
        )
    return serialized_quizzes, serialized_quizzes[0], default_questions or QUESTIONS, leaders or LEADERS


def user_stats(user):
    if user is None or not user.is_authenticated:
        return [
            {"label": "Average score", "value": "87%", "trend": "+12%"},
            {"label": "Completed quizzes", "value": "24", "trend": "+6"},
            {"label": "Study streak", "value": "14 days", "trend": "Best"},
            {"label": "Global rank", "value": "#128", "trend": "Top 8%"},
        ]
    try:
        results = Result.objects.filter(user=user)
        completed = results.count()
        average = 0
        if completed:
            average = int(sum(float(result.percentage) for result in results) / completed)
        rank = list(Leaderboard.objects.order_by("-best_percentage", "-best_score").values_list("user_id", flat=True)).index(user.id) + 1 if Leaderboard.objects.filter(user=user).exists() else "-"
    except (OperationalError, ProgrammingError):
        completed = 0
        average = 0
        rank = "-"
    return [
        {"label": "Average score", "value": f"{average}%", "trend": "Live"},
        {"label": "Completed quizzes", "value": str(completed), "trend": "Submitted"},
        {"label": "Study streak", "value": f"{min(completed, 14)} days", "trend": "Active"},
        {"label": "Global rank", "value": f"#{rank}" if rank != "-" else "-", "trend": "Leaderboard"},
    ]


def get_attempt_for_request(request, quiz):
    attempt_id = request.GET.get("attempt")
    attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz, is_submitted=True)
    if attempt_id:
        return attempts.filter(id=attempt_id).first()
    return attempts.order_by("-submitted_at", "-created_at").first()


def base_context(**extra):
    quizzes, quiz, questions, leaders = get_quiz_context()
    context = {
        "quizzes": quizzes,
        "quiz": quiz,
        "questions": questions,
        "leaders": leaders,
        "activity": ACTIVITY,
        "stats": extra.pop("stats", None),
    }
    request = extra.pop("request", None)
    if context["stats"] is None:
        context["stats"] = user_stats(request.user if request else None)
    context.update(extra)
    return context


def page(request, template, **extra):
    return render(request, template, base_context(request=request, **extra))


def home(request):
    return page(request, "pages/home.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    form=SignUpForm()
    if request.method == "POST":
        form = SignUpForm(
            {
                "name": request.POST.get("name", ""),
                "username": request.POST.get("email", ""),
                "email": request.POST.get("email", ""),
                "password1": request.POST.get("password", ""),
                "password2": request.POST.get("password", ""),
            }
        )
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("student_dashboard")
        print(form.errors)
        messages.error(request, "Please correct the signup form and try again.")
    return render(request, "auth/signup.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("student_dashboard")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data["user"])
            if not form.cleaned_data.get("remember"):
                request.session.set_expiry(0)
            messages.success(request, "Logged in successfully.")
            return redirect("student_dashboard")
        messages.error(request, "Invalid email or password.")
    return page(request, "auth/login.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out.")
    return page(request, "auth/logout.html")


def forgot_password(request):
    return page(request, "auth/forgot_password.html")


def reset_password(request):
    return page(request, "auth/reset_password.html")


def change_password(request):
    return page(request, "auth/change_password.html")


def email_verified(request):
    return page(request, "auth/email_verified.html")


@login_required(login_url="login")
def profile(request):
    return page(request, "auth/profile.html")


@login_required(login_url="login")
def edit_profile(request):
    return page(request, "auth/edit_profile.html")


def quiz_list(request):
    return page(request, "quiz/list.html")


def quiz_detail(request, slug):
    quiz_obj = get_object_or_404(Quiz.objects.select_related("category"), slug=slug, is_published=True)
    return page(request, "quiz/detail.html", quiz=serialize_quiz(quiz_obj))


def quiz_instructions(request, slug):
    quiz_obj = get_object_or_404(Quiz.objects.select_related("category"), slug=slug, is_published=True)
    return page(request, "quiz/instructions.html", quiz=serialize_quiz(quiz_obj))


@login_required(login_url="login")
def start_quiz(request, slug):
    quiz_obj = get_object_or_404(
        Quiz.objects.select_related("category").prefetch_related("questions__choices"),
        slug=slug,
        is_published=True,
    )
    questions = [serialize_question(question) for question in quiz_obj.questions.all()]
    return page(request, "quiz/start.html", quiz=serialize_quiz(quiz_obj), questions=questions)


@login_required(login_url="login")
@transaction.atomic
def submit_quiz(request, slug):
    if request.method != "POST":
        return redirect("start_quiz", slug=slug)

    quiz_obj = get_object_or_404(
        Quiz.objects.prefetch_related("questions__choices"),
        slug=slug,
        is_published=True,
    )
    questions = list(quiz_obj.questions.all())
    selected_answers = {}
    correct_answers = 0
    wrong_answers = 0
    skipped_answers = 0

    for question in questions:
        selected_choice_id = request.POST.get(f"question_{question.id}")
        selected_answers[str(question.id)] = selected_choice_id or ""
        correct_choice = question.choices.filter(is_correct=True).first()
        if not selected_choice_id:
            skipped_answers += 1
        elif correct_choice and str(correct_choice.id) == selected_choice_id:
            correct_answers += 1
        else:
            wrong_answers += 1

    total_questions = len(questions)
    percentage = Decimal("0.00")
    if total_questions:
        percentage = Decimal(correct_answers * 100 / total_questions).quantize(Decimal("0.01"))

    attempt = QuizAttempt.objects.create(
        user=request.user,
        quiz=quiz_obj,
        submitted_at=timezone.now(),
        selected_answers=selected_answers,
        score=correct_answers,
        total_questions=total_questions,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        skipped_answers=skipped_answers,
        percentage=percentage,
        is_submitted=True,
    )
    Result.objects.create(
        attempt=attempt,
        user=request.user,
        quiz=quiz_obj,
        score=correct_answers,
        percentage=percentage,
        correct_answers=correct_answers,
        wrong_answers=wrong_answers,
        skipped_answers=skipped_answers,
        passed=percentage >= 40,
    )
    entry, _ = Leaderboard.objects.get_or_create(user=request.user, quiz=quiz_obj)
    entry.attempts_count = QuizAttempt.objects.filter(user=request.user, quiz=quiz_obj, is_submitted=True).count()
    if percentage >= entry.best_percentage:
        entry.best_percentage = percentage
        entry.best_score = correct_answers
    entry.save()
    messages.success(request, "Quiz submitted successfully.")
    return redirect(f"{request.path.replace('/submit/', '/result/')}?attempt={attempt.id}")


@login_required(login_url="login")
def quiz_result(request, slug):
    quiz_obj = get_object_or_404(Quiz, slug=slug, is_published=True)
    attempt = get_attempt_for_request(request, quiz_obj)
    return page(request, "quiz/result.html", quiz=serialize_quiz(quiz_obj), attempt=attempt, result=getattr(attempt, "result", None))


@login_required(login_url="login")
def score_card(request, slug):
    quiz_obj = get_object_or_404(Quiz, slug=slug, is_published=True)
    attempt = get_attempt_for_request(request, quiz_obj)
    return page(request, "quiz/score_card.html", quiz=serialize_quiz(quiz_obj), attempt=attempt, result=getattr(attempt, "result", None))


@login_required(login_url="login")
def review_answers(request, slug):
    quiz_obj = get_object_or_404(Quiz.objects.prefetch_related("questions__choices"), slug=slug, is_published=True)
    attempt = get_attempt_for_request(request, quiz_obj)
    selected_answers = attempt.selected_answers if attempt else {}
    questions = [
        serialize_question(question, selected_answers.get(str(question.id)))
        for question in quiz_obj.questions.all()
    ]
    return page(request, "quiz/review_answers.html", quiz=serialize_quiz(quiz_obj), questions=questions, attempt=attempt)


def leaderboard(request):
    return page(request, "quiz/leaderboard.html")


@login_required(login_url="login")
def user_ranking(request):
    return page(request, "quiz/ranking.html")


@login_required(login_url="login")
def progress(request):
    return page(request, "quiz/progress.html")


@login_required(login_url="login")
def certificate(request):

    latest_result = (
        Result.objects.filter(user=request.user)
        .select_related("quiz")
        .order_by("-id")
        .first()
    )

    if not latest_result:
        messages.error(request, "No quiz attempt found.")
        return redirect("quiz_list")

    passed = latest_result.percentage >= 40

    context = {
        "result": latest_result,
        "passed": passed,
        "quiz": latest_result.quiz,
    }

    return render(request, "quiz/certificate.html", context)


@login_required(login_url="login")
def student_dashboard(request):
    return page(request, "dashboard/student.html")


def admin_dashboard(request):
    return page(request, "dashboard/admin.html")


def teacher_dashboard(request):
    return page(request, "dashboard/teacher.html")


def create_quiz(request):
    return page(request, "admin_features/create_quiz.html")


def add_questions(request):
    return page(request, "admin_features/add_questions.html")


def edit_quiz(request):
    return page(request, "admin_features/edit_quiz.html")


def delete_confirm(request):
    return page(request, "admin_features/delete_confirm.html")


def manage_users(request):
    return page(request, "admin_features/manage_users.html")


def manage_categories(request):
    return page(request, "admin_features/manage_categories.html")


def manage_leaderboard(request):
    return page(request, "admin_features/manage_leaderboard.html")


def about(request):
    return page(request, "pages/about.html")


def contact(request):
    return page(request, "pages/contact.html")


def faq(request):
    return page(request, "pages/faq.html")


def terms(request):
    return page(request, "pages/terms.html")


def privacy(request):
    return page(request, "pages/privacy.html")


def handler404(request, exception):
    return render(request, "errors/404.html", base_context(), status=404)


def handler500(request):
    return render(request, "errors/500.html", base_context(), status=500)
