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
    Grid,
    Dropdown
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
                    {
                        sessionStorage.getItem('name') && sessionStorage.getItem('userId') && sessionStorage.getItem('token')
                        ? 
                            <Dropdown
                                text={sessionStorage.getItem('name')}
                                icon='user'
                                labeled
                                button
                                className='icon'
                            >
                                <Dropdown.Menu>
                                    <Dropdown.Item text='Log Out' value='logout' icon='sign-out'/>
                                </Dropdown.Menu>
                            </Dropdown>
                        :                     
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
                    }


                </Item>
            </Container>
        </Menu>
    </Segment>
);

export default NavBar;