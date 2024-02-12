from typing import Optional
import settings
from sqlalchemy import Column, Integer, Index, text, Text, DateTime, String, Boolean
#from sqlalchemy.dialects.mysql import LONGBLOB, MEDIUMTEXT, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.automap import automap_base
from lsorm import Session

PREFIX = settings.PREFIX


class Base(DeclarativeBase):
    objects = Session.query_property()

    @classmethod
    def columns(cls):
        return cls.__table__.columns.keys()

    @classmethod
    def get(cls, pk):
        return Session.get(cls, pk)


class ClassFactory:
    def __init__(self, sid, base_class):
        self.sid = sid
        self.base_class = base_class

    def create_class(self, type):
        """
        Users = create_user_class(239779)
        """
        if type == "users":
            table_name = f"{PREFIX}_tokens_{self.sid}"

            class Users(self.base_class):
                __tablename__ = table_name
                tid: Mapped[int] = mapped_column(primary_key=True)
                firstname: Mapped[Optional[str]]
                lastname: Mapped[Optional[str]]
                email: Mapped[Optional[str]]
                token: Mapped[Optional[str]]

                def __repr__(self) -> str:
                    return f"Users(table={self.__tablename__!r})"

                @property
                def full_name(self):
                    return self.firstname + " " + self.lastname

            return Users

        elif type == "answers":
            table_name = f"iso_survey_{self.sid}"

            Base = automap_base(declarative_base=self.base_class)
            Base.prepare()

            survey_cls = getattr(Base.classes, table_name)
            survey_cls.objects = Session.query_property()

            return survey_cls

        else:
            raise Exception("Type not valid")


class AnswerL10n(Base):
    __tablename__ = f"{PREFIX}_answer_l10ns"
    __table_args__ = (Index(f"{PREFIX}_answer_l10ns_idx", "aid", "language", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aid: Mapped[int] = mapped_column(Integer, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False) 
    language: Mapped[str] = mapped_column(String(20), nullable=False)

class Answer(Base):
    __tablename__ = f"{PREFIX}_answers"
    __table_args__ = (Index(f"{PREFIX}_answers_idx", "qid", "code", "scale_id", unique=True),)

    aid: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(5), nullable=False)
    sortorder: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    assessment_value: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    scale_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))

class ArchivedTableSetting(Base):
    __tablename__ = f"{PREFIX}_archived_table_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    survey_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tbl_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tbl_type: Mapped[str] = mapped_column(String(10), nullable=False)
    created: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    properties: Mapped[str] = mapped_column(Text, nullable=False)
    attributes: Mapped[str] = mapped_column(Text)

class Assessment(Base):
    __tablename__ = f"{PREFIX}_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    sid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, server_default=text("'0'"))
    scope: Mapped[str] = mapped_column(String(5), nullable=False)
    gid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, server_default=text("'0'"))
    name: Mapped[str] = mapped_column(Text, nullable=False)
    minimum: Mapped[str] = mapped_column(String(50), nullable=False)
    maximum: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)  # Assuming MEDIUMTEXT is equivalent to Text
    language: Mapped[str] = mapped_column(String(20), primary_key=True, nullable=False, server_default=text("'en'"))

class AssetVersion(Base):
    __tablename__ = f"{PREFIX}_asset_version"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)

class Box(Base):
    __tablename__ = f"{PREFIX}_boxes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    position: Mapped[int] = mapped_column(Integer)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    ico: Mapped[str] = mapped_column(String(255))
    desc: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[str] = mapped_column(Text, nullable=False)
    usergroup: Mapped[int] = mapped_column(Integer, nullable=False)

class Condition(Base):
    __tablename__ = f"{PREFIX}_conditions"

    cid: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, server_default=text("'0'"))
    cqid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, server_default=text("'0'"))
    cfieldname: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("''"))
    method: Mapped[str] = mapped_column(String(5), nullable=False, server_default=text("''"))
    value: Mapped[str] = mapped_column(String(255), nullable=False, server_default=text("''"))
    scenario: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'1'"))

