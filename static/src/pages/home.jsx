import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import _ from 'lodash';
import NavBar from '../components/NavBar';
import AllBooks from '../components/AllBooks';
import BookDetails from './BookDetails';
import AddNewBook from './AddNewBook';
import SeeLogList from './SeeLogList';
import LogPreview from './LogPreview';
import {
    Container,
    Segment,
    Grid,
    Header
} from 'semantic-ui-react';

class Home extends Component {
    render() {
        console.log(`${process.env.API_URL}`);
        return (
            <div>
                <NavBar/>
                <Container style={{marginTop: '2em', marginBottom: '4em'}}>
                    <Switch>
                        <Route exact path='/'>
                            <Grid>
                                <Grid.Row>
                                    <Grid.Column width={4}>
                                        <Segment>
                                            <Header as='h3' dividing>
                                                Hello
                                            </Header>
                                        </Segment>
                                    </Grid.Column>
                                    <AllBooks/>
                                </Grid.Row>
                            </Grid>
                        </Route>
                        <Route path='/user_action/new_book' component={AddNewBook}/>
                        <Route exact path='/user_action/logs/:id' component={LogPreview}/>
                        <Route exact path='/user_action/logs' component={SeeLogList}/>
                        <Route exact path='/review/:asin' component={(props) => (<BookDetails timestamp={new Date().toString()} {...props} />)}/>
                    </Switch>
                </Container>
            </div>
        )
    }
}

export default Home;