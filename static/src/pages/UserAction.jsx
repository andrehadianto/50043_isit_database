import React, { Component } from 'react';
import AddNewBook from '../pages/AddNewBook';
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