# DefaultvalueL10n
class DefaultvalueL10n(Base):
    __tablename__ = f"{PREFIX}_defaultvalue_l10ns"
    __table_args__ = (Index(f"{PREFIX}_idx1_defaultvalue_ls", "dvid", "language"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dvid: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    language: Mapped[str] = mapped_column(String(20), nullable=False)
    defaultvalue: Mapped[str] = mapped_column(Text)

# Defaultvalue
class Defaultvalue(Base):
    __tablename__ = f"{PREFIX}_defaultvalues"
    __table_args__ = (Index(f"{PREFIX}_idx1_defaultvalue", "qid", "scale_id", "sqid", "specialtype"),)

    dvid: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    scale_id: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    sqid: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    specialtype: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("''"))

# ExpressionError
class ExpressionError(Base):
    __tablename__ = f"{PREFIX}_expression_errors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    errortime: Mapped[str] = mapped_column(String(50))
    sid: Mapped[int] = mapped_column(Integer)
    gid: Mapped[int] = mapped_column(Integer)
    qid: Mapped[int] = mapped_column(Integer)
    gseq: Mapped[int] = mapped_column(Integer)
    qseq: Mapped[int] = mapped_column(Integer)
    type: Mapped[str] = mapped_column(String(50))
    eqn: Mapped[str] = mapped_column(Text)
    prettyprint: Mapped[str] = mapped_column(Text)

# FailedEmail
class FailedEmail(Base):
    __tablename__ = f"{PREFIX}_failed_emails"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    surveyid: Mapped[int] = mapped_column(Integer, nullable=False)
    responseid: Mapped[int] = mapped_column(Integer, nullable=False)
    email_type: Mapped[str] = mapped_column(String(200), nullable=False)
    recipient: Mapped[str] = mapped_column(String(320), nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'en'"))
    error_message: Mapped[str] = mapped_column(Text)
    created: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), server_default=text("'SEND FAILED'"))
    updated: Mapped[DateTime] = mapped_column(DateTime)
    resend_vars: Mapped[str] = mapped_column(Text, nullable=False)

# FailedLoginAttempt
class FailedLoginAttempt(Base):
    __tablename__ = f"{PREFIX}_failed_login_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip: Mapped[str] = mapped_column(String(40), nullable=False)
    last_attempt: Mapped[str] = mapped_column(String(20), nullable=False)
    number_attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    is_frontend: Mapped[bool] = mapped_column(Boolean, nullable=False)  # Assuming TINYINT(1) is used as Boolean

# GroupL10n
class GroupL10n(Base):
    __tablename__ = f"{PREFIX}_group_l10ns"
    __table_args__ = (Index(f"{PREFIX}_idx1_group_ls", "gid", "language", unique=True),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gid: Mapped[int] = mapped_column(Integer, nullable=False)
    group_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text)  # Assuming MEDIUMTEXT is equivalent to Text
    language: Mapped[str] = mapped_column(String(20), nullable=False)

# Group
class Group(Base):
    __tablename__ = f"{PREFIX}_groups"

    gid: Mapped[int] = mapped_column(Integer, primary_key=True)
    sid: Mapped[int] = mapped_column(Integer, nullable=False, index=True, server_default=text("'0'"))
    group_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    randomization_group: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("''"))
    grelevance: Mapped[str] = mapped_column(Text)

# LabelL10n
class LabelL10n(Base):
    __tablename__ = f"{PREFIX}_label_l10ns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'en'"))

