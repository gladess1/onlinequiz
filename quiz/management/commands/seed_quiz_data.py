from django.core.management.base import BaseCommand

from quiz.models import Category, Choice, Question, Quiz


SEED_DATA = {
    "Python": [
        ("Which keyword defines a function in Python?", ["func", "def", "function", "lambda"], "def", "Python uses def to declare named functions."),
        ("Which data type is immutable?", ["list", "dict", "tuple", "set"], "tuple", "Tuples cannot be changed after creation."),
        ("Which symbol is used for comments?", ["//", "#", "/* */", "<!-- -->"], "#", "Python uses # for single-line comments."),
        ("Which function displays output?", ["echo()", "display()", "print()", "printf()"], "print()", "print() displays output."),
        ("Which keyword creates a loop?", ["repeat", "loop", "for", "iterate"], "for", "for creates loops."),
        ("Which collection stores key-value pairs?", ["list", "tuple", "dict", "set"], "dict", "Dictionary stores key-value pairs."),
        ("Which operator is used for exponent?", ["^", "**", "//", "%"], "**", "Python uses ** for powers."),
        ("Which keyword handles exceptions?", ["catch", "try", "error", "final"], "try", "try handles exceptions."),
        ("Which method adds item to list?", ["push()", "append()", "insert()", "add()"], "append()", "append() adds items."),
        ("Which keyword imports modules?", ["include", "using", "import", "require"], "import", "import loads modules."),
    ],
    

    "Java": [
        ("Which method starts a Java application?", ["start()", "main()", "run()", "init()"], "main()", "The JVM calls the public static main method."),
        ("Which keyword creates inheritance?", ["inherits", "extends", "implements", "super"], "extends", "A class extends another class in Java inheritance."),
        ("Which keyword creates object?", ["class", "new", "this", "object"], "new", "new creates objects."),
        ("Java is which type language?", ["Compiled", "Interpreted", "Both", "None"], "Both", "Java uses compilation and JVM."),
        ("Which package is imported by default?", ["java.io", "java.lang", "java.util", "java.sql"], "java.lang", "java.lang is default."),
        ("Which symbol ends statements?", [".", ":", ";", ","], ";", "Java uses semicolon."),
        ("Which keyword prevents inheritance?", ["final", "static", "private", "protected"], "final", "final prevents extension."),
        ("Which loop executes at least once?", ["for", "while", "do while", "foreach"], "do while", "do while executes once."),
        ("Which keyword refers current object?", ["super", "self", "this", "current"], "this", "this refers current object."),
        ("Which method prints output?", ["System.out.print()", "echo()", "printf()", "println()"], "System.out.print()", "Used for output."),
    ],

    "C": [
        ("Which function prints output in C?", ["cout", "printf", "print", "echo"], "printf", "printf writes formatted output."),
        ("Which header supports printf?", ["stdio.h", "stdlib.h", "string.h", "math.h"], "stdio.h", "stdio.h declares standard input/output functions."),
        ("Which symbol is used for comments?", ["#", "//", "/* */", "<!-- -->"], "//", "C supports // comments."),
        ("Which keyword defines constant?", ["constant", "const", "fixed", "define"], "const", "const creates constants."),
        ("Which loop checks condition first?", ["do while", "while", "repeat", "foreach"], "while", "while checks first."),
        ("Which operator gives remainder?", ["/", "%", "*", "//"], "%", "Modulo gives remainder."),
        ("Which data type stores characters?", ["char", "string", "text", "varchar"], "char", "char stores characters."),
        ("Which function reads input?", ["scanf", "input", "cin", "read"], "scanf", "scanf reads input."),
        ("Which keyword exits loop?", ["skip", "exit", "break", "stop"], "break", "break exits loop."),
        ("C language was developed by?", ["Dennis Ritchie", "James Gosling", "Guido", "Bjarne"], "Dennis Ritchie", "Dennis created C."),
    ],
    

    "C++": [
        ("Which stream prints output?", ["cin", "cout", "printf", "cerrin"], "cout", "std::cout writes output."),
        ("Which feature allows same function name with different parameters?", ["Overloading", "Overriding", "Inheritance", "Encapsulation"], "Overloading", "Function overloading depends on parameter lists."),
        ("Which operator accesses class members?", [".", "->", "::", ":"], ".", "Dot accesses members."),
        ("Which keyword creates class?", ["define", "struct", "class", "object"], "class", "class creates classes."),
        ("Which concept hides data?", ["Inheritance", "Encapsulation", "Polymorphism", "Abstraction"], "Encapsulation", "Encapsulation hides data."),
        ("Which stream takes input?", ["cout", "scanf", "cin", "gets"], "cin", "cin reads input."),
        ("Who developed C++?", ["Dennis", "Bjarne", "James", "Guido"], "Bjarne", "Bjarne created C++."),
        ("Which symbol is scope resolution?", ["->", "::", ".", ":"], "::", "Scope resolution operator."),
        ("Which keyword inherits class?", ["extends", "inherits", ":", "public"], "public", "public used in inheritance."),
        ("Which function is constructor?", ["same as class name", "main()", "init()", "build()"], "same as class name", "Constructors match class name."),
    ],
    

    "JavaScript": [
        ("Which keyword declares a block-scoped variable?", ["var", "let", "define", "dim"], "let", "let creates block-scoped variables."),
        ("Which operator checks strict equality?", ["==", "===", "=", "!="], "===", "=== compares value and type."),
        ("Which method converts JSON string into object?", ["JSON.parse()", "JSON.stringify()", "JSON.object()", "JSON.convert()"], "JSON.parse()", "JSON.parse converts JSON text into JavaScript object."),
        ("Which symbol is used for comments in JavaScript?", ["//", "#", "<!-- -->", "**"], "//", "Double slash creates single line comments."),
        ("Which function prints output in browser console?", ["print()", "echo()", "console.log()", "write()"], "console.log()", "console.log displays output in browser console."),
        ("Which company developed JavaScript?", ["Microsoft", "Netscape", "Google", "Apple"], "Netscape", "JavaScript was originally developed by Netscape."),
        ("Which loop runs at least once?", ["for", "while", "do while", "foreach"], "do while", "do while executes once before checking condition."),
        ("Which keyword is used to define constant values?", ["let", "constant", "const", "fixed"], "const", "const creates constant variables."),
        ("Which array method adds item at the end?", ["push()", "pop()", "shift()", "concat()"], "push()", "push adds element to end of array."),
        ("Which event occurs when button is clicked?", ["onhover", "onclick", "onmouse", "onchange"], "onclick", "onclick triggers when user clicks element."),
    ],
    

    "Django": [
        ("Which file commonly stores URL patterns?", ["models.py", "urls.py", "views.py", "admin.py"], "urls.py", "URL patterns are declared in urls.py."),
        ("Which command creates migrations?", ["migrate", "makemigrations", "startapp", "collectstatic"], "makemigrations", "makemigrations creates migration files from model changes."),
        ("Which ORM is used in Django?", ["Hibernate", "Entity Framework", "Django ORM", "SQLAlchemy"], "Django ORM", "Django includes its own ORM."),
        ("Which command starts Django development server?", ["python runserver", "django start", "python manage.py runserver", "startserver"], "python manage.py runserver", "runserver starts local development server."),
        ("Which file contains app models?", ["views.py", "models.py", "forms.py", "admin.py"], "models.py", "Database models are written in models.py."),
        ("Which template syntax prints variable value?", ["{{ }}", "{% %}", "[[ ]]", "<%= %>"], "{{ }}", "Double curly braces display template variables."),
        ("Which command creates a Django app?", ["createapp", "django-admin", "python manage.py startapp", "newapp"], "python manage.py startapp", "startapp creates a Django application."),
        ("Which database is default in Django?", ["MySQL", "SQLite", "MongoDB", "Oracle"], "SQLite", "SQLite is default database in Django."),
        ("Which file handles app administration settings?", ["settings.py", "urls.py", "admin.py", "forms.py"], "admin.py", "admin.py registers models for admin panel."),
        ("Which decorator restricts page to logged in users?", ["@admin_only", "@secure", "@login_required", "@authenticated"], "@login_required", "@login_required allows only authenticated users."),
    ],
    

    "Data Structures": [
        ("Which structure follows LIFO?", ["Queue", "Stack", "Array", "Graph"], "Stack", "Stacks remove the most recently added item first."),
        ("Which structure follows FIFO?", ["Stack", "Queue", "Tree", "Heap"], "Queue", "Queues remove the earliest added item first."),
        ("Which data structure stores elements in key-value pairs?", ["Array", "Stack", "Dictionary", "Queue"], "Dictionary", "Dictionary stores data using key-value pairs."),
        ("Which traversal visits root first?", ["Postorder", "Inorder", "Preorder", "Levelorder"], "Preorder", "Preorder visits root before child nodes."),
        ("Which searching algorithm works on sorted arrays?", ["Linear Search", "Binary Search", "Bubble Search", "DFS"], "Binary Search", "Binary search requires sorted data."),
        ("Which sorting algorithm repeatedly swaps adjacent elements?", ["Merge Sort", "Quick Sort", "Bubble Sort", "Heap Sort"], "Bubble Sort", "Bubble sort swaps adjacent elements."),
        ("Which data structure uses nodes connected by pointers?", ["Array", "Linked List", "Stack", "Queue"], "Linked List", "Linked lists use nodes connected through pointers."),
        ("Which structure is used in recursion?", ["Queue", "Stack", "Tree", "Graph"], "Stack", "Function calls are stored in stack memory."),
        ("Which graph traversal uses queue?", ["DFS", "BFS", "Binary Search", "Recursion"], "BFS", "Breadth First Search uses queue."),
        ("Which tree has maximum two children?", ["Binary Tree", "Heap", "Graph", "Trie"], "Binary Tree", "Binary trees allow at most two child nodes."),
    ],
    
}


