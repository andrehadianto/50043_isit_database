import React, { Component, Fragment } from 'react';
import { Switch, Route } from 'react-router-dom';
import NavBar from '../components/NavBar';
import AllBooks from '../components/AllBooks';
import FilteredBooks from '../components/FilteredBooks';
import CategoryFilter from '../components/CategoryFilter';
import BookSearch from '../components/BookSearch';
import BookDetails from './BookDetails';
import AddNewBook from './AddNewBook';
import SeeLogList from './SeeLogList';
import LogPreview from './LogPreview';
import {
    Container,
    Segment,
    Header,
    Menu
} from 'semantic-ui-react';

const HomepageBanner = () => {
    return (
        <Container 
            text
            style={{
                alignItems: "center",
                minHeight: 400,
                padding: "1em 0em"
            }}
        >
            <Header
                as='h1'
                content='Book archive website'
                inverted
                style={{
                    fontSize: '4em',
                    fontWeight: 'normal',
                    marginBottom: 0,
                    marginTop: '1em',
                }}
            />
            <Header
                as='h2'
                content='Forget physical library. The future is now, old man.'
                inverted
                style={{
                    fontSize: '1.4em',
                    fontWeight: 'normal',
                    marginTop: '1.5em',
                }}
            />
        </Container>
    )
}

class Home extends Component {
    render() {
        return (
            <Fragment>
                <Segment
                    inverted
                    textAlign='center'
                    vertical
                >
                    <NavBar/>
                    <Route exact path='/'>
                        <Menu secondary inverted size='small'>
                            <Container style={{ display: 'flex' }}>
                                <BookSearch/>
                                <CategoryFilter/>
                            </Container>
                        </Menu>
                        <HomepageBanner/>
                    </Route>
                    <Route exact path='/filter' component={CategoryFilter}/>
                </Segment>
                <Container style={{marginTop: '2em', marginBottom: '4em'}}>
                    <Switch>
                        <Route exact path='/' component={AllBooks}/>
                        <Route exact path='/filter' component={FilteredBooks}/>
                        <Route path='/user_action/new_book' component={AddNewBook}/>
                        <Route exact path='/user_action/logs/:id' component={LogPreview}/>
                        <Route exact path='/user_action/logs' component={SeeLogList}/>
                        <Route exact path='/review/:asin' component={(props) => (<BookDetails timestamp={new Date().toString()} {...props} />)}/>
                    </Switch>
                </Container>
            </Fragment>
        )
    }
}

export default Home;