# Label
class Label(Base):
    __tablename__ = f"{PREFIX}_labels"
    __table_args__ = (
        Index(f"{PREFIX}_idx5_labels", "lid", "code", unique=True),
        Index(f"{PREFIX}_idx4_labels", "lid", "sortorder"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lid: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    code: Mapped[str] = mapped_column(String(20), nullable=False, index=True, server_default=text("''"))
    sortorder: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    assessment_value: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'0'"))

# Labelset
class Labelset(Base):
    __tablename__ = f"{PREFIX}_labelsets"

    lid: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_name: Mapped[str] = mapped_column(String(100), nullable=False, server_default=text("''"))
    languages: Mapped[str] = mapped_column(String(255), nullable=False)

# MapTutorialUser
class MapTutorialUser(Base):
    __tablename__ = f"{PREFIX}_map_tutorial_users"

    tid: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    uid: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    taken: Mapped[int] = mapped_column(Integer, server_default=text("'1'"))

# Message
class Message(Base):
    __tablename__ = f"{PREFIX}_message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    language: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False, server_default=text("''"))
    translation: Mapped[str] = mapped_column(Text)

# Notification
class Notification(Base):
    __tablename__ = f"{PREFIX}_notifications"
    __table_args__ = (Index(f"{PREFIX}_notifications_pk", "entity", "entity_id", "status"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity: Mapped[str] = mapped_column(String(15), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)  # Assuming MEDIUMTEXT is equivalent to Text
    status: Mapped[str] = mapped_column(String(15), nullable=False, server_default=text("'new'"))
    importance: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("'1'"))
    display_class: Mapped[str] = mapped_column(String(31), server_default=text("'default'"))
    hash: Mapped[str] = mapped_column(String(64), index=True)
    created: Mapped[DateTime] = mapped_column(DateTime)
    first_read: Mapped[DateTime] = mapped_column(DateTime)

# ParticipantAttribute
class ParticipantAttribute(Base):
    __tablename__ = f"{PREFIX}_participant_attribute"

    participant_id: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    attribute_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)

# ParticipantAttributeName
class ParticipantAttributeName(Base):
    __tablename__ = f"{PREFIX}_participant_attribute_names"
    __table_args__ = (
        Index(
            f"{PREFIX}_idx_participant_attribute_names",
            "attribute_id",
            "attribute_type",
        ),
    )

    attribute_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    attribute_type: Mapped[str] = mapped_column(String(4), primary_key=True, nullable=False)
    defaultname: Mapped[str] = mapped_column(String(255), nullable=False)
    visible: Mapped[str] = mapped_column(String(5), nullable=False)
    encrypted: Mapped[str] = mapped_column(String(5), nullable=False)
    core_attribute: Mapped[str] = mapped_column(String(5), nullable=False)

# ParticipantAttributeNamesLang
class ParticipantAttributeNamesLang(Base):
    __tablename__ = f"{PREFIX}_participant_attribute_names_lang"

    attribute_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    attribute_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lang: Mapped[str] = mapped_column(String(20), primary_key=True, nullable=False)

# ParticipantAttributeValue
class ParticipantAttributeValue(Base):
    __tablename__ = f"{PREFIX}_participant_attribute_values"

    value_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)  # Assuming MEDIUMTEXT is equivalent to Text


class ParticipantShare(Base):
    __tablename__ = f"{PREFIX}_participant_shares"

    participant_id = Column(VARCHAR(50), primary_key=True, nullable=False)
    share_uid = Column(Integer, primary_key=True, nullable=False)
    date_added = Column(DateTime, nullable=False)
    can_edit = Column(VARCHAR(5), nullable=False)


class Participant(Base):
    __tablename__ = f"{PREFIX}_participants"

    participant_id = Column(VARCHAR(50), primary_key=True)
    firstname = Column(TEXT)
    lastname = Column(TEXT)
    email = Column(TEXT)
    language = Column(VARCHAR(40), index=True)
    blacklisted = Column(VARCHAR(1), nullable=False)
    owner_uid = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    created = Column(DateTime)
    modified = Column(DateTime)
    
    def __repr__(self) -> str:
        return f"Participant(table={self.__tablename__!r})"

    @property
    def full_name(self):
        return self.firstname + " " + self.lastname

class Permission(Base):
    __tablename__ = f"{PREFIX}_permissions"
    __table_args__ = (
        Index(
            f"{PREFIX}_idx1_permissions",
            "entity_id",
            "entity",
            "permission",
            "uid",
            unique=True,
        ),
    )

    id = Column(Integer, primary_key=True)
    entity = Column(VARCHAR(50), nullable=False)
    entity_id = Column(Integer, nullable=False)
    uid = Column(Integer, nullable=False)
    permission = Column(VARCHAR(100), nullable=False)
    create_p = Column(Integer, nullable=False, server_default=text("'0'"))
    read_p = Column(Integer, nullable=False, server_default=text("'0'"))
    update_p = Column(Integer, nullable=False, server_default=text("'0'"))
    delete_p = Column(Integer, nullable=False, server_default=text("'0'"))
    import_p = Column(Integer, nullable=False, server_default=text("'0'"))
    export_p = Column(Integer, nullable=False, server_default=text("'0'"))


class Permissiontemplate(Base):
    __tablename__ = f"{PREFIX}_permissiontemplates"

    ptid = Column(Integer, primary_key=True)
    name = Column(VARCHAR(127), nullable=False, unique=True)
    description = Column(TEXT)
    renewed_last = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, nullable=False)


class PluginSetting(Base):
    __tablename__ = f"{PREFIX}_plugin_settings"

    id = Column(Integer, primary_key=True)
    plugin_id = Column(Integer, nullable=False)
    model = Column(VARCHAR(50))
    model_id = Column(Integer)
    key = Column(VARCHAR(50), nullable=False)
    value = Column(MEDIUMTEXT)


