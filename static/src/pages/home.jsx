import React, { Component } from 'react';
import AddReview from '../components/AddReview';
import AddNewBook from '../components/AddNewBook';
import {
    Menu,
    Container,
    Image,
    Button,

    Segment,
    Grid,
    Header,
    Form
} from 'semantic-ui-react';

const { Item } = Menu;

const options = [
    { key: 'm', text: 'Male', value: 'male' },
    { key: 'f', text: 'Female', value: 'female' },
    { key: 'o', text: 'Other', value: 'other' },
  ]

class Home extends Component {
    render() {
        return (
            <div>
                <Segment inverted vertical size="tiny">
                    <Menu inverted size="large">
                        <Container>
                            <Item as='a' header>
                                <Image size='mini' src="https://icon-library.net/images/react-icon/react-icon-28.jpg" style={{ marginRight: '1.5em' }} />
                                isit database?
                            </Item> 
                            <Item position='right' name='login'> 
                                <Button as='a'inverted>
                                    Log in
                                </Button>
                            </Item>              
                        </Container>
                    </Menu>
                </Segment>

                <Segment vertical padded>
                    <Grid container verticalAlign='middle'>
                        <Grid.Row>
                            <Header as='h2'>
                                See some reviews
                            </Header>
                        </Grid.Row>
                    </Grid>
                </Segment>
                <AddReview options={options}/>
                <AddNewBook options={options}/>
            </div>
        )
    }
}

export default Home;