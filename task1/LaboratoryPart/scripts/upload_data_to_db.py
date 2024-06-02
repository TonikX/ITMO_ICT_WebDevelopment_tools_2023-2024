from models import *
from passlib.context import CryptContext
from datetime import datetime, timedelta
crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')





def refresh_instances(session, instances):
    for instance in instances:
        session.refresh(instance)

def main():
    with get_session_func() as session:
        # Create users
        hashed_password = crypto_context.hash('786811')
        users = [
            User(username=f"user{i}", email=f"user{i}@example.com", hashed_password=hashed_password) for i in range(1, 6)
        ]
        session.add_all(users)
        session.commit()
        refresh_instances(session, users)
        print('Created users')

        # Create projects
        project_university = Project(title="University", description="Project related to university tasks")
        project_soft_skills = Project(title="Soft skills", description="Project related to improving soft skills")

        projects = [project_university, project_soft_skills]
        session.add_all(projects)
        session.commit()
        refresh_instances(session, projects)

        print('Created projects')


        links = [
            ProjectUserLink(user_id=users[0].id, project_id=project_university.id, role=Role.admin),
            ProjectUserLink(user_id=users[1].id, project_id=project_university.id, role=Role.viewer),
            ProjectUserLink(user_id=users[2].id, project_id=project_university.id, role=Role.viewer),
            ProjectUserLink(user_id=users[3].id, project_id=project_soft_skills.id, role=Role.admin),
            ProjectUserLink(user_id=users[4].id, project_id=project_soft_skills.id, role=Role.viewer),
        ]
        session.add_all(links)
        session.commit()
        refresh_instances(session, links)
        print('Added users to projects')

        categories_university = [
            Category(title="Homework", project_id =project_university.id),
            Category(title="Events", project_id=project_university.id)
        ]
        categories_soft_skills = [
            Category(title="Pitch", project_id=project_soft_skills.id),
            Category(title="Team Building", project_id=project_soft_skills.id)
        ]
        categories = categories_university + categories_soft_skills
        session.add_all(categories)
        session.commit()
        refresh_instances(session, categories)


        tasks_university = [
            Task(title="Research Paper", description="Work on the research paper.", priority=Priority.high,
                 approximate_time=datetime.now().time(), category_id=categories_university[0].id),
            Task(title="Study Group", description="Organize a study group session.", priority=Priority.medium,
                 approximate_time=datetime.now().time(), category_id=categories_university[1].id),
        ]

        tasks_soft_skills = [
            Task(title="Presentation Skills", description="Improve presentation skills.", priority=Priority.medium,
                 approximate_time=datetime.now().time(), category_id=categories_soft_skills[0].id),
            Task(title="Team Collaboration", description="Work on team collaboration techniques.",
                 priority=Priority.high,
                 approximate_time=datetime.now().time(), category_id=categories_soft_skills[1].id)
        ]
        tasks = tasks_university + tasks_soft_skills
        session.add_all(tasks)
        session.commit()
        refresh_instances(session, tasks)
        print('Added tasks')

        # Add calendar entries for each task
        start_time = datetime.now()
        for task in tasks_university + tasks_soft_skills:
            entries = [
                CalendarEntry(start_time=start_time, end_time=start_time + timedelta(hours=1), task_id=task.id),
                CalendarEntry(start_time=start_time + timedelta(days=1),
                              end_time=start_time + timedelta(days=1, hours=2), task_id=task.id),
            ]
            session.add_all(entries)
            session.commit()
            refresh_instances(session, entries)
        print('Added calendar entries')
        session.commit()


if __name__ == '__main__':
    main()