class Plugin(Base):
    __tablename__ = f"{PREFIX}_plugins"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    plugin_type = Column(VARCHAR(6), server_default=text("'user'"))
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    priority = Column(Integer, nullable=False, server_default=text("'0'"))
    version = Column(VARCHAR(32))
    load_error = Column(Integer, server_default=text("'0'"))
    load_error_message = Column(TEXT)


class QuestionAttribute(Base):
    __tablename__ = f"{PREFIX}_question_attributes"

    qaid = Column(Integer, primary_key=True)
    qid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    attribute = Column(VARCHAR(50), index=True)
    value = Column(MEDIUMTEXT)
    language = Column(VARCHAR(20))


class QuestionL10n(Base):
    __tablename__ = f"{PREFIX}_question_l10ns"
    __table_args__ = (Index(f"{PREFIX}_idx1_question_ls", "qid", "language", unique=True),)

    id = Column(Integer, primary_key=True)
    qid = Column(Integer, nullable=False)
    question = Column(MEDIUMTEXT, nullable=False)
    help = Column(MEDIUMTEXT)
    script = Column(TEXT)
    language = Column(VARCHAR(20), nullable=False)


class QuestionTheme(Base):
    __tablename__ = f"{PREFIX}_question_themes"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(150), nullable=False, index=True)
    visible = Column(VARCHAR(1))
    xml_path = Column(VARCHAR(255))
    image_path = Column(VARCHAR(255))
    title = Column(VARCHAR(100), nullable=False)
    creation_date = Column(DateTime)
    author = Column(VARCHAR(150))
    author_email = Column(VARCHAR(255))
    author_url = Column(VARCHAR(255))
    copyright = Column(TEXT)
    license = Column(TEXT)
    version = Column(VARCHAR(45))
    api_version = Column(VARCHAR(45), nullable=False)
    description = Column(TEXT)
    last_update = Column(DateTime)
    owner_id = Column(Integer)
    theme_type = Column(VARCHAR(150))
    question_type = Column(VARCHAR(150), nullable=False)
    core_theme = Column(TINYINT(1))
    extends = Column(VARCHAR(150))
    group = Column(VARCHAR(150))
    settings = Column(TEXT)


class Question(Base):
    __tablename__ = f"{PREFIX}_questions"

    qid = Column(Integer, primary_key=True)
    parent_qid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    sid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    gid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    type = Column(VARCHAR(30), nullable=False, index=True, server_default=text("'T'"))
    title = Column(VARCHAR(20), nullable=False, index=True, server_default=text("''"))
    preg = Column(TEXT)
    other = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    mandatory = Column(VARCHAR(1))
    encrypted = Column(VARCHAR(1), server_default=text("'N'"))
    question_order = Column(Integer, nullable=False)
    scale_id = Column(Integer, nullable=False, server_default=text("'0'"))
    same_default = Column(Integer, nullable=False, server_default=text("'0'"))
    relevance = Column(TEXT)
    question_theme_name = Column(VARCHAR(150))
    modulename = Column(VARCHAR(255))
    same_script = Column(Integer, nullable=False, server_default=text("'0'"))
    
    @property
    def get_id(self):
        base_id = f"{self.sid}X{self.gid}X"
        if self.type in ["T", "M", "X"]:
            base_id += f"{self.parent_qid}{self.title}"
        elif self.parent_qid == 0:
            base_id = "group"
        else:
            base_id += f"{self.qid}"
        return base_id

class Quota(Base):
    __tablename__ = f"{PREFIX}_quota"

    id = Column(Integer, primary_key=True)
    sid = Column(Integer, index=True)
    name = Column(VARCHAR(255))
    qlimit = Column(Integer)
    action = Column(Integer)
    active = Column(Integer, nullable=False, server_default=text("'1'"))
    autoload_url = Column(Integer, nullable=False, server_default=text("'0'"))


class QuotaLanguagesetting(Base):
    __tablename__ = f"{PREFIX}_quota_languagesettings"

    quotals_id = Column(Integer, primary_key=True)
    quotals_quota_id = Column(Integer, nullable=False, server_default=text("'0'"))
    quotals_language = Column(VARCHAR(45), nullable=False, server_default=text("'en'"))
    quotals_name = Column(VARCHAR(255))
    quotals_message = Column(MEDIUMTEXT, nullable=False)
    quotals_url = Column(VARCHAR(255))
    quotals_urldescrip = Column(VARCHAR(255))


