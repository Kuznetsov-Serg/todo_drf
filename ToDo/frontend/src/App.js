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
import TodoList from './components/Todo.js';
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
            'Content-Type': 'application/json'
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
                        <Route exact path='/projects' component={() => <ProjectList projects={this.state.projects} users={this.state.users} />} />
                        <Route exact path='/todo' component={() => <TodoList todo={this.state.todo} />} />
                        <Route exact path='/project/:id'>
                            <ProjectDetail projects={this.state.projects} users={this.state.users} todo={this.state.todo} />
                        </Route>
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
