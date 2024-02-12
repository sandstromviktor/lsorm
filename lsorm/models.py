from typing import Any, Optional, Type

from sqlalchemy import (
    Boolean,
    DateTime,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    text,
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import settings
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
    def __init__(self, sid: int, base_class: Type[Base]):
        self.sid: int = sid
        self.base_class: Type[Base] = base_class

    def create_class(self, table: str) -> Any:
        """
        Users = create_user_class(239779)
        """
        if table.lower() in ("users", "u", "participant", "participants"):
            table_name = f"{PREFIX}_tokens_{self.sid}"
            base_class: Type[Any] = self.base_class

            class Users(base_class):
                __tablename__ = table_name
                tid: Mapped[int] = mapped_column(primary_key=True)
                firstname: Mapped[Optional[str]]
                lastname: Mapped[Optional[str]]
                email: Mapped[Optional[str]]
                token: Mapped[Optional[str]]

                def __repr__(self) -> str:
                    return f"Users(table={self.__tablename__!r})"

                @property
                def full_name(self) -> str:
                    if self.firstname and self.lastname:
                        return str(self.firstname) + " " + str(self.lastname)
                    else:
                        return "No Name"

            return Users

        elif table.lower() in ("answers", "answer", "a", "reponse", "repsonses"):
            table_name = f"iso_survey_{self.sid}"

            Base = automap_base(declarative_base=self.base_class)
            Base.prepare(autoload_with=Session.get_bind())

            survey_cls = getattr(Base.classes, table_name)
            survey_cls.objects = Session.query_property()

            return survey_cls

        else:
            raise Exception("Type not valid")


class AnswerL10n(Base):
    __tablename__ = f"{PREFIX}_answer_l10ns"
    __table_args__ = (
        Index(f"{PREFIX}_answer_l10ns_idx", "aid", "language", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    aid: Mapped[int] = mapped_column(Integer, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(20), nullable=False)


class Answer(Base):
    __tablename__ = f"{PREFIX}_answers"
    __table_args__ = (
        Index(f"{PREFIX}_answers_idx", "qid", "code", "scale_id", unique=True),
    )

    aid: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[int] = mapped_column(Integer, nullable=False)
    code: Mapped[str] = mapped_column(String(5), nullable=False)
    sortorder: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    assessment_value: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    scale_id: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


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
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    scope: Mapped[str] = mapped_column(String(5), nullable=False)
    gid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    minimum: Mapped[str] = mapped_column(String(50), nullable=False)
    maximum: Mapped[str] = mapped_column(String(50), nullable=False)
    message: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # Assuming Text is equivalent to Text
    language: Mapped[str] = mapped_column(
        String(20),
        primary_key=True,
        nullable=False,
        server_default=text("'en'"),
    )


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
    qid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    cqid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    cfieldname: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default=text("''")
    )
    method: Mapped[str] = mapped_column(
        String(5), nullable=False, server_default=text("''")
    )
    value: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default=text("''")
    )
    scenario: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'1'")
    )


# DefaultvalueL10n
class DefaultvalueL10n(Base):
    __tablename__ = f"{PREFIX}_defaultvalue_l10ns"
    __table_args__ = (
        Index(f"{PREFIX}_idx1_defaultvalue_ls", "dvid", "language"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dvid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    language: Mapped[str] = mapped_column(String(20), nullable=False)
    defaultvalue: Mapped[str] = mapped_column(Text)


# Defaultvalue
class Defaultvalue(Base):
    __tablename__ = f"{PREFIX}_defaultvalues"
    __table_args__ = (
        Index(
            f"{PREFIX}_idx1_defaultvalue",
            "qid",
            "scale_id",
            "sqid",
            "specialtype",
        ),
    )

    dvid: Mapped[int] = mapped_column(Integer, primary_key=True)
    qid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    scale_id: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    sqid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    specialtype: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("''")
    )


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
    language: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'en'")
    )
    error_message: Mapped[str] = mapped_column(Text)
    created: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), server_default=text("'SEND FAILED'")
    )
    updated: Mapped[DateTime] = mapped_column(DateTime)
    resend_vars: Mapped[str] = mapped_column(Text, nullable=False)


