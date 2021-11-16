import React from 'react'
import {Link} from 'react-router-dom'


const UserItem = ({user}) => {
    return (
        <tr>
            <td><Link to={`/user/${user.id}`}>{user.username}</Link></td>
            <td>{user.firstName}</td>
            <td>{user.lastName}</td>
            <td>{user.email}</td>
        </tr>
    )
}


export default UserItem;