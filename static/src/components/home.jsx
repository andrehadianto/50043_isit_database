import React, { Component } from 'react';
import {
    Menu,
    Container,
    Image,
    Button
} from 'semantic-ui-react';

const { Item } = Menu;

class Home extends Component {
    render() {
        return (
            <div>
                <Menu fixed='top' inverted>
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
            </div>
        )
    }
}

export default Home;