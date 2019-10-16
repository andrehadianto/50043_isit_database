import React from 'react';
import { Link } from 'react-router-dom';
import {
    Segment,
    Container,
    Menu,
    Image,
    Button,
    Icon,
    Modal,
    Header,
    Form,
    Message,
    Grid
} from 'semantic-ui-react';

const { Item } = Menu;

const NavBar = () => (
    <Segment inverted vertical size="tiny">
        <Menu inverted size="large">
            <Container>
                <Link to='/'>
                    <Item header>
                        <Image size='mini' src='https://icon-library.net/images/react-icon/react-icon-28.jpg' style={{ marginRight: '1.5em' }} />
                        isit database?
                    </Item>
                </Link>
                <Item position='right'> 
                    <Modal
                        trigger={
                            <Button icon as='a'inverted labelPosition='left'>
                                <Icon inverted name='sign in'/>
                                Log in
                            </Button>}
                        style={{ maxWidth: '450px' }}
                    >
                        <Modal.Content>
                                <Grid textAlign='center' verticalAlign='middle'>
                                    <Grid.Column>
                                        <Header as='h2' color='blue' textAlign='center'>
                                            <Image src='https://icon-library.net/images/react-icon/react-icon-28.jpg' /> Log-in to your account
                                        </Header>
                                        <Form size='large'>
                                            <Segment stacked>
                                            <Form.Input fluid icon='user' iconPosition='left' placeholder='Username' />
                                            <Form.Input
                                                fluid
                                                icon='lock'
                                                iconPosition='left'
                                                placeholder='Password'
                                                type='password'
                                            />

                                            <Button color='blue' fluid size='large'>
                                                Login
                                            </Button>
                                            </Segment>
                                        </Form>
                                        <Message>
                                            New to us? <a href='#'>Sign Up</a>
                                        </Message>
                                    </Grid.Column>
                            </Grid>
                        </Modal.Content>
                    </Modal>

                </Item>
            </Container>
        </Menu>
    </Segment>
);

export default NavBar;