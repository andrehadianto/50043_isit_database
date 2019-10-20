import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import LoginMenu from './LoginMenu';
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
                                    <LoginMenu/>
                            </Grid>
                        </Modal.Content>
                    </Modal>

                </Item>
            </Container>
        </Menu>
    </Segment>
);

export default NavBar;