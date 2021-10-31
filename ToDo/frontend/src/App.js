import React from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';
import UserList from './components/User.js';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'users': []
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
                const users = response.data
                this.setState(
                            {
                               'users': users
                            }
                )
            }).catch(error => console.log(error))
    }

    render () {
        return (
            <div>
                <UserList users={this.state.users} />
            </div>
        )
    }
}

export default App;
