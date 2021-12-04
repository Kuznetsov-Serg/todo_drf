import TodoItem from './TodoItem.js'
import {HashRouter, BrowseRouter, Route, Link, Switch, Redirect} from "react-router-dom"


const TodoList = ({todo, users, deleteTodo}) => {
    return (
        <div>
            <table>
                <thead>
                    <tr>
                        <th>Проект</th>
                        <th>пользователь-создатель</th>
                        <th>заголовок</th>
                        <th>заметка</th>
                        <th>Активность</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {todo.map((todo)=> <TodoItem todo={todo} users={users} deleteTodo={deleteTodo} />)}
                </tbody>
            </table>
           <button type="button" class="btn btn-info"><Link to='/todo/create'>Создать заметку</Link></button>
       </div>
    )
}

export default TodoList;