# FailedLoginAttempt
class FailedLoginAttempt(Base):
    __tablename__ = f"{PREFIX}_failed_login_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip: Mapped[str] = mapped_column(String(40), nullable=False)
    last_attempt: Mapped[str] = mapped_column(String(20), nullable=False)
    number_attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    is_frontend: Mapped[bool] = mapped_column(
        Boolean, nullable=False
    )  # Assuming TINYINT(1) is used as Boolean


# GroupL10n
class GroupL10n(Base):
    __tablename__ = f"{PREFIX}_group_l10ns"
    __table_args__ = (
        Index(f"{PREFIX}_idx1_group_ls", "gid", "language", unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gid: Mapped[int] = mapped_column(Integer, nullable=False)
    group_name: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(
        Text
    )  # Assuming Text is equivalent to Text
    language: Mapped[str] = mapped_column(String(20), nullable=False)


# Group
class Group(Base):
    __tablename__ = f"{PREFIX}_groups"

    gid: Mapped[int] = mapped_column(Integer, primary_key=True)
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    group_order: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    randomization_group: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("''")
    )
    grelevance: Mapped[str] = mapped_column(Text)


# LabelL10n
class LabelL10n(Base):
    __tablename__ = f"{PREFIX}_label_l10ns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(
        String(20), nullable=False, server_default=text("'en'")
    )


# Label
class Label(Base):
    __tablename__ = f"{PREFIX}_labels"
    __table_args__ = (
        Index(f"{PREFIX}_idx5_labels", "lid", "code", unique=True),
        Index(f"{PREFIX}_idx4_labels", "lid", "sortorder"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lid: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    code: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, server_default=text("''")
    )
    sortorder: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    assessment_value: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


# Labelset
class Labelset(Base):
    __tablename__ = f"{PREFIX}_labelsets"

    lid: Mapped[int] = mapped_column(Integer, primary_key=True)
    label_name: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default=text("''")
    )
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
    language: Mapped[str] = mapped_column(
        String(50), primary_key=True, nullable=False, server_default=text("''")
    )
    translation: Mapped[str] = mapped_column(Text)


# Notification
class Notification(Base):
    __tablename__ = f"{PREFIX}_notifications"
    __table_args__ = (
        Index(f"{PREFIX}_notifications_pk", "entity", "entity_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity: Mapped[str] = mapped_column(String(15), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # Assuming Text is equivalent to Text
    status: Mapped[str] = mapped_column(
        String(15), nullable=False, server_default=text("'new'")
    )
    importance: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'1'")
    )
    display_class: Mapped[str] = mapped_column(
        String(31), server_default=text("'default'")
    )
    hash: Mapped[str] = mapped_column(String(64), index=True)
    created: Mapped[DateTime] = mapped_column(DateTime)
    first_read: Mapped[DateTime] = mapped_column(DateTime)


# ParticipantAttribute
class ParticipantAttribute(Base):
    __tablename__ = f"{PREFIX}_participant_attribute"

    participant_id: Mapped[str] = mapped_column(
        String(50), primary_key=True, nullable=False
    )
    attribute_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )
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

    attribute_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )
    attribute_type: Mapped[str] = mapped_column(
        String(4), primary_key=True, nullable=False
    )
    defaultname: Mapped[str] = mapped_column(String(255), nullable=False)
    visible: Mapped[str] = mapped_column(String(5), nullable=False)
    encrypted: Mapped[str] = mapped_column(String(5), nullable=False)
    core_attribute: Mapped[str] = mapped_column(String(5), nullable=False)


# ParticipantAttributeNamesLang
class ParticipantAttributeNamesLang(Base):
    __tablename__ = f"{PREFIX}_participant_attribute_names_lang"

    attribute_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )
    attribute_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lang: Mapped[str] = mapped_column(
        String(20), primary_key=True, nullable=False
    )


