import React from 'react'
import {Link} from 'react-router-dom'


const ProjectItem = ({project, users}) => {
    return (
        <tr>
            <td>><Link to={`/project/${project.id}`}>{project.name}</Link></td>
            <td>{project.repositoryUrl}</td>
            <td>{project.users.map((userId) => {return users.find((user) => user.id == userId).firstName+' '})}</td>
        </tr>
    )
}


export default ProjectItem;