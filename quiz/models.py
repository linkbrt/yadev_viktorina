from django.db import models


class Quiz(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=150, unique=True)
    success_page = models.FileField(
        upload_to='pages/',
        blank=True, null=True,
    )
    questions = models.ManyToManyField("Question")

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.title


class QuestionType(models.Choices):
    CHOISE = 'choise'
    INPUT = 'input'


class Question(models.Model):

    quiz_model = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    content = models.TextField()
    image = models.ImageField(
        upload_to='question/',
        blank=True, null=True,
    )
    type = models.CharField(
        max_length=50,
        choices=QuestionType.choices,
        default=QuestionType.INPUT)

    def __str__(self):
        return self.content


class Answer(models.Model):

    content = models.CharField(max_length=100)
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class QuizState:
    def __init__(self, quiz_pk: int = 1,
                 question_index: int = 1,
                 max_index: int = 10,
                 passed: bool = False) -> None:
        self.quiz_pk = quiz_pk
        self.question_index = question_index
        self.max_index = max_index
        self.passed = passed

    # я уверен что переключение passed в двух местах это костыль
    # но я не знаю как сделать лучше -_-
    # p.s. хотя есть в этом какая-то логика но я вообще не уверен

    def next(self) -> None:
        if self.question_index < self.max_index:
            self.question_index += 1
            self.passed = not self.passed

    def step(self) -> None:
        self.passed = not self.passed

    def to_dict(self) -> dict:
        return {
            'quiz_pk': self.quiz_pk,
            'question_index': self.question_index,
            'max_index': self.max_index,
            'passed': self.passed,
        }

    @staticmethod
    def from_dict(data) -> 'QuizState':
        if not data:
            return QuizState()
        return QuizState(**data)
