import React from 'react';
import { Link } from 'react-router-dom';
import {
    Segment,
    Container,
    Menu,
    Image,
    Button,
    Icon
} from 'semantic-ui-react';

const { Item } = Menu;

const NavBar = () => (
    <Segment inverted vertical size="tiny">
        <Menu inverted size="large">
            <Container>
                <Link to='/'>
                    <Item header>
                        <Image size='mini' src="https://icon-library.net/images/react-icon/react-icon-28.jpg" style={{ marginRight: '1.5em' }} />
                        isit database?
                    </Item>
                </Link>
                <Item position='right'> 
                    <Button icon as='a'inverted labelPosition='left'>
                        <Icon inverted name='sign in'/>
                        Log in
                    </Button>
                </Item>
            </Container>
        </Menu>
    </Segment>
);

export default NavBar;