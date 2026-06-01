from django.contrib import admin
from django.urls import path

from quiz import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
    path("change-password/", views.change_password, name="change_password"),
    path("email-verified/", views.email_verified, name="email_verified"),
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("quizzes/", views.quiz_list, name="quiz_list"),
    path("quizzes/<slug:slug>/", views.quiz_detail, name="quiz_detail"),
    path("quizzes/<slug:slug>/instructions/", views.quiz_instructions, name="quiz_instructions"),
    path("quizzes/<slug:slug>/start/", views.start_quiz, name="start_quiz"),
    path("quizzes/<slug:slug>/submit/", views.submit_quiz, name="submit_quiz"),
    path("quizzes/<slug:slug>/result/", views.quiz_result, name="quiz_result"),
    path("quizzes/<slug:slug>/score-card/", views.score_card, name="score_card"),
    path("quizzes/<slug:slug>/review/", views.review_answers, name="review_answers"),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("ranking/", views.user_ranking, name="user_ranking"),
    path("progress/", views.progress, name="progress"),
    path("certificate/", views.certificate, name="certificate"),
    path("dashboard/student/", views.student_dashboard, name="student_dashboard"),
    path("dashboard/admin/", views.admin_dashboard, name="admin_dashboard"),
    path("dashboard/teacher/", views.teacher_dashboard, name="teacher_dashboard"),
    path("manage/quizzes/create/", views.create_quiz, name="create_quiz"),
    path("manage/quizzes/add-questions/", views.add_questions, name="add_questions"),
    path("manage/quizzes/edit/", views.edit_quiz, name="edit_quiz"),
    path("manage/delete/", views.delete_confirm, name="delete_confirm"),
    path("manage/users/", views.manage_users, name="manage_users"),
    path("manage/categories/", views.manage_categories, name="manage_categories"),
    path("manage/leaderboard/", views.manage_leaderboard, name="manage_leaderboard"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("terms/", views.terms, name="terms"),
    path("privacy/", views.privacy, name="privacy"),
]

handler404 = "quiz.views.handler404"
handler500 = "quiz.views.handler500"
