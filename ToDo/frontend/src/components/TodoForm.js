import React from 'react'


class TodoForm extends React.Component {
    constructor(props) {
        super(props)
        console.log('Props = ', props)
        this.state = {'project': props.projects[0].id, 'user': props.users[0].id, 'title': '', 'text': ''}
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

    handleSubmit(event) {
        this.props.createTodo(this.state.project, this.state.user, this.state.title, this.state.text)
        event.preventDefault()
    }

    render() {
        return (
        <form onSubmit={(event)=> this.handleSubmit(event)}>
            <div className="form-group">
                <label>Проект</label>
                <select className="form-control" name="project" onChange={(event)=>this.handleChange(event)}>
                                {this.props.projects.map((item)=><option value={item.id}>{item.name}</option>)}
                </select>

                <label>Пользователь</label>
                <select className="form-control" name="users" onChange={(event)=>this.handleChange(event)}>
                                {this.props.users.map((item)=><option value={item.id}>{item.username}</option>)}
                </select>

                <label>Заголовок</label>
                <input type="text" className="form-control" name="title" value={this.state.title} onChange={(event)=>this.handleChange(event)} />

                <label>Заметка</label>
                <input type="text" className="form-control" name="text" value={this.state.text} onChange={(event)=>this.handleChange(event)} />
            </div>
            <input type="submit" className="btn btn-primary" value="Save" />
        </form>
        );
    }
}

export default TodoForm