class QuotaMember(Base):
    __tablename__ = f"{PREFIX}_quota_members"
    __table_args__ = (
        Index(
            f"{PREFIX}_idx1_quota_members",
            "sid",
            "qid",
            "quota_id",
            "code",
            unique=True,
        ),
    )

    id = Column(Integer, primary_key=True)
    sid = Column(Integer)
    qid = Column(Integer)
    quota_id = Column(Integer)
    code = Column(VARCHAR(11))


class SavedControl(Base):
    __tablename__ = f"{PREFIX}_saved_control"

    scid = Column(Integer, primary_key=True)
    sid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    srid = Column(Integer, nullable=False, index=True, server_default=text("'0'"))
    identifier = Column(TEXT, nullable=False)
    access_code = Column(TEXT, nullable=False)
    email = Column(VARCHAR(192))
    ip = Column(TEXT, nullable=False)
    saved_thisstep = Column(TEXT, nullable=False)
    status = Column(VARCHAR(1), nullable=False, server_default=text("''"))
    saved_date = Column(DateTime, nullable=False)
    refurl = Column(TEXT)


class Session(Base):
    __tablename__ = f"{PREFIX}_sessions"

    id = Column(VARCHAR(32), primary_key=True)
    expire = Column(Integer, index=True)
    data = Column(LONGBLOB)


class SettingsGlobal(Base):
    __tablename__ = f"{PREFIX}_settings_global"

    stg_name = Column(VARCHAR(50), primary_key=True, server_default=text("''"))
    stg_value = Column(MEDIUMTEXT, nullable=False)


class SettingsUser(Base):
    __tablename__ = f"{PREFIX}_settings_user"

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False, index=True)
    entity = Column(VARCHAR(15), index=True)
    entity_id = Column(VARCHAR(31), index=True)
    stg_name = Column(VARCHAR(63), nullable=False, index=True)
    stg_value = Column(MEDIUMTEXT)


class SourceMessage(Base):
    __tablename__ = f"{PREFIX}_source_message"

    id = Column(Integer, primary_key=True)
    category = Column(VARCHAR(35))
    message = Column(TEXT)

class SurveyLink(Base):
    __tablename__ = f"{PREFIX}_survey_links"

    participant_id = Column(VARCHAR(50), primary_key=True, nullable=False)
    token_id = Column(Integer, primary_key=True, nullable=False)
    survey_id = Column(Integer, primary_key=True, nullable=False)
    date_created = Column(DateTime)
    date_invited = Column(DateTime)
    date_completed = Column(DateTime)


class SurveyUrlParameter(Base):
    __tablename__ = f"{PREFIX}_survey_url_parameters"

    id = Column(Integer, primary_key=True)
    sid = Column(Integer, nullable=False)
    parameter = Column(VARCHAR(50), nullable=False)
    targetqid = Column(Integer)
    targetsqid = Column(Integer)


class Surveymenu(Base):
    __tablename__ = f"{PREFIX}_surveymenu"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer)
    survey_id = Column(Integer)
    user_id = Column(Integer)
    name = Column(VARCHAR(128), unique=True)
    ordering = Column(Integer, server_default=text("'0'"))
    level = Column(Integer, server_default=text("'0'"))
    title = Column(VARCHAR(168), nullable=False, index=True, server_default=text("''"))
    position = Column(VARCHAR(192), nullable=False, server_default=text("'side'"))
    description = Column(TEXT)
    showincollapse = Column(Integer, server_default=text("'0'"))
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    changed_at = Column(DateTime)
    changed_by = Column(Integer, nullable=False, server_default=text("'0'"))
    created_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, server_default=text("'0'"))


class SurveymenuEntry(Base):
    __tablename__ = f"{PREFIX}_surveymenu_entries"

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, index=True)
    user_id = Column(Integer)
    ordering = Column(Integer, server_default=text("'0'"))
    name = Column(VARCHAR(168), unique=True, server_default=text("''"))
    title = Column(VARCHAR(168), nullable=False, server_default=text("''"))
    menu_title = Column(VARCHAR(168), nullable=False, index=True, server_default=text("''"))
    menu_description = Column(TEXT)
    menu_icon = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    menu_icon_type = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    menu_class = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    menu_link = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    action = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    template = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    partial = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    classes = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    permission = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    permission_grade = Column(VARCHAR(192))
    data = Column(MEDIUMTEXT)
    getdatamethod = Column(VARCHAR(192), nullable=False, server_default=text("''"))
    language = Column(VARCHAR(32), nullable=False, server_default=text("'en-GB'"))
    showincollapse = Column(Integer, server_default=text("'0'"))
    active = Column(Integer, nullable=False, server_default=text("'0'"))
    changed_at = Column(DateTime)
    changed_by = Column(Integer, nullable=False, server_default=text("'0'"))
    created_at = Column(DateTime)
    created_by = Column(Integer, nullable=False, server_default=text("'0'"))