class Command(BaseCommand):
    help = "Seed quiz data"

    def handle(self, *args, **options):

        for category_name, questions in SEED_DATA.items():

            slug = category_name.lower().replace(" ", "-")

            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": category_name,
                    "description": f"{category_name} practice quizzes for exam preparation."
                },
            )

            if not created:
                category.name = category_name
                category.description = f"{category_name} practice quizzes for exam preparation."
                category.save()

            quiz_title = f"{category_name} Fundamentals"

            quiz = Quiz.objects.filter(title=quiz_title).first()

            if not quiz:
                quiz = Quiz.objects.create(
                    category=category,
                    title=quiz_title,
                    slug=f"{slug}-fundamentals",
                    description=f"Practice core {category_name} concepts with instant scoring and answer review.",
                    level="Beginner" if category_name in {"Python", "C", "JavaScript"} else "Intermediate",
                    duration_minutes=25,
                    is_published=True,
                )

            quiz.questions.all().delete()

            for index, (text, options_list, correct, explanation) in enumerate(questions, start=1):

                question = Question.objects.create(
                    quiz=quiz,
                    text=text,
                    explanation=explanation,
                    order=index
                )

                for option in options_list:
                    Choice.objects.create(
                        question=question,
                        text=option,
                        is_correct=(option == correct)
                    )

        self.stdout.write(
            self.style.SUCCESS("Seeded quiz data successfully.")
        )