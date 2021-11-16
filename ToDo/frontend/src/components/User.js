import UserItem from './UserItem.js'


const UserList = ({users}) => {
    return (
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
                {users.map((user)=> <UserItem user={user}/>)}
            </tbody>
        </table>
    )
}

export default UserList;