# ParticipantAttributeValue
class ParticipantAttributeValue(Base):
    __tablename__ = f"{PREFIX}_participant_attribute_values"

    value_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    attribute_id: Mapped[int] = mapped_column(Integer, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)


# ParticipantShare
class ParticipantShare(Base):
    __tablename__ = f"{PREFIX}_participant_shares"

    participant_id: Mapped[str] = mapped_column(
        String(50), primary_key=True, nullable=False
    )
    share_uid: Mapped[int] = mapped_column(
        Integer, primary_key=True, nullable=False
    )
    date_added: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    can_edit: Mapped[str] = mapped_column(String(5), nullable=False)


# Participant
class Participant(Base):
    __tablename__ = f"{PREFIX}_participants"

    participant_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    firstname: Mapped[str] = mapped_column(Text)
    lastname: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(40), index=True)
    blacklisted: Mapped[str] = mapped_column(String(1), nullable=False)
    owner_uid: Mapped[int] = mapped_column(Integer, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped[DateTime] = mapped_column(DateTime)
    modified: Mapped[DateTime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"Participant(table={self.__tablename__!r})"

    @property
    def full_name(self):
        return self.firstname + " " + self.lastname


# Permission
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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    uid: Mapped[int] = mapped_column(Integer, nullable=False)
    permission: Mapped[str] = mapped_column(String(100), nullable=False)
    create_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    read_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    update_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    delete_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    import_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    export_p: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


# Permissiontemplate
class Permissiontemplate(Base):
    __tablename__ = f"{PREFIX}_permissiontemplates"

    ptid: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)
    renewed_last: Mapped[DateTime] = mapped_column(DateTime)
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, nullable=False)


# PluginSetting
class PluginSetting(Base):
    __tablename__ = f"{PREFIX}_plugin_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plugin_id: Mapped[int] = mapped_column(Integer, nullable=False)
    model: Mapped[str] = mapped_column(String(50))
    model_id: Mapped[int] = mapped_column(Integer)
    key: Mapped[str] = mapped_column(String(50), nullable=False)
    value: Mapped[str] = mapped_column(Text)


class Plugin(Base):
    __tablename__ = f"{PREFIX}_plugins"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=False)
    plugin_type = mapped_column(String(6), server_default=text("'user'"))
    active = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    priority = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    version = mapped_column(String(32))
    load_error = mapped_column(Integer, server_default=text("'0'"))
    load_error_message = mapped_column(Text)


class QuestionAttribute(Base):
    __tablename__ = f"{PREFIX}_question_attributes"

    qaid = mapped_column(Integer, primary_key=True)
    qid = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    attribute = mapped_column(String(50), index=True)
    value = mapped_column(Text)
    language = mapped_column(String(20))


class QuestionL10n(Base):
    __tablename__ = f"{PREFIX}_question_l10ns"
    __table_args__ = (
        Index(f"{PREFIX}_idx1_question_ls", "qid", "language", unique=True),
    )

    id = mapped_column(Integer, primary_key=True)
    qid = mapped_column(Integer, nullable=False)
    question = mapped_column(Text, nullable=False)
    help = mapped_column(Text)
    script = mapped_column(Text)
    language = mapped_column(String(20), nullable=False)


