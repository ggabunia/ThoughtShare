import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ThoughtShare.settings')

import django

django.setup()

from faker import Faker
from idea_app.models import *
import random
import string

fakegen = Faker()
categories = list(Category.objects.all())
for idea in Idea.objects.all():
    rand = random.randint(0,len(categories)-1)
    descr = fakegen.paragraph(nb_sentences=10)
    title = fakegen.sentence(nb_words=10, variable_nb_words=True)
    idea.i_title = title
    idea.i_description = descr
    idea.i_category = categories[rand]
    idea.save()
    
