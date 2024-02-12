from lsorm import Session, models

Session.configure(source="Settings")

question = models.Question

for q in question.objects.all():
    print(q.sid)