class Survey(Base):
    __tablename__ = f"{PREFIX}_surveys"

    sid = Column(Integer, primary_key=True)
    owner_id = Column(Integer, nullable=False, index=True)
    gsid = Column(Integer, index=True, server_default=text("'1'"))
    admin = Column(VARCHAR(50))
    active = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    expires = Column(DateTime)
    startdate = Column(DateTime)
    adminemail = Column(VARCHAR(254))
    anonymized = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    format = Column(VARCHAR(1))
    savetimings = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    template = Column(VARCHAR(100), server_default=text("'default'"))
    language = Column(VARCHAR(50))
    additional_languages = Column(TEXT)
    datestamp = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    usecookie = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowregister = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowsave = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    autonumber_start = Column(Integer, nullable=False, server_default=text("'0'"))
    autoredirect = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowprev = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    printanswers = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    ipaddr = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    ipanonymize = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    refurl = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    datecreated = Column(DateTime)
    showsurveypolicynotice = Column(Integer, server_default=text("'0'"))
    publicstatistics = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    publicgraphs = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    listpublic = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    htmlemail = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    sendconfirmation = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    tokenanswerspersistence = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    assessments = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    usecaptcha = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    usetokens = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    bounce_email = Column(VARCHAR(254))
    attributedescriptions = Column(MEDIUMTEXT)
    emailresponseto = Column(TEXT)
    emailnotificationto = Column(TEXT)
    tokenlength = Column(Integer, nullable=False, server_default=text("'15'"))
    showxquestions = Column(VARCHAR(1), server_default=text("'Y'"))
    showgroupinfo = Column(VARCHAR(1), server_default=text("'B'"))
    shownoanswer = Column(VARCHAR(1), server_default=text("'Y'"))
    showqnumcode = Column(VARCHAR(1), server_default=text("'X'"))
    bouncetime = Column(Integer)
    bounceprocessing = Column(VARCHAR(1), server_default=text("'N'"))
    bounceaccounttype = Column(VARCHAR(4))
    bounceaccounthost = Column(VARCHAR(200))
    bounceaccountpass = Column(TEXT)
    bounceaccountencryption = Column(VARCHAR(3))
    bounceaccountuser = Column(VARCHAR(200))
    showwelcome = Column(VARCHAR(1), server_default=text("'Y'"))
    showprogress = Column(VARCHAR(1), server_default=text("'Y'"))
    questionindex = Column(Integer, nullable=False, server_default=text("'0'"))
    navigationdelay = Column(Integer, nullable=False, server_default=text("'0'"))
    nokeyboard = Column(VARCHAR(1), server_default=text("'N'"))
    alloweditaftercompletion = Column(VARCHAR(1), server_default=text("'N'"))
    googleanalyticsstyle = Column(VARCHAR(1))
    googleanalyticsapikey = Column(VARCHAR(25))
    tokenencryptionoptions = Column(TEXT)


class SurveysGroup(Base):
    __tablename__ = f"{PREFIX}_surveys_groups"

    gsid = Column(Integer, primary_key=True)
    name = Column(VARCHAR(45), nullable=False, index=True)
    title = Column(VARCHAR(100), index=True)
    template = Column(VARCHAR(128), server_default=text("'default'"))
    description = Column(TEXT)
    sortorder = Column(Integer, nullable=False)
    owner_id = Column(Integer)
    parent_id = Column(Integer)
    alwaysavailable = Column(TINYINT(1))
    created = Column(DateTime)
    modified = Column(DateTime)
    created_by = Column(Integer, nullable=False)


