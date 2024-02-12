from lsorm import Session, models

Session.configure(source="Settings")
Survey = models.Survey

survey = Survey.objects.filter(Survey.active == "Y").first()

sid = survey.sid

class_factory = models.ClassFactory(sid, models.Base)

users = class_factory.create_class(table="users")

for user in users.objects.all():
    print(user.full_name)