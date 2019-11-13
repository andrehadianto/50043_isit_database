import React from 'react';
import { Link } from 'react-router-dom';
import LoginMenu from './LoginMenu';
import {
    Segment,
    Container,
    Menu,
    Button,
    Icon,
    Modal,
    Grid,
    Dropdown
} from 'semantic-ui-react';

const { Item } = Menu;

const NavBar = () => {
    const onLogOut = () => {
        sessionStorage.clear();
        window.location.replace('/isit');
    }

    return (
        <Segment inverted vertical size="tiny">
            <Menu inverted size="large">
                <Container>
                    <a href='/isit'>
                        <Item header>
                            <Icon name='bomb' size='large'/>
                            isit database?
                        </Item>
                    </a>
                    <Item position='right'> 
                        {
                            sessionStorage.getItem('name') && sessionStorage.getItem('id') && sessionStorage.getItem('token')
                            ?
                                <Dropdown
                                    text={sessionStorage.getItem('name')}
                                    icon='user'
                                    labeled
                                    button
                                    className='icon'
                                >
                                    <Dropdown.Menu>
                                        <Dropdown.Item text='Add New Book' value='addBook' icon='book' as={ Link } to='/user_action/new_book'/>
                                        <Dropdown.Item text='See Logs' value='seeLogs' icon='eye' as={ Link } to='/user_action/logs'/>
                                        <Dropdown.Divider/>
                                        <Dropdown.Item text='Log Out' value='logout' icon='sign-out' onClick={onLogOut}/>
                                    </Dropdown.Menu>
                                </Dropdown>
                            :
                                <LoginMenu/>
                        }


                    </Item>
                </Container>
            </Menu>
        </Segment>
    )
};

export default NavBar;