class QuestionTheme(Base):
    __tablename__ = f"{PREFIX}_question_themes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    visible: Mapped[str] = mapped_column(String(1))
    xml_path: Mapped[str] = mapped_column(String(255))
    image_path: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    creation_date: Mapped[DateTime] = mapped_column(DateTime)
    author: Mapped[str] = mapped_column(String(150))
    author_email: Mapped[str] = mapped_column(String(255))
    author_url: Mapped[str] = mapped_column(String(255))
    copyright: Mapped[str] = mapped_column(Text)
    license: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(String(45))
    api_version: Mapped[str] = mapped_column(String(45), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    last_update: Mapped[DateTime] = mapped_column(DateTime)
    owner_id: Mapped[int] = mapped_column(Integer)
    theme_type: Mapped[str] = mapped_column(String(150))
    question_type: Mapped[str] = mapped_column(String(150), nullable=False)
    core_theme: Mapped[bool] = mapped_column(
        Boolean
    )  # Assuming TINYINT(1) is used as Boolean
    extends: Mapped[str] = mapped_column(String(150))
    group: Mapped[str] = mapped_column(String(150))
    settings: Mapped[str] = mapped_column(Text)


class Question(Base):
    __tablename__ = f"{PREFIX}_questions"

    qid: Mapped[int] = mapped_column(Integer, primary_key=True)
    parent_qid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    sid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    gid: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    type: Mapped[str] = mapped_column(
        String(30), nullable=False, index=True, server_default=text("'T'")
    )
    title: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, server_default=text("''")
    )
    preg: Mapped[str] = mapped_column(Text)
    other: Mapped[str] = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    mandatory: Mapped[str] = mapped_column(String(1))
    encrypted: Mapped[str] = mapped_column(
        String(1), server_default=text("'N'")
    )
    question_order: Mapped[int] = mapped_column(Integer, nullable=False)
    scale_id: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    same_default: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    relevance: Mapped[str] = mapped_column(Text)
    question_theme_name: Mapped[str] = mapped_column(String(150))
    modulename: Mapped[str] = mapped_column(String(255))
    same_script: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )

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

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sid: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String(255))
    qlimit: Mapped[int] = mapped_column(Integer)
    action: Mapped[int] = mapped_column(Integer)
    active: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'1'")
    )
    autoload_url: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


# TODO: Add typing from here
class QuotaLanguagesetting(Base):
    __tablename__ = f"{PREFIX}_quota_languagesettings"

    quotals_id = mapped_column(Integer, primary_key=True)
    quotals_quota_id = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    quotals_language = mapped_column(
        String(45), nullable=False, server_default=text("'en'")
    )
    quotals_name = mapped_column(String(255))
    quotals_message = mapped_column(Text, nullable=False)
    quotals_url = mapped_column(String(255))
    quotals_urldescrip = mapped_column(String(255))


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

    id = mapped_column(Integer, primary_key=True)
    sid = mapped_column(Integer)
    qid = mapped_column(Integer)
    quota_id = mapped_column(Integer)
    code = mapped_column(String(11))


class SavedControl(Base):
    __tablename__ = f"{PREFIX}_saved_control"

    scid = mapped_column(Integer, primary_key=True)
    sid = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    srid = mapped_column(
        Integer, nullable=False, index=True, server_default=text("'0'")
    )
    identifier = mapped_column(Text, nullable=False)
    access_code = mapped_column(Text, nullable=False)
    email = mapped_column(String(192))
    ip = mapped_column(Text, nullable=False)
    saved_thisstep = mapped_column(Text, nullable=False)
    status = mapped_column(
        String(1), nullable=False, server_default=text("''")
    )
    saved_date = mapped_column(DateTime, nullable=False)
    refurl = mapped_column(Text)


class LSSession(Base):
    __tablename__ = f"{PREFIX}_sessions"

    id = mapped_column(String(32), primary_key=True)
    expire = mapped_column(Integer, index=True)
    data = mapped_column(LargeBinary)


class SettingsGlobal(Base):
    __tablename__ = f"{PREFIX}_settings_global"

    stg_name = mapped_column(
        String(50), primary_key=True, server_default=text("''")
    )
    stg_value = mapped_column(Text, nullable=False)


class SettingsUser(Base):
    __tablename__ = f"{PREFIX}_settings_user"

    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(Integer, nullable=False, index=True)
    entity = mapped_column(String(15), index=True)
    entity_id = mapped_column(String(31), index=True)
    stg_name = mapped_column(String(63), nullable=False, index=True)
    stg_value = mapped_column(Text)


class SourceMessage(Base):
    __tablename__ = f"{PREFIX}_source_message"

    id = mapped_column(Integer, primary_key=True)
    category = mapped_column(String(35))
    message = mapped_column(Text)


