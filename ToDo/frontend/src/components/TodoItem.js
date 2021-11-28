
const TodoItem = ({todo, users}) => {
    let user = users.filter((item) => item.id == todo.user)[0]
    return (
        <tr>
            <td>{todo.project}</td>
            <td>{user.firstName}</td>
            <td>{todo.title}</td>
            <td>{todo.text}</td>
        </tr>
    )
}

export default TodoItem;