class SurveysGroupsetting(Base):
    __tablename__ = f"{PREFIX}_surveys_groupsettings"

    gsid = Column(Integer, primary_key=True)
    owner_id = Column(Integer)
    admin = Column(VARCHAR(50))
    adminemail = Column(VARCHAR(254))
    anonymized = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    format = Column(VARCHAR(1))
    savetimings = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    template = Column(VARCHAR(100), server_default=text("'default'"))
    datestamp = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    usecookie = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowregister = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowsave = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    autonumber_start = Column(Integer, server_default=text("'0'"))
    autoredirect = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    allowprev = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    printanswers = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    ipaddr = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    ipanonymize = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    refurl = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    showsurveypolicynotice = Column(Integer, server_default=text("'0'"))
    publicstatistics = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    publicgraphs = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    listpublic = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    htmlemail = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    sendconfirmation = Column(VARCHAR(1), nullable=False, server_default=text("'Y'"))
    tokenanswerspersistence = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    assessments = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    usecaptcha = Column(VARCHAR(1), nullable=False, server_default=text("'N'"))
    bounce_email = Column(VARCHAR(254))
    attributedescriptions = Column(TEXT)
    emailresponseto = Column(TEXT)
    emailnotificationto = Column(TEXT)
    tokenlength = Column(Integer, server_default=text("'15'"))
    showxquestions = Column(VARCHAR(1), server_default=text("'Y'"))
    showgroupinfo = Column(VARCHAR(1), server_default=text("'B'"))
    shownoanswer = Column(VARCHAR(1), server_default=text("'Y'"))
    showqnumcode = Column(VARCHAR(1), server_default=text("'X'"))
    showwelcome = Column(VARCHAR(1), server_default=text("'Y'"))
    showprogress = Column(VARCHAR(1), server_default=text("'Y'"))
    questionindex = Column(Integer, server_default=text("'0'"))
    navigationdelay = Column(Integer, server_default=text("'0'"))
    nokeyboard = Column(VARCHAR(1), server_default=text("'N'"))
    alloweditaftercompletion = Column(VARCHAR(1), server_default=text("'N'"))


class SurveysLanguagesetting(Base):
    __tablename__ = f"{PREFIX}_surveys_languagesettings"

    surveyls_survey_id = Column(Integer, primary_key=True, nullable=False)
    surveyls_language = Column(VARCHAR(45), primary_key=True, nullable=False, server_default=text("'en'"))
    surveyls_title = Column(VARCHAR(200), nullable=False, index=True)
    surveyls_description = Column(MEDIUMTEXT)
    surveyls_welcometext = Column(MEDIUMTEXT)
    surveyls_endtext = Column(MEDIUMTEXT)
    surveyls_policy_notice = Column(MEDIUMTEXT)
    surveyls_policy_error = Column(TEXT)
    surveyls_policy_notice_label = Column(VARCHAR(192))
    surveyls_url = Column(TEXT)
    surveyls_urldescription = Column(VARCHAR(255))
    surveyls_email_invite_subj = Column(VARCHAR(255))
    surveyls_email_invite = Column(MEDIUMTEXT)
    surveyls_email_remind_subj = Column(VARCHAR(255))
    surveyls_email_remind = Column(MEDIUMTEXT)
    surveyls_email_register_subj = Column(VARCHAR(255))
    surveyls_email_register = Column(MEDIUMTEXT)
    surveyls_email_confirm_subj = Column(VARCHAR(255))
    surveyls_email_confirm = Column(MEDIUMTEXT)
    surveyls_dateformat = Column(Integer, nullable=False, server_default=text("'1'"))
    surveyls_attributecaptions = Column(TEXT)
    surveyls_alias = Column(VARCHAR(100))
    email_admin_notification_subj = Column(VARCHAR(255))
    email_admin_notification = Column(MEDIUMTEXT)
    email_admin_responses_subj = Column(VARCHAR(255))
    email_admin_responses = Column(MEDIUMTEXT)
    surveyls_numberformat = Column(Integer, nullable=False, server_default=text("'0'"))
    attachments = Column(TEXT)


class TemplateConfiguration(Base):
    __tablename__ = f"{PREFIX}_template_configuration"

    id = Column(Integer, primary_key=True)
    template_name = Column(VARCHAR(150), nullable=False, index=True)
    sid = Column(Integer, index=True)
    gsid = Column(Integer, index=True)
    uid = Column(Integer, index=True)
    files_css = Column(TEXT)
    files_js = Column(TEXT)
    files_print_css = Column(TEXT)
    options = Column(TEXT)
    cssframework_name = Column(VARCHAR(45))
    cssframework_css = Column(MEDIUMTEXT)
    cssframework_js = Column(MEDIUMTEXT)
    packages_to_load = Column(TEXT)
    packages_ltr = Column(TEXT)
    packages_rtl = Column(TEXT)