class SurveyLink(Base):
    __tablename__ = f"{PREFIX}_survey_links"

    participant_id = mapped_column(
        String(50), primary_key=True, nullable=False
    )
    token_id = mapped_column(Integer, primary_key=True, nullable=False)
    survey_id = mapped_column(Integer, primary_key=True, nullable=False)
    date_created = mapped_column(DateTime)
    date_invited = mapped_column(DateTime)
    date_completed = mapped_column(DateTime)


class SurveyUrlParameter(Base):
    __tablename__ = f"{PREFIX}_survey_url_parameters"

    id = mapped_column(Integer, primary_key=True)
    sid = mapped_column(Integer, nullable=False)
    parameter = mapped_column(String(50), nullable=False)
    targetqid = mapped_column(Integer)
    targetsqid = mapped_column(Integer)


class Surveymenu(Base):
    __tablename__ = f"{PREFIX}_surveymenu"

    id = mapped_column(Integer, primary_key=True)
    parent_id = mapped_column(Integer)
    survey_id = mapped_column(Integer)
    user_id = mapped_column(Integer)
    name = mapped_column(String(128), unique=True)
    ordering = mapped_column(Integer, server_default=text("'0'"))
    level = mapped_column(Integer, server_default=text("'0'"))
    title = mapped_column(
        String(168), nullable=False, index=True, server_default=text("''")
    )
    position = mapped_column(
        String(192), nullable=False, server_default=text("'side'")
    )
    description = mapped_column(Text)
    showincollapse = mapped_column(Integer, server_default=text("'0'"))
    active = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    changed_at = mapped_column(DateTime)
    changed_by = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    created_at = mapped_column(DateTime)
    created_by = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


class SurveymenuEntry(Base):
    __tablename__ = f"{PREFIX}_surveymenu_entries"

    id = mapped_column(Integer, primary_key=True)
    menu_id = mapped_column(Integer, index=True)
    user_id = mapped_column(Integer)
    ordering = mapped_column(Integer, server_default=text("'0'"))
    name = mapped_column(String(168), unique=True, server_default=text("''"))
    title = mapped_column(
        String(168), nullable=False, server_default=text("''")
    )
    menu_title = mapped_column(
        String(168), nullable=False, index=True, server_default=text("''")
    )
    menu_description = mapped_column(Text)
    menu_icon = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    menu_icon_type = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    menu_class = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    menu_link = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    action = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    template = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    partial = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    classes = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    permission = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    permission_grade = mapped_column(String(192))
    data = mapped_column(Text)
    getdatamethod = mapped_column(
        String(192), nullable=False, server_default=text("''")
    )
    language = mapped_column(
        String(32), nullable=False, server_default=text("'en-GB'")
    )
    showincollapse = mapped_column(Integer, server_default=text("'0'"))
    active = mapped_column(Integer, nullable=False, server_default=text("'0'"))
    changed_at = mapped_column(DateTime)
    changed_by = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    created_at = mapped_column(DateTime)
    created_by = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )


