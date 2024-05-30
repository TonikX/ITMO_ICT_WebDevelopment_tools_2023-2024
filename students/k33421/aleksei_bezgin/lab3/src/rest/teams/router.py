from fastapi import APIRouter, HTTPException
from sqlalchemy import exc
from sqlmodel import select

from db.models import Team as TeamModel, MemberTeamLink as MemberTeamLinkModel
from rest.dependencies import DatabaseSession
from rest.teams.schemas import Team, Member, TeamCreateData, MemberBase, TeamUpdateData

router = APIRouter()


@router.get("/")
def get_teams(session: DatabaseSession) -> list[Team]:
    stmt = select(TeamModel)
    teams = session.scalars(stmt).all()
    return [
        Team.model_validate(
            team,
            update={
                "members": [
                    Member.model_validate(member_link.member, update={"role": member_link.role})
                    for member_link in team.member_links
                ]
            },
        )
        for team in teams
    ]


@router.get("/{team_id}")
def get_team(team_id: int, session: DatabaseSession) -> Team:
    stmt = select(TeamModel).where(TeamModel.id == team_id)
    team = session.scalars(stmt).first()
    return Team.model_validate(
        team,
        update={
            "members": [
                Member.model_validate(member_link.member, update={"role": member_link.role})
                for member_link in team.member_links
            ]
        },
    )


@router.post("/")
def create_team(team_data: TeamCreateData, session: DatabaseSession) -> Team:
    team_model = TeamModel.model_validate(team_data)
    session.add(team_model)
    session.commit()
    session.refresh(team_model)

    for member in team_data.members:
        member_team_link = MemberTeamLinkModel(team_id=team_model.id, member_id=member.id, role=member.role)
        session.add(member_team_link)

    session.commit()
    session.refresh(team_model)

    return Team.model_validate(
        team_model,
        update={
            "members": [
                Member.model_validate(member_link.member, update={"role": member_link.role})
                for member_link in team_model.member_links
            ]
        },
    )


@router.post("/{team_id}/add_member")
def add_member_to_team(team_id: int, member_data: MemberBase, session: DatabaseSession) -> Team:
    stmt = select(TeamModel).where(TeamModel.id == team_id)
    team_model = session.scalars(stmt).first()

    member_team_link = MemberTeamLinkModel(team_id=team_model.id, member_id=member_data.id, role=member_data.role)

    session.add(member_team_link)

    try:
        session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail="Member already exists in this team")

    session.refresh(team_model)

    return Team.model_validate(
        team_model,
        update={
            "members": [
                Member.model_validate(member_link.member, update={"role": member_link.role})
                for member_link in team_model.member_links
            ]
        },
    )


@router.patch("/{team_id}")
def update_team(team_id: int, team_data: TeamUpdateData, session: DatabaseSession) -> Team:
    stmt = select(TeamModel).where(TeamModel.id == team_id)
    team_model = session.scalars(stmt).first()

    for key, value in team_data.model_dump(exclude_unset=True).items():
        setattr(team_model, key, value)

    session.add(team_model)
    session.commit()
    session.refresh(team_model)

    return Team.model_validate(
        team_model,
        update={
            "members": [
                Member.model_validate(member_link.member, update={"role": member_link.role})
                for member_link in team_model.member_links
            ]
        },
    )


@router.delete("/{team_id}")
def delete_team(team_id: int, session: DatabaseSession) -> str:
    stmt = select(TeamModel).where(TeamModel.id == team_id)
    team_model = session.scalars(stmt).first()
    if not team_model:
        raise HTTPException(status_code=404, detail="Team not found")

    session.delete(team_model)
    session.commit()

    return f"Team {team_model.name} deleted"


@router.delete("/{team_id}/kick_member/{member_id}")
def kick_member_from_team(team_id: int, member_id: int, session: DatabaseSession) -> str:
    stmt = select(MemberTeamLinkModel).where(
        MemberTeamLinkModel.member_id == member_id, MemberTeamLinkModel.team_id == team_id
    )
    member_team_link = session.scalars(stmt).first()
    if not member_team_link:
        raise HTTPException(status_code=404, detail="Team or member not found")

    member = member_team_link.member
    team = member_team_link.team

    session.delete(member_team_link)
    session.commit()

    return f"{member.full_name} was deleted from team {team.name}"