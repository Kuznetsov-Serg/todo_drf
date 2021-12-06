import React from 'react';
import { useParams } from 'react-router-dom'

import UserItem from './UserItem.js'
import ProjectItem from './ProjectItem.js'
import TodoItem from './TodoItem.js'


const ProjectDetail = ({projects, users, todo}) => {
    let { id } = useParams();
    console.log('project_id = ',{id})

    let filtered_projects = projects.filter((item) => item.id == id)
    let filtered_todo = todo.filter((item) => item.project == id)
//    let filtered_users = users.filter((item) => filtered_projects[0].users.indexOf(item.id) > -1)
    let filtered_users = users.filter(user => filtered_projects[0].users.includes(parseInt(user.id)))

    return (
        <div>
            <h1>Проект:</h1>
            <table>
                <thead>
                    <tr>
                        <th>Наименование</th>
                        <th>Репозиторий</th>
                        <th>Участники</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered_projects.map((project)=> <ProjectItem project={project} users={users} />)}
                </tbody>
            </table>

            <h1>Заметки:</h1>
            <table>
                <thead>
                    <tr>
                        <th>Проект</th>
                        <th>пользователь-создатель</th>
                        <th>заголовок</th>
                        <th>заметка</th>
                        <th>Активность</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered_todo.map((todo)=> <TodoItem todo={todo} users={users}/>)}
                </tbody>
            </table>
            <h1>Пользователи:</h1>
            <table>
                <thead>
                    <tr>
                        <th>UserName</th>
                        <th>First Name</th>
                        <th>Last Name</th>
                        <th>Email</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered_users.map((user)=> <UserItem user={user}/>)}
                </tbody>
            </table>

        </div>
    )
}

export default ProjectDetail;