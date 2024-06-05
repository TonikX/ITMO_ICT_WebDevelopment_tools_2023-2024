async def main():
    project_id = await create_project()
    category_none_id = await create_none_category(project_id)
    task_pages = [
        'c8e2b50cb4004158a32435f7ae588136',   # без таска       
        'a4e74092-e9ef-43ca-b1dc-e1e8ee48e4e9', #itmo
        '171dfc520da94253abd2f9ba9fb10958', # быт
        '171dfc520da94253abd2f9ba9fb10958', # быт
        '171dfc520da94253abd2f9ba9fb10958', # быт
        '171dfc520da94253abd2f9ba9fb10958', # быт
        '0961bbad0aea4b6086701b6aedee1745', # itmo
        'd332d38f8a364ab89c03394d8ded3cd4' # itmo
    ]
    task_pages = to_uuid(task_pages)
    
    task_writer = TaskWriter(project_id, category_none_id)
    for task_id in task_pages:
        await task_writer.write_task_to_db(task_id)
        print('Прошел')
        
def to_uuid(str_list):
    result = []
    for s in str_list:
        uuid = str(UUID(s))
        result.append(uuid)
    return result