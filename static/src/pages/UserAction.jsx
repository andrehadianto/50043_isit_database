import React, { Component } from 'react';
import axios from 'axios';
import AddNewBook from '../components/AddNewBook';
import {
    Grid, Container
} from 'semantic-ui-react';

class UserAction extends Component {
    render() {
        return (
            <Grid>
                <AddNewBook/>
            </Grid>
        );
    }
}

export default UserAction;