import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import Home from '../pages/Home'
import NotFound from '../pages/NotFound404';

class AppRouter extends Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div>
            <BrowserRouter basename="/isit">
                <Switch>
                    <Route path="/" component={Home}/>
                    <Route component={NotFound}/>
                </Switch>
            </BrowserRouter>
            </div>

        );
    }
}

export default AppRouter;