import React from 'react';
import ProjectItem from './ProjectItem.js'


const ProjectList = ({projects, users}) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Наименование</th>
                    <th>Репозиторий</th>
                    <th>Участники</th>
                </tr>
            </thead>
            <tbody>
                {projects.map((project)=> <ProjectItem project={project} users={users}/>)}
            </tbody>
        </table>
    )
}

export default ProjectList;