class Survey(Base):
    __tablename__ = f"{PREFIX}_surveys"

    sid = mapped_column(Integer, primary_key=True)
    owner_id = mapped_column(Integer, nullable=False, index=True)
    gsid = mapped_column(Integer, index=True, server_default=text("'1'"))
    admin = mapped_column(String(50))
    active = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    expires = mapped_column(DateTime)
    startdate = mapped_column(DateTime)
    adminemail = mapped_column(String(254))
    anonymized = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    format = mapped_column(String(1))
    savetimings = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    template = mapped_column(String(100), server_default=text("'default'"))
    language = mapped_column(String(50))
    additional_languages = mapped_column(Text)
    datestamp = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    usecookie = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowregister = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowsave = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    autonumber_start = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    autoredirect = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowprev = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    printanswers = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    ipaddr = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    ipanonymize = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    refurl = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    datecreated = mapped_column(DateTime)
    showsurveypolicynotice = mapped_column(Integer, server_default=text("'0'"))
    publicstatistics = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    publicgraphs = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    listpublic = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    htmlemail = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    sendconfirmation = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    tokenanswerspersistence = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    assessments = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    usecaptcha = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    usetokens = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    bounce_email = mapped_column(String(254))
    attributedescriptions = mapped_column(Text)
    emailresponseto = mapped_column(Text)
    emailnotificationto = mapped_column(Text)
    tokenlength = mapped_column(
        Integer, nullable=False, server_default=text("'15'")
    )
    showxquestions = mapped_column(String(1), server_default=text("'Y'"))
    showgroupinfo = mapped_column(String(1), server_default=text("'B'"))
    shownoanswer = mapped_column(String(1), server_default=text("'Y'"))
    showqnumcode = mapped_column(String(1), server_default=text("'X'"))
    bouncetime = mapped_column(Integer)
    bounceprocessing = mapped_column(String(1), server_default=text("'N'"))
    bounceaccounttype = mapped_column(String(4))
    bounceaccounthost = mapped_column(String(200))
    bounceaccountpass = mapped_column(Text)
    bounceaccountencryption = mapped_column(String(3))
    bounceaccountuser = mapped_column(String(200))
    showwelcome = mapped_column(String(1), server_default=text("'Y'"))
    showprogress = mapped_column(String(1), server_default=text("'Y'"))
    questionindex = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    navigationdelay = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    nokeyboard = mapped_column(String(1), server_default=text("'N'"))
    alloweditaftercompletion = mapped_column(
        String(1), server_default=text("'N'")
    )
    googleanalyticsstyle = mapped_column(String(1))
    googleanalyticsapikey = mapped_column(String(25))
    tokenencryptionoptions = mapped_column(Text)


class SurveysGroup(Base):
    __tablename__ = f"{PREFIX}_surveys_groups"

    gsid = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(45), nullable=False, index=True)
    title = mapped_column(String(100), index=True)
    template = mapped_column(String(128), server_default=text("'default'"))
    description = mapped_column(Text)
    sortorder = mapped_column(Integer, nullable=False)
    owner_id = mapped_column(Integer)
    parent_id = mapped_column(Integer)
    alwaysavailable = mapped_column(Boolean)
    created = mapped_column(DateTime)
    modified = mapped_column(DateTime)
    created_by = mapped_column(Integer, nullable=False)


class SurveysGroupsetting(Base):
    __tablename__ = f"{PREFIX}_surveys_groupsettings"

    gsid = mapped_column(Integer, primary_key=True)
    owner_id = mapped_column(Integer)
    admin = mapped_column(String(50))
    adminemail = mapped_column(String(254))
    anonymized = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    format = mapped_column(String(1))
    savetimings = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    template = mapped_column(String(100), server_default=text("'default'"))
    datestamp = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    usecookie = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowregister = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowsave = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    autonumber_start = mapped_column(Integer, server_default=text("'0'"))
    autoredirect = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    allowprev = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    printanswers = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    ipaddr = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    ipanonymize = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    refurl = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    showsurveypolicynotice = mapped_column(Integer, server_default=text("'0'"))
    publicstatistics = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    publicgraphs = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    listpublic = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    htmlemail = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    sendconfirmation = mapped_column(
        String(1), nullable=False, server_default=text("'Y'")
    )
    tokenanswerspersistence = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    assessments = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    usecaptcha = mapped_column(
        String(1), nullable=False, server_default=text("'N'")
    )
    bounce_email = mapped_column(String(254))
    attributedescriptions = mapped_column(Text)
    emailresponseto = mapped_column(Text)
    emailnotificationto = mapped_column(Text)
    tokenlength = mapped_column(Integer, server_default=text("'15'"))
    showxquestions = mapped_column(String(1), server_default=text("'Y'"))
    showgroupinfo = mapped_column(String(1), server_default=text("'B'"))
    shownoanswer = mapped_column(String(1), server_default=text("'Y'"))
    showqnumcode = mapped_column(String(1), server_default=text("'X'"))
    showwelcome = mapped_column(String(1), server_default=text("'Y'"))
    showprogress = mapped_column(String(1), server_default=text("'Y'"))
    questionindex = mapped_column(Integer, server_default=text("'0'"))
    navigationdelay = mapped_column(Integer, server_default=text("'0'"))
    nokeyboard = mapped_column(String(1), server_default=text("'N'"))
    alloweditaftercompletion = mapped_column(
        String(1), server_default=text("'N'")
    )


