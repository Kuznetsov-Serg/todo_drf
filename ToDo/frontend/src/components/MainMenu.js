//import React from 'react';
import {Link} from 'react-router-dom'

var style = {
    backgroundColor: "#F8F8F8",
    borderTop: "1px solid #E7E7E7",
    textAlign: "center",
    padding: "20px",
    left: "0",
//    bottom: "0",
    height: "60px",
    width: "100%",
};

const MainMenu = () => {
    return (
        <div style={style}>
            <button type="button" class="btn btn-link" Link><Link to='/'>Users</Link></button>
            <button type="button" class="btn btn-link"><Link to='/projects'>Projects</Link></button>
            <button type="button" class="btn btn-link"><Link to='/todo'>ToDo</Link></button>

            <button type="button" class="btn btn-primary">Primary</button>
            <button type="button" class="btn btn-secondary">Secondary</button>
            <button type="button" class="btn btn-success">Success</button>
            <button type="button" class="btn btn-danger">Danger</button>
            <button type="button" class="btn btn-warning">Warning</button>
            <button type="button" class="btn btn-info">Info</button>
            <button type="button" class="btn btn-light">Light</button>
            <button type="button" class="btn btn-dark">Dark</button>

            <button type="button" class="btn btn-link">Link</button>
        </div>
    );
};

export default MainMenu;
