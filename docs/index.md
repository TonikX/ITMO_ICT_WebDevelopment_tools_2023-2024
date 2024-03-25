# Лабораторная работа 1
## Цель лабораторной работы
Научится реализовывать полноценное серверное приложение с помощью фреймворка FastAPI с применением дополнительных средств и библиотек.
##Описание работы (разработка платформы для поиска людей в команду)
Задача - создать веб-платформу, которая поможет людям находить партнеров для совместной работы над проектами. Платформа должна предоставлять возможность пользователям создавать профили, описывать свои навыки, опыт и интересы, а также искать других участников и команды для участия в проектах.

- Создание профилей: Возможность пользователям создавать профили, указывать информацию о себе, своих навыках, опыте работы и предпочтениях по проектам.

- Поиск и фильтрация профилей: Реализация функционала поиска пользователей и команд на основе заданных критериев, таких как навыки, опыт, интересы и т.д.

- Создание и просмотр проектов: Возможность пользователям создавать проекты и описывать их цели, требования и ожидаемые результаты. Возможность просмотра доступных проектов и их участников.

- Управление командами и проектами: Возможность участникам создавать команды для совместной работы над проектами и управления участниками. Функционал для управления проектами, включая установку сроков, назначение задач, отслеживание прогресса и т.д.

## Реализация функционала (практическое задание включает)
- Авторизацию и регистрацию 
- Генерацию JWT-токенов
- Аутентификацию по JWT-токену
- Хэширование паролей


