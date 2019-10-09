import React, { Component } from 'react';
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
                <Segment vertical padded>
                    <Grid container verticalAlign='middle'>
                        <Grid.Row>
                            <Header as='h2'>
                                Add new review
                            </Header>
                        </Grid.Row>
                        <Grid.Row>
                            <Form>
                                <Form.Select fluid placeholder='Select book' options={options}/>
                                <Form.TextArea placeholder='How was the book?'/>
                                <Form.Button>Submit</Form.Button>
                            </Form>
                        </Grid.Row>
                    </Grid>
                </Segment>
                <Segment vertical padded>
                    <Grid container verticalAlign='middle'>
                        <Grid.Row>
                            <Header as='h2'>
                                Add new book
                            </Header>
                        </Grid.Row>
                        <Grid.Row>
                            <Form>
                                <Form.Input fluid placeholder='Book title'/>
                                <Form.TextArea placeholder='Description'/>
                                <Form.Input fluid placeholder='price'/>
                                <Form.Select fluid placeholder='Select category' options={options}/>
                                <Form.Button>Submit</Form.Button>
                            </Form>
                        </Grid.Row>
                    </Grid>
                </Segment>
            </div>
        )
    }
}

export default Home;