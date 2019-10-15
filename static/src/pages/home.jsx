import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import _ from 'lodash';
import AddReview from '../components/AddReview';
import AddNewBook from '../components/AddNewBook';
import NavBar from '../components/NavBar';
import AllBooks from '../components/AllBooks';
import BookDetails from './BookDetails';

import {
    Container,

    Message,
    Segment,
    Grid,
    Header
} from 'semantic-ui-react';

const options = [
    { key: 'm', text: 'Male', value: 'male' },
    { key: 'f', text: 'Female', value: 'female' },
    { key: 'o', text: 'Other', value: 'other' },
  ]

const tmp_columns = _.times(100, (i) => (
    <Message compact key={i}>Hi</Message>
))

class Home extends Component {
    render() {
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
                        <Route exact path='/review/:asin' component={BookDetails}/>
                    </Switch>





                    <Segment.Group>
                        <Segment padded>
                            <Grid container verticalAlign='middle'>
                                <Grid.Column style={{minWidth: 600}}>
                                    <Header as='h2'>
                                        See some reviews
                                    </Header>
                                </Grid.Column>
                            </Grid>
                        </Segment>
                        <AddReview options={options}/>
                        <AddNewBook options={options}/>
                    </Segment.Group>
                </Container>
            </div>
        )
    }
}

export default Home;