class SurveysLanguagesetting(Base):
    __tablename__ = f"{PREFIX}_surveys_languagesettings"

    surveyls_survey_id = mapped_column(
        Integer, primary_key=True, nullable=False
    )
    surveyls_language = mapped_column(
        String(45),
        primary_key=True,
        nullable=False,
        server_default=text("'en'"),
    )
    surveyls_title = mapped_column(String(200), nullable=False, index=True)
    surveyls_description = mapped_column(Text)
    surveyls_welcometext = mapped_column(Text)
    surveyls_endtext = mapped_column(Text)
    surveyls_policy_notice = mapped_column(Text)
    surveyls_policy_error = mapped_column(Text)
    surveyls_policy_notice_label = mapped_column(String(192))
    surveyls_url = mapped_column(Text)
    surveyls_urldescription = mapped_column(String(255))
    surveyls_email_invite_subj = mapped_column(String(255))
    surveyls_email_invite = mapped_column(Text)
    surveyls_email_remind_subj = mapped_column(String(255))
    surveyls_email_remind = mapped_column(Text)
    surveyls_email_register_subj = mapped_column(String(255))
    surveyls_email_register = mapped_column(Text)
    surveyls_email_confirm_subj = mapped_column(String(255))
    surveyls_email_confirm = mapped_column(Text)
    surveyls_dateformat = mapped_column(
        Integer, nullable=False, server_default=text("'1'")
    )
    surveyls_attributecaptions = mapped_column(Text)
    surveyls_alias = mapped_column(String(100))
    email_admin_notification_subj = mapped_column(String(255))
    email_admin_notification = mapped_column(Text)
    email_admin_responses_subj = mapped_column(String(255))
    email_admin_responses = mapped_column(Text)
    surveyls_numberformat = mapped_column(
        Integer, nullable=False, server_default=text("'0'")
    )
    attachments = mapped_column(Text)


class TemplateConfiguration(Base):
    __tablename__ = f"{PREFIX}_template_configuration"

    id = mapped_column(Integer, primary_key=True)
    template_name = mapped_column(String(150), nullable=False, index=True)
    sid = mapped_column(Integer, index=True)
    gsid = mapped_column(Integer, index=True)
    uid = mapped_column(Integer, index=True)
    files_css = mapped_column(Text)
    files_js = mapped_column(Text)
    files_print_css = mapped_column(Text)
    options = mapped_column(Text)
    cssframework_name = mapped_column(String(45))
    cssframework_css = mapped_column(Text)
    cssframework_js = mapped_column(Text)
    packages_to_load = mapped_column(Text)
    packages_ltr = mapped_column(Text)
    packages_rtl = mapped_column(Text)


class Template(Base):
    __tablename__ = f"{PREFIX}_templates"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(150), nullable=False, index=True)
    folder = mapped_column(String(45))
    title = mapped_column(String(100), nullable=False, index=True)
    creation_date = mapped_column(DateTime)
    author = mapped_column(String(150))
    author_email = mapped_column(String(255))
    author_url = mapped_column(String(255))
    copyright = mapped_column(Text)
    license = mapped_column(Text)
    version = mapped_column(String(45))
    api_version = mapped_column(String(45), nullable=False)
    view_folder = mapped_column(String(45), nullable=False)
    files_folder = mapped_column(String(45), nullable=False)
    description = mapped_column(Text)
    last_update = mapped_column(DateTime)
    owner_id = mapped_column(Integer, index=True)
    extends = mapped_column(String(150), index=True)


