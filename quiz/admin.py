from django.contrib import admin

from .models import Category, Choice, Leaderboard, Question, Quiz, QuizAttempt, Result


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4
    max_num = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "duration_minutes", "is_published")
    list_filter = ("category", "level", "is_published")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "order", "short_text", "marks")
    list_filter = ("quiz__category", "quiz")
    search_fields = ("text", "explanation")
    inlines = [ChoiceInline]

    def short_text(self, obj):
        return obj.text[:70]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")
    list_filter = ("is_correct", "question__quiz")
    search_fields = ("text",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "percentage", "is_submitted", "submitted_at")
    list_filter = ("is_submitted", "quiz", "quiz__category")
    search_fields = ("user__username", "user__email", "quiz__title")
    readonly_fields = ("selected_answers",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "score", "percentage", "passed", "created_at")
    list_filter = ("passed", "quiz", "quiz__category")
    search_fields = ("user__username", "user__email", "quiz__title")


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "best_score", "best_percentage", "attempts_count")
    list_filter = ("quiz", "quiz__category")
    search_fields = ("user__username", "user__email", "quiz__title")
