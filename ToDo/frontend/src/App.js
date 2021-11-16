import React from 'react';
import axios from 'axios';
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
import NotFound404 from './components/NotFound404.js';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': [],
            'projects': [],
            'todo': [],
        }
    }
    componentDidMount() {

//        const users = [
//            {
//               'username': 'kuznetsov',
//               'first_name': 'Фёдор',
//               'last_name': 'Достоевский',
//               'email': 'ksn@netqis.com'
//            },
//            {
//               'username': 'ivanov',
//               'first_name': 'Иван',
//               'last_name': 'Достоевский',
//               'email': 'ivanov@netqis.com'
//            },
//            ]
//        this.setState({
//                       'users': users
//                    })
        axios.get('http://127.0.0.1:8000/api/users/')
            .then(response => {
//                const users = response.data             // обычно берем данные так
                const users = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'users': users
                            }
                )
            }).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8000/api/projects/')
            .then(response => {
                const projects = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'projects': projects
                            }
                )
            }).catch(error => console.log(error))

        axios.get('http://127.0.0.1:8000/api/todo/')
            .then(response => {
                const todo = response.data.results     // после ввода paginator возвращает словарь --> список в results
                this.setState(
                            {
                               'todo': todo
                            }
                )
            }).catch(error => console.log(error))
    }

    render () {
        return (
            <div>
                <HashRouter>
                    <MainMenu />
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
                        <Route component={NotFound404} />
                    </Switch>
                </HashRouter>
                <Footer />
            </div>
        )
    }
}

export default App;