class Tokens239779(Base):
    __tablename__ = f"{PREFIX}_tokens_239779"

    tid = mapped_column(Integer, primary_key=True)
    participant_id = mapped_column(String(50))
    firstname = mapped_column(Text)
    lastname = mapped_column(Text)
    email = mapped_column(Text, index=True)
    emailstatus = mapped_column(Text)
    token = mapped_column(String(36), index=True)
    language = mapped_column(String(25))
    blacklisted = mapped_column(String(17))
    sent = mapped_column(String(17), server_default=text("'N'"))
    remindersent = mapped_column(String(17), server_default=text("'N'"))
    remindercount = mapped_column(Integer, server_default=text("'0'"))
    completed = mapped_column(String(17), server_default=text("'N'"))
    usesleft = mapped_column(Integer, server_default=text("'1'"))
    validfrom = mapped_column(DateTime)
    validuntil = mapped_column(DateTime)
    mpid = mapped_column(Integer)


class TutorialEntry(Base):
    __tablename__ = f"{PREFIX}_tutorial_entries"

    teid = mapped_column(Integer, primary_key=True)
    ordering = mapped_column(Integer)
    title = mapped_column(Text)
    content = mapped_column(Text)
    settings = mapped_column(Text)


class TutorialEntryRelation(Base):
    __tablename__ = f"{PREFIX}_tutorial_entry_relation"

    teid = mapped_column(Integer, primary_key=True, nullable=False)
    tid = mapped_column(Integer, primary_key=True, nullable=False)
    uid = mapped_column(Integer, index=True)
    sid = mapped_column(Integer, index=True)


class Tutorial(Base):
    __tablename__ = f"{PREFIX}_tutorials"

    tid = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(128), unique=True)
    title = mapped_column(String(192))
    icon = mapped_column(String(64))
    description = mapped_column(Text)
    active = mapped_column(Integer, server_default=text("'0'"))
    settings = mapped_column(Text)
    permission = mapped_column(String(128), nullable=False)
    permission_grade = mapped_column(String(128), nullable=False)


class UserGroup(Base):
    __tablename__ = f"{PREFIX}_user_groups"

    ugid = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False, unique=True)
    description = mapped_column(Text, nullable=False)
    owner_id = mapped_column(Integer, nullable=False)


class UserInGroup(Base):
    __tablename__ = f"{PREFIX}_user_in_groups"

    ugid = mapped_column(Integer, primary_key=True, nullable=False)
    uid = mapped_column(Integer, primary_key=True, nullable=False)


class UserInPermissionrole(Base):
    __tablename__ = f"{PREFIX}_user_in_permissionrole"

    ptid = mapped_column(Integer, primary_key=True, nullable=False)
    uid = mapped_column(Integer, primary_key=True, nullable=False)


class User(Base):
    __tablename__ = f"{PREFIX}_users"

    uid = mapped_column(Integer, primary_key=True)
    users_name = mapped_column(
        String(64), nullable=False, unique=True, server_default=text("''")
    )
    password = mapped_column(Text, nullable=False)
    full_name = mapped_column(String(50), nullable=False)
    parent_id = mapped_column(Integer, nullable=False)
    lang = mapped_column(String(20))
    email = mapped_column(String(192), index=True)
    htmleditormode = mapped_column(String(7), server_default=text("'default'"))
    templateeditormode = mapped_column(
        String(7), nullable=False, server_default=text("'default'")
    )
    questionselectormode = mapped_column(
        String(7), nullable=False, server_default=text("'default'")
    )
    one_time_pw = mapped_column(Text)
    dateformat = mapped_column(
        Integer, nullable=False, server_default=text("'1'")
    )
    last_login = mapped_column(DateTime)
    created = mapped_column(DateTime)
    modified = mapped_column(DateTime)
    validation_key = mapped_column(String(38))
    validation_key_expiration = mapped_column(DateTime)
    last_forgot_email_password = mapped_column(DateTime)
    expires = mapped_column(DateTime)
