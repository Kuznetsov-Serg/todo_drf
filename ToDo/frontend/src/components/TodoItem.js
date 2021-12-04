import React from 'react'

const TodoItem = ({todo, users, deleteTodo}) => {
    let user = users.filter((item) => item.id == todo.user)[0]
    return (
        <tr>
            <td>{todo.project}</td>
            <td>{user.username}</td>
            <td>{todo.title}</td>
            <td>{todo.text}</td>
            <td>{todo.isActive ? '✅' : '❌'}</td>
            {deleteTodo && <td><button onClick={()=>deleteTodo(todo.id)} type='button'>{todo.isActive ? 'Delete ❌ ': 'Activate ✅ ' }</button></td>}
        </tr>
    )
}

export default TodoItem;