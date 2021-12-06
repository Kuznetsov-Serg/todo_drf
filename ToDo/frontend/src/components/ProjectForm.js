import React from 'react'
import { useParams } from 'react-router-dom'
import { withRouter } from "react-router";



class ProjectForm extends React.Component {

    constructor(props) {
        super(props)
        if (props.project) {    // Update
            this.state = {
                            'id': props.project.id,
                            'name': props.project.name,
                            'repository_url': props.project.repositoryUrl,
                            'users': props.project.users,
                }
            }
        else {                  // Create
            this.state = {'name': '', 'repository_url': '', 'users': []}
        }
        console.log('props = ', props)
        console.log('props.id = ', props.id)
        console.log('this.state = ', this.state)
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

    handleUsersChange(event) {
        if (!event.target.selectedOptions) {
            this.setState({
                'users': []
            })
            return;
        }
        let users = []
        for(let i=0; i< event.target.selectedOptions.length; i++) {
            users.push(event.target.selectedOptions.item(i).value)
        }
        this.setState({
            'users': users
        })
    }

    handleSubmit(event) {
        if (this.props.project) {      // Update
            this.props.updateProject(this.state.id, this.state.name, this.state.repository_url, this.state.users)
            }
        else {                          // Create
            this.props.createProject(this.state.name, this.state.repository_url, this.state.users)
            }
        console.log(this.state.name, this.state.repository_url, this.state.users)
        event.preventDefault()
    }

    render() {
        return (
        <form onSubmit={(event)=> this.handleSubmit(event)}>
            <div className="form-group">
                <label>Наименование</label>
                <input type="text" className="form-control" name="name" value={this.state.name} onChange={(event)=>this.handleChange(event)} />
                <label>Ссылка на репозиторий</label>
                <input type="text" className="form-control" name="repository_url" value={this.state.repository_url} onChange={(event)=>this.handleChange(event)} />
            </div>
            <div className="form-group">
                <label for="users">Пользователи</label>
                <select name="users" multiple onChange={(event)=>this.handleUsersChange(event)}>
                                {this.props.users.map((item)=><option value={item.id}>{item.username}</option>)}
                </select>
            </div>
            <input type="submit" className="btn btn-primary" value="Save" />
        </form>
        );
    }
}

export default ProjectForm
