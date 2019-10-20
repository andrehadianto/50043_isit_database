import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { AppContext } from '../globalContext/AppContext';
import Home from '../pages/Home'
import NotFound from '../pages/NotFound404';

class AppRouter extends Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    render() {
        return (
            <div>
                <AppContext.Provider
                    value={this.state}
                >
                    <BrowserRouter basename="/isit">
                        <Switch>
                            <Route path="/" component={Home}/>
                            <Route component={NotFound}/>
                        </Switch>
                    </BrowserRouter>
                </AppContext.Provider>
            </div>
        );
    }
}

export default AppRouter;