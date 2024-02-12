from lsorm import Session, models

Session.configure(source="Settings")
Survey = models.Survey

survey = Survey.objects.filter(Survey.active == "Y").first()

sid = survey.sid

# The ClassFactory is used to fetch reponses and users from
# the dynamically created tables name <prefix>_survey_<sid>, <prefix>_tokens_<sid>
class_factory = models.ClassFactory(sid, models.Base)

users = class_factory.create_class(table="users")

for user in users.objects.all():
    print(user.full_name)
    
responses = class_factory.create_class("answers")

specific_column = "757291X16X48B02"

specific_column_object = responses.objects.filter(responses.token == user.token).first()

specific_column_object.get_columns(specific_column_object.columns()[:10])


getattr(specific_column_object, specific_column)