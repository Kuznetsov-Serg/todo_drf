import React from 'react';
import ProjectItem from './ProjectItem.js'
import {HashRouter, BrowseRouter, Route, Link, Switch, Redirect} from "react-router-dom"


class ProjectList extends React.Component {
    constructor(props) {
        super(props)
        this.state = {'filter': '', 'filtered_projects': props.projects}
    }

    handleChange(event)
    {
        this.setState(
                {
                    [event.target.name]: event.target.value
                }
            );
        console.log(event.target.name, '=', event.target.value)
    }

    handleFilterChange(event) {
        this.setState(
                        {
                            filter: event.target.value,
                            filtered_projects: this.props.projects.filter((item) => item.name.toUpperCase().indexOf(event.target.value.toUpperCase()) != -1)
                        }
                    );
        console.log(event.target.name, '=', event.target.value)
    }

    render() {
        return (
        <div>
            <label>Фильтр</label>
            <input type="text"  name="filter" value={this.state.filter} onChange={(event)=>this.handleFilterChange(event)} />
            <table>
                <thead>
                    <tr>
                        <th>Наименование</th>
                        <th>Репозиторий</th>
                        <th>Участники</th>
                        <th></th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    {this.state.filtered_projects.map((project)=> <ProjectItem project={project} users={this.props.users} deleteProject={this.props.deleteProject} updateProject={this.props.updateProject}/>)}
                </tbody>
            </table>
            <button type="button" class="btn btn-info"><Link to='/projects/create'>Создать проект</Link></button>
        </div>
        );
    }
}

export default ProjectList;