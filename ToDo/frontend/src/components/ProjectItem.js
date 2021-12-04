import React from 'react'
import {Link} from 'react-router-dom'


const ProjectItem = ({project, users, deleteProject, updateProject}) => {
    return (
        <tr>
            <td>><Link to={`/project/${project.id}`}>{project.name}</Link></td>
            <td>{project.repositoryUrl}</td>
            <td>{project.users.map((userId) => {return users.find((user) => user.id == userId).firstName+' '})}</td>
            {updateProject && <td><button type="button"><Link to={`/project/update/${project.id}`}>Change</Link></button></td>}
            {deleteProject && <td><button onClick={()=>deleteProject(project.id)} type='button'>Delete</button></td>}
        </tr>
    )
}


export default ProjectItem;