### models.py
    from sqlmodel import SQLModel, Field, Relationship
    import typing
    
    
    class SkillsProfiles(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    profile_id: typing.Optional[int] = Field(default=None, foreign_key="profile.id")
    skill_id: typing.Optional[int] = Field(default=None, foreign_key="skill.id")
    
    
    class SkillsProjects(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: typing.Optional[int] = Field(default=None, foreign_key="project.id")
    skill_id: typing.Optional[int] = Field(default=None, foreign_key="skill.id")
    
    
    class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    skills_profiles: typing.Optional[typing.List["Profile"]] = Relationship(
        back_populates="own_skills", link_model=SkillsProfiles
    )
    skills_projects: typing.Optional[typing.List["Project"]] = Relationship(
        back_populates="requirements_skills", link_model=SkillsProjects
    )
    
    
    class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: str
    is_active: bool = Field(default=True)
    user_profile: typing.Optional["Profile"] = Relationship(
        back_populates="user", sa_relationship_kwargs={'uselist': False}
    )
    
    
    class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    creator_id: int
    is_active: bool = Field(default=True)
    projects_team: typing.Optional[typing.List["Project"]] = Relationship(back_populates="team_project")
    profiles_team: typing.Optional[typing.List["Profile"]] = Relationship(back_populates="team_profile")
    
    
    class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    team_id: int = Field(default=None, foreign_key="team.id")
    team_project: Team = Relationship(back_populates="projects_team")
    goal: str
    is_active: bool = Field(default=True)
    requirements_skills: typing.Optional[typing.List[Skill]] = Relationship(
        back_populates="skills_projects", link_model=SkillsProjects
    )
    results: str
    
    
    class Profile(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: typing.Optional[int] = Field(default=None, foreign_key="user.id")
    user: typing.Optional[User] = Relationship(back_populates="user_profile")
    is_active: bool = Field(default=True)
    description: typing.Optional[str]
    team_id: typing.Optional[int] = Field(default=None, foreign_key="team.id")
    team_profile: typing.Optional[Team] = Relationship(back_populates="profiles_team")
    own_skills: typing.Optional[typing.List[Skill]] = Relationship(
        back_populates="skills_profiles", link_model=SkillsProfiles,
        sa_relationship_kwargs={'uselist': True}
    )
    projects_interests: typing.Optional[str]
    experience: typing.Optional[str]

### profile.py

    import typing
    
    from fastapi import APIRouter, Depends
    
    from src.dependencies import get_current_user
    from src.settings.connection import get_session
    from src import models
    from src.schemas.profile import ProfileUpdate
    from src.adapters.db import SqlalchemyWorker
    from sqlmodel import select
    
    profile_route = APIRouter(prefix="/profile", tags=["profile"])
    
    
    @profile_route.patch("/{id}", response_model=models.Profile, status_code=200)
    def update_profile(
            profile_id: int, profile_update: ProfileUpdate, session=Depends(get_session),
            user=Depends(get_current_user)
    ) -> models.Profile:
        sqlalchemy_worker = SqlalchemyWorker(session)
        profile_query = select(models.Profile).where(models.Profile.id == profile_id, models.Profile.is_active == True)
        skills = profile_update.skills
        delattr(profile_update, "skills")
        updated_profile = sqlalchemy_worker.patch_object(profile_query, profile_update)
        skills_query = select(models.Skill).where(models.Skill.id.in_(skills))
        skills_profile = sqlalchemy_worker.get_objects(skills_query)
        for skill_profile in skills_profile:
            if skill_profile not in updated_profile.own_skills:
                updated_profile.own_skills.append(skill_profile)
        session.commit()
        profile = session.refresh(updated_profile)
        return profile
    
    
    @profile_route.delete("/{id}", status_code=204)
    def deactivate_profile(profile_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> None:
        query = select(models.Profile).where(models.Profile.id == profile_id, models.Profile.is_active == True)
        SqlalchemyWorker(session).delete_object(query)
    
    
    @profile_route.get("/{id}", response_model=models.Profile)
    def get_profile(profile_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> models.Profile:
        query = (select(models.Profile)
                 .where(models.Profile.id == profile_id, models.Profile.is_active == True))
    
        return SqlalchemyWorker(session).get_object(query)
    
    
    @profile_route.get("/", response_model=typing.List[models.Profile])
    def get_profiles(session=Depends(get_session), search: typing.Optional[str] = None,
                     user=Depends(get_current_user)) -> typing.List[models.Profile]:
        query = (select(models.Profile)
                 .where(models.Profile.own_skills.any(models.Skill.name == search))) if search else select(models.Profile)
        return SqlalchemyWorker(session).get_objects(query)

### project.py
    import typing
    
    from fastapi import APIRouter, Depends
    from sqlmodel import select
    
    from src.adapters.db import SqlalchemyWorker
    from src.dependencies import get_current_user
    from src.models import Project, Team, Skill, Profile
    from src.schemas.project import ProjectCreate
    from src.settings.connection import get_session
    
    project_route = APIRouter(prefix="/project", tags=["project"])
    
    
    @project_route.post("/", response_model=Project, status_code=201)
    async def create_project(
            created_project: ProjectCreate, session=Depends(get_session), user=Depends(get_current_user)
    ) -> Project:
        sqlalchemy_worker = SqlalchemyWorker(session)
        team_query = select(Team).where(Team.id == created_project.team_id, Team.is_active == True)
        sqlalchemy_worker.get_object(team_query)
        project = Project.model_validate(created_project)
    
        return sqlalchemy_worker.create_object(project)
    
    
    @project_route.patch("/{id}", response_model=Project)
    async def update_project(
            project_id: int,
            created_project: ProjectCreate,
            session=Depends(get_session),
            user=Depends(get_current_user)
    ) -> Project:
        sqlalchemy_worker = SqlalchemyWorker(session)
        query = select(Project).where(Project.id == project_id, Project.is_active == True)
        team_query = select(Team).where(Team.id == created_project.team_id, Team.is_active == True)
        sqlalchemy_worker.get_object(team_query)
    
        return SqlalchemyWorker(session).patch_object(query, created_project)
    
    
    @project_route.delete("/{id}", status_code=204)
    async def delete_project(project_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> None:
        query = select(Project).where(Project.id == project_id, Project.is_active == True)
    
        SqlalchemyWorker(session).delete_object(query)
    
    
    @project_route.get("/{id}")
    async def get_project(project_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> dict:
        sqlalchemy_worker = SqlalchemyWorker(session)
        query = select(Project).where(Project.id == project_id, Project.is_active == True)
    
        project = sqlalchemy_worker.get_object(query)
        project_members_query = select(Profile).where(project.team_id == Profile.team_id)
        project_members = sqlalchemy_worker.get_objects(project_members_query)
        project = project.model_dump()
        project["members"] = project_members
    
        return project
    
    
    @project_route.get("/", response_model=typing.List[Project])
    async def get_projects(
            session=Depends(get_session),
            search: typing.Optional[str] = None,
            user=Depends(get_current_user)
    ) -> typing.List[Project]:
        query = select(Project).where(Project.requirements_skills.any(Skill.name == search)) if search else select(Project)
    
        return SqlalchemyWorker(session).get_objects(query)

### team.py
    import typing
    
    from fastapi import APIRouter, Depends
    from starlette.responses import JSONResponse
    
    from src.dependencies import get_current_user
    from src.models import Team
    from src.settings.connection import get_session
    from src.adapters.db import SqlalchemyWorker
    from src.schemas.team import TeamUpdate, TeamCreate, TeamParticipantUpdate
    from sqlmodel import select
    from src import models
    
    team_route = APIRouter(prefix="/team", tags=["team"])
    
    
    @team_route.post("/", response_model=Team)
    async def create_team(created_team: TeamCreate, session=Depends(get_session), user=Depends(get_current_user)) -> Team:
        created_team.creator_id = user.id
        team = Team.model_validate(created_team)
        return SqlalchemyWorker(session).create_object(team)
    
    
    @team_route.get("/", response_model=typing.List[Team])
    async def get_teams(session=Depends(get_session), user=Depends(get_current_user)) -> typing.List[Team]:
        query = select(models.Team)
        return SqlalchemyWorker(session).get_objects(query)
    
    
    @team_route.get("/{id}", response_model=Team)
    async def get_team(team_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> Team:
        query = select(models.Team).where(models.Team.id == team_id)
        return SqlalchemyWorker(session).get_object(query)
    
    
    @team_route.patch("/{id}", response_model=Team)
    async def update_team(
            team_id: int, updated_team: TeamUpdate,
            session=Depends(get_session), user=Depends(get_current_user)
    ) -> Team:
        query = select(models.Team).where(models.Team.id == team_id)
        return SqlalchemyWorker(session).patch_object(query, updated_team)
    
    
    @team_route.delete("/{id}")
    async def delete_team(team_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> None:
        query = select(models.Team).where(models.Team.id == team_id)
        SqlalchemyWorker(session).delete_object(query)
    
    
    @team_route.post("/participant/add")
    async def add_participant(
            updated_participant: TeamParticipantUpdate, session=Depends(get_session)
    ):
        sqlalchemy_worker = SqlalchemyWorker(session)
        profile_query = (
            select(models.Profile)
            .where(models.Profile.id == updated_participant.profile_id, models.Profile.is_active == True))
        team_query = select(models.Team).where(models.Team.id == updated_participant.team_id)
        team = sqlalchemy_worker.get_object(team_query)
        profile = sqlalchemy_worker.get_object(profile_query)
        profile.team_id = team.id
        session.commit()
        return JSONResponse(status_code=200, content={"message": f"Participant {profile.user.username} add"})
    
    
    @team_route.post("/participant/delete", status_code=200)
    async def delete_participant(
            updated_participant: TeamParticipantUpdate, session=Depends(get_session)
    ):
        sqlalchemy_worker = SqlalchemyWorker(session)
        profile_query = (
            select(models.Profile)
            .where(models.Profile.id == updated_participant.profile_id, models.Profile.is_active == True))
        team_query = select(models.Team).where(models.Team.id == updated_participant.team_id)
        team = sqlalchemy_worker.get_object(team_query)
        profile = sqlalchemy_worker.get_object(profile_query)
        profile.team_id = None
        session.commit()
        return JSONResponse(status_code=200, content={"message": f"Participant {profile.user.username} deleted"})

### auth.py

    import datetime
    import os
    
    import fastapi
    from fastapi import HTTPException
    from fastapi.security import HTTPBearer
    from passlib.context import CryptContext
    import jwt
    
    from src.settings.config import config
    
    
    class AuthHandler:
        security = HTTPBearer()
        pwd_context = CryptContext(schemes=['bcrypt'])
        secret = config.hash_password_secret

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, token: str = fastapi.Header("token")):
        return self.decode_token(token)
### db.py
    import typing

    from fastapi import HTTPException
    
    
    class SqlalchemyWorker:

    def __init__(self, session):
        self.session = session

    def create_object(self, created_object: typing.Any):
        self.session.add(created_object)
        self.session.commit()
        self.session.refresh(created_object)
        return created_object

    def get_object(self, query):
        response = self.session.exec(query).first()
        if not response:
            raise HTTPException(status_code=404, detail="Object not found")
        return response

    def get_objects(self, query):
        return self.session.exec(query).all()

    def patch_object(self, query, updated_data):
        get_object = self.get_object(query)
        profile_data = updated_data.model_dump(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(get_object, key, value)
        self.session.add(get_object)
        self.session.commit()
        self.session.refresh(get_object)
        return get_object

    def delete_object(self, query):
        get_object = self.get_object(query)
        get_object.is_active = False
        self.session.commit()

## Ссылки на практические задания
- Задание 1 - https://github.com/mariaantonova334734/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/main/students/K33422/practical_works/pr%201.1
- Задание 2 - https://github.com/mariaantonova334734/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/main/students/K33422/practical_works/pr%201.2
- Задание 3 - https://github.com/mariaantonova334734/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/main/students/K33422/practical_works/pr%201.3

##Вывод
В рамках данной лабораторной работы были получены навыки по реализации полноценного серверного приложения с помощью фреймворка FastAPI. Был получен опыт по реализации платформы для поиска людей в команду.