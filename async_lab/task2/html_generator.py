def generate_projects_html(index):
    project_template = '''
        <li>
            <div>
                <p class="name">Project {index}</p>
                <p class="description">Description of project {index}</p>
                <p class="expected-result">Expected result</p>
                <p class="team-id">{team_id}</p>
            </div>
        </li>
'''

    projects_html = ''.join([project_template.format(index=i + 1, team_id=(i % 50) + 1) for i in range(100)])

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Projects</title>
        </head>
        <body>
            <h1>Projects</h1>
            <ul>
                {projects_html}
            </ul>
            <a href="index.html">Back to home</a>
        </body>
        </html>'''

    with open(f'./data/projects{index + 1}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content successfully saved to './data/projects{index + 1}.html'")


def generate_users_html(index):
    user_template = '''
                <li>
                    <div>
                        <p class="username">username{index}</p>
                        <p class="password">password{index}</p>
                        <p class="profile-id">{profile_id}</p>
                    </div>
                </li>
        '''

    users_html = ''.join([user_template.format(index=i + 1, profile_id=(i % 10) + 1) for i in range(100)])

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Users</title>
        </head>
        <body>
            <h1>Users</h1>
            <ul>
                {users_html}
            </ul>
            <a href="index.html">Back to home</a>
        </body>
        </html>'''

    with open(f'./data/users{index + 1}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content successfully saved to './data/users{index + 1}.html'")


def generate_tasks_html(index):
    task_template = '''
                <li>
                    <div>
                        <p class="name">Task{index}</p>
                        <p class="description">Description of task {index}</p>
                        <p class="deadline">2024-12-{day}T12:00:00</p>
                        <p class="project-id">{project_id}</p>
                    </div>
                </li>
        '''

    tasks_html = ''.join(
        [task_template.format(index=i + 1, day=(i % 30) + 1, project_id=(i % 10) + 1) for i in range(100)])

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Tasks</title>
        </head>
        <body>
            <h1>Tasks</h1>
            <ul>
                {tasks_html}
            </ul>
            <a href="index.html">Back to home</a>
        </body>
        </html>'''


    with open(f'./data/tasks{index + 1}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content successfully saved to './data/tasks{index + 1}.html'")


def generate_userprofiles_html(index):
    profile_template = '''
                <li>
                    <div>
                        <p class="id">User Profile ID: {index}</p>
                        <p class="avatar">avatar{index}.jpg</p>
                        <p class="birth_date">1990-01-{day}</p>
                        <ol class="skills">
                            {skills_html}
                        </ol>
                    </div>
                </li>
        '''

    skills_list = [["skill1", "skill2", "skill3"], ["skillA", "skillB"], ["skillX", "skillY", "skillZ"]]
    profiles_html = ''.join([profile_template.format(
        index=i + 1,
        day=(i % 30) + 1,
        skills_html=''.join(f'<li>{skill}</li>' for skill in skills_list[i % len(skills_list)])
    ) for i in range(100)])

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>User Profiles</title>
        </head>
        <body>
            <h1>User Profiles</h1>
            <ul>
                {profiles_html}
            </ul>
            <a href="index.html">Back to home</a>
        </body>
        </html>'''

    # Сохранение HTML в файл
    with open(f'./data/userprofiles{index + 1}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content successfully saved to './data/userprofiles{index + 1}.html'")

def generate_teams_html(index):
    team_template = '''
                <li>
                    <div>
                        <p class="id">Team ID: {index}</p>
                        <p class="name">Team Name {index}</p>
                    </div>
                </li>
        '''

    teams_html = ''.join([team_template.format(index=i + 1) for i in range(100)])

    html_content = f'''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Teams</title>
        </head>
        <body>
            <h1>Teams</h1>
            <ul>
                {teams_html}
            </ul>
            <a href="index.html">Back to home</a>
        </body>
        </html>'''

    # Сохранение HTML в файл
    with open(f'./data/teams{index + 1}.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML content successfully saved to './data/teams{index + 1}.html'")

for i in range(5):
    generate_projects_html(i)
    generate_users_html(i)
    generate_tasks_html(i)
    generate_userprofiles_html(i)
    generate_teams_html(i)

