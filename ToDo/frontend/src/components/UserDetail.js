import React from 'react';
import { useParams } from 'react-router-dom'

import UserItem from './UserItem.js'
import ProjectItem from './ProjectItem.js'
import TodoItem from './TodoItem.js'


const UserDetail = ({all_obj}) => {
    let { id } = useParams();
    console.log('user_id = ',{id})

    let filtered_users = all_obj.users.filter((item) => item.id == id)
    let filtered_projects = all_obj.projects.filter((project) => project.users.includes(parseInt(id)))
    let filtered_todo = all_obj.todo.filter((todo) => todo.user == id)

    return (
        <div>
            <h1>Пользователь:</h1>
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

            <h1>Проекты:</h1>
            <table>
                <thead>
                    <tr>
                        <th>Наименование</th>
                        <th>Репозиторий</th>
                        <th>Участники</th>
                    </tr>
                </thead>
                <tbody>
                    {filtered_projects.map((project)=> <ProjectItem project={project} users={all_obj.users}/>)}
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
                    </tr>
                </thead>
                <tbody>
                    {filtered_todo.map((todo)=> <TodoItem todo={todo}/>)}
                </tbody>
            </table>
        </div>
    )
}

export default UserDetail;