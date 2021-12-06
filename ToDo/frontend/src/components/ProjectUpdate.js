import React from 'react';
import { useParams } from 'react-router-dom';

import ProjectForm from './ProjectForm.js';


const ProjectUpdate = ({projects, users, updateProject}) => {
    let { id } = useParams();               // не работает под class - пришлось выделить в отдельный модуль
    console.log('project_id = ',{id})
    console.log('projects = ',projects)
    console.log('users = ',users)
    let project = projects.filter((item) => item.id == id)[0]
    return (
            <div>
                <ProjectForm id={id} project={project} users={users} updateProject={updateProject}/>
            </div>
    )
}

export default ProjectUpdate;