class Template(Base):
    __tablename__ = f"{PREFIX}_templates"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(150), nullable=False, index=True)
    folder = Column(VARCHAR(45))
    title = Column(VARCHAR(100), nullable=False, index=True)
    creation_date = Column(DateTime)
    author = Column(VARCHAR(150))
    author_email = Column(VARCHAR(255))
    author_url = Column(VARCHAR(255))
    copyright = Column(TEXT)
    license = Column(MEDIUMTEXT)
    version = Column(VARCHAR(45))
    api_version = Column(VARCHAR(45), nullable=False)
    view_folder = Column(VARCHAR(45), nullable=False)
    files_folder = Column(VARCHAR(45), nullable=False)
    description = Column(MEDIUMTEXT)
    last_update = Column(DateTime)
    owner_id = Column(Integer, index=True)
    extends = Column(VARCHAR(150), index=True)


class Tokens239779(Base):
    __tablename__ = f"{PREFIX}_tokens_239779"

    tid = Column(Integer, primary_key=True)
    participant_id = Column(VARCHAR(50))
    firstname = Column(TEXT)
    lastname = Column(TEXT)
    email = Column(TEXT, index=True)
    emailstatus = Column(TEXT)
    token = Column(VARCHAR(36), index=True)
    language = Column(VARCHAR(25))
    blacklisted = Column(VARCHAR(17))
    sent = Column(VARCHAR(17), server_default=text("'N'"))
    remindersent = Column(VARCHAR(17), server_default=text("'N'"))
    remindercount = Column(Integer, server_default=text("'0'"))
    completed = Column(VARCHAR(17), server_default=text("'N'"))
    usesleft = Column(Integer, server_default=text("'1'"))
    validfrom = Column(DateTime)
    validuntil = Column(DateTime)
    mpid = Column(Integer)


class TutorialEntry(Base):
    __tablename__ = f"{PREFIX}_tutorial_entries"

    teid = Column(Integer, primary_key=True)
    ordering = Column(Integer)
    title = Column(TEXT)
    content = Column(MEDIUMTEXT)
    settings = Column(MEDIUMTEXT)


class TutorialEntryRelation(Base):
    __tablename__ = f"{PREFIX}_tutorial_entry_relation"

    teid = Column(Integer, primary_key=True, nullable=False)
    tid = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, index=True)
    sid = Column(Integer, index=True)


class Tutorial(Base):
    __tablename__ = f"{PREFIX}_tutorials"

    tid = Column(Integer, primary_key=True)
    name = Column(VARCHAR(128), unique=True)
    title = Column(VARCHAR(192))
    icon = Column(VARCHAR(64))
    description = Column(TEXT)
    active = Column(Integer, server_default=text("'0'"))
    settings = Column(MEDIUMTEXT)
    permission = Column(VARCHAR(128), nullable=False)
    permission_grade = Column(VARCHAR(128), nullable=False)


class UserGroup(Base):
    __tablename__ = f"{PREFIX}_user_groups"

    ugid = Column(Integer, primary_key=True)
    name = Column(VARCHAR(20), nullable=False, unique=True)
    description = Column(TEXT, nullable=False)
    owner_id = Column(Integer, nullable=False)


class UserInGroup(Base):
    __tablename__ = f"{PREFIX}_user_in_groups"

    ugid = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, primary_key=True, nullable=False)


class UserInPermissionrole(Base):
    __tablename__ = f"{PREFIX}_user_in_permissionrole"

    ptid = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, primary_key=True, nullable=False)


class User(Base):
    __tablename__ = f"{PREFIX}_users"

    uid = Column(Integer, primary_key=True)
    users_name = Column(VARCHAR(64), nullable=False, unique=True, server_default=text("''"))
    password = Column(TEXT, nullable=False)
    full_name = Column(VARCHAR(50), nullable=False)
    parent_id = Column(Integer, nullable=False)
    lang = Column(VARCHAR(20))
    email = Column(VARCHAR(192), index=True)
    htmleditormode = Column(VARCHAR(7), server_default=text("'default'"))
    templateeditormode = Column(VARCHAR(7), nullable=False, server_default=text("'default'"))
    questionselectormode = Column(VARCHAR(7), nullable=False, server_default=text("'default'"))
    one_time_pw = Column(TEXT)
    dateformat = Column(Integer, nullable=False, server_default=text("'1'"))
    last_login = Column(DateTime)
    created = Column(DateTime)
    modified = Column(DateTime)
    validation_key = Column(VARCHAR(38))
    validation_key_expiration = Column(DateTime)
    last_forgot_email_password = Column(DateTime)
    expires = Column(DateTime)
