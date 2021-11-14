
const TodoItem = ({todo}) => {
    return (
        <tr>
            <td>{todo.project}</td>
            <td>{todo.user}</td>
            <td>{todo.title}</td>
            <td>{todo.text}</td>
        </tr>
    )
}

export default TodoItem;