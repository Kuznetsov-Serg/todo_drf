import React from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie';
import logo from './logo.svg';
import './App.css';
import {HashRouter, BrowseRouter, Route, Link, Switch, Redirect} from "react-router-dom"

import MainMenu from './components/MainMenu.js';
import Footer from './components/Footer.js';
import UserList from './components/User.js';
import UserDetail from './components/UserDetail.js';
import ProjectList from './components/Project.js';
import ProjectDetail from './components/ProjectDetail.js';
import ProjectForm from './components/ProjectForm.js';
import ProjectUpdate from './components/ProjectUpdate.js';
import TodoList from './components/Todo.js';
import TodoForm from './components/TodoForm.js';
import LoginForm from './components/Auth.js';
import NotFound404 from './components/NotFound404.js';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'projects': [],
            'todo': [],
            'token': '',
            'username': '',
        }
    }

    set_token(token) {
        const cookies = new Cookies()
        cookies.set('token', token)
        this.setState({'token': token}, () => this.load_data())
    }

    get_token_from_storage() {
        const cookies = new Cookies()
        const token = cookies.get('token')
        this.setState({'token': token}, () => this.load_data())
    }

    is_authenticated() {
//        return this.state.token != ''     // Так иногда при первом запросе косячит (со слов преподавателя)
        return !!this.state.token
    }

    logout() {
        this.set_token('')
        this.setState({'username': ''})
    }

    get_token(username, password) {
        axios.post('http://127.0.0.1:8000/api-token-auth/', {username: username, password: password})
        .then(response => {
            console.log(response.data)
            this.set_token(response.data['token'])
            this.setState({'username': username})
            console.log(this.state.username)
            // Вариант хранения Token в localStorage
//            localStorage.setItem('token', response.data.token)
//            let token = localStorage.getItem('token')
//            console.log(token)
        }).catch(error => alert('Неверный логин или пароль'))
    }

    get_headers() {
        let headers = {
            'Accept':'application/json; version=v2',     // для поддержки версионности API через AcceptHeaderVersioning
            'Content-Type':'application/json'
        }
        if (this.is_authenticated()){
                headers['Authorization'] = 'Token ' + this.state.token
            }
        return headers
    }

    componentDidMount() {
        this.get_token_from_storage()
    }

    load_data() {
        const headers = this.get_headers()
        axios.get('http://127.0.0.1:8000/api/users/', {headers})
            .then(response => {
//                const users = response.data             // обычно берем данные так
                const users = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'users': users
                            }
                )
            }).catch(error => {
                                this.setState({users:[]})
                                console.log(error)
                                }
                )
        axios.get('http://127.0.0.1:8000/api/projects/', {headers})
            .then(response => {
                const projects = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'projects': projects
                            }
                )
            }).catch(error => {
                                this.setState({projects:[]})
                                console.log(error)
                                }
                )
        axios.get('http://127.0.0.1:8000/api/todo/', {headers})
            .then(response => {
                const todo = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'todo': todo
                            }
                )
            }).catch(error => {
                                this.setState({todo:[]})
                                console.log(error)
                                }
                )
    }

    createProject (name, repository_url, users) {
        const headers = this.get_headers()
        const data = {name: name, repository_url: repository_url, users: users}
        console.log(data)
        axios.post('http://127.0.0.1:8000/api/projects/', data, {headers})
            .then(response => {
//                let new_project = response.data
//                const user = this.state.users.filter((item) => item.id === new_project.users)[0]
//                new_book.author = author
//                this.setState({books: [...this.state.books, new_book]})
                this.load_data()    // лучше перезапрашивать данные, на случай если кто-то еще правит БД
            }).catch(error => {console.log(error)})
    }

    updateProject (id, name, repository_url, users) {
        const headers = this.get_headers()
        const data = {id: id, name: name, repository_url: repository_url, users: users}
        console.log('data before update',data)
        axios.put(`http://127.0.0.1:8000/api/projects/${id}/`, data, {headers})
            .then(response => {
                this.load_data()
            }).catch(error => {console.log(error)})
    }

    deleteProject (id) {
        const headers = this.get_headers()
        console.log('Id deleted project =', id)
        axios.delete(`http://127.0.0.1:8000/api/projects/${id}`, {headers})
            .then(response => {
//                this.setState(
//                            {
//                                projects: this.state.projects.filter((item)=>item.id !== id)
//                            }
//                    )
                this.load_data()    // лучше перезапрашивать данные, на случай если кто-то еще правит БД
            }).catch(error => {console.log(error)})
    }

    createTodo (project, user, title, text) {
        const headers = this.get_headers()
        const data = {project: project, user: user, title: title, text: text}
        console.log('data = ', data)
        axios.post('http://127.0.0.1:8000/api/todo/', data, {headers})
            .then(response => {
                this.load_data()    // лучше перезапрашивать данные, на случай если кто-то еще правит БД
            }).catch(error => {console.log(error)})
    }

    deleteTodo (id) {
        const headers = this.get_headers()
        console.log('Id deleted todo =', id)
        axios.delete(`http://127.0.0.1:8000/api/todo/${id}`, {headers})
            .then(response => {
                this.load_data()    // лучше перезапрашивать данные, на случай если кто-то еще правит БД
            }).catch(error => {console.log(error)})
    }

    render () {
        return (
            <div>
                <HashRouter>
                    <MainMenu />

                    {this.is_authenticated() ?
                        <button type="button" class="btn btn-info" onClick={() => this.logout()}>Logout {this.state.username}</button> :
                        <button type="button" class="btn btn-info"><Link to='/login'>Login</Link></button>
                    }
                    <Switch>
                        <Route exact path='/' component={() => <UserList users={this.state.users} />} />
                        <Route exact path='/projects' component={() => <ProjectList projects={this.state.projects} users={this.state.users} deleteProject={(id)=>this.deleteProject(id)} updateProject={(id)=>this.updateProject(id)} />} />
                        <Route exact path='/todo' component={() => <TodoList todo={this.state.todo} users={this.state.users} deleteTodo={(id)=>this.deleteTodo(id)} />} />
                        <Route exact path='/todo/create' component={() => <TodoForm projects={this.state.projects} users={this.state.users} createTodo={(project,user,title,text) => this.createTodo(project,user,title,text)} />} />
                        <Route exact path='/project/:id'>
                            <ProjectDetail projects={this.state.projects} users={this.state.users} todo={this.state.todo} />
                        </Route>
                        <Route exact path='/projects/create' component={() => <ProjectForm users={this.state.users} createProject={(name,repository_url,users) => this.createProject(name,repository_url,users)} />} />
                        <Route exact path='/project/update/:id' component={() => <ProjectUpdate projects={this.state.projects}  users={this.state.users} updateProject={(id,name,repository_url,users) => this.updateProject(id,name,repository_url,users)} />} />
                        <Route exact path='/user/:id'>
                            <UserDetail all_obj={this.state} />
                        </Route>
                        <Route exact path='/login' component={() => <LoginForm get_token={(username, password) => this.get_token(username, password)} />} />
                        <Route component={NotFound404} />
                    </Switch>
                </HashRouter>
                <Footer />
            </div>
        )
    }
}

export default App;
