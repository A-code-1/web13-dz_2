from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
import random
from tqdm import tqdm

fake = Faker()

class Command(BaseCommand):
    help = 'Fills database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Filling ratio')

    def handle(self, *args, **options):
        ratio = options['ratio']
        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        self.stdout.write(f'Creating {num_users} users...')
        users = []
        for i in tqdm(range(num_users)):
            user = User.objects.create_user(
                username=fake.user_name() + str(i),
                password='password123'
            )
            profile = Profile.objects.create(user=user, nickname=user.username, avatar='avatars/default.png')
            users.append(profile)

        self.stdout.write(f'Creating {num_tags} tags...')
        tags = []
        for _ in tqdm(range(num_tags)):
            tags.append(Tag.objects.create(name=fake.word()))

        self.stdout.write(f'Creating {num_questions} questions...')
        questions = []
        for _ in tqdm(range(num_questions)):
            q = Question.objects.create(
                name=fake.sentence(nb_words=6),
                text=fake.paragraph(nb_sentences=3),
                profile=random.choice(users),
                likes_count=random.randint(0, 100)
            )
            q.tag.set(random.sample(tags, k=random.randint(1, 3)))
            questions.append(q)

        self.stdout.write(f'Creating {num_answers} answers...')
        answers = []
        for _ in tqdm(range(num_answers)):
            a = Answer.objects.create(
                text=fake.sentence(),
                profile=random.choice(users),
                question=random.choice(questions),
                likes_count=random.randint(0, 50)
            )
            answers.append(a)

        self.stdout.write(f'Creating {num_likes} likes...')
        for _ in tqdm(range(num_likes)):
            if random.choice([True, False]):
                try:
                    QuestionLike.objects.create(
                        question=random.choice(questions),
                        profile=random.choice(users)
                    )
                except:
                    pass
            else:
                try:
                    AnswerLike.objects.create(
                        answer=random.choice(answers),
                        profile=random.choice(users)
                    )
                except:
                    pass

        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))