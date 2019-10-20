import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { AppContext } from '../globalContext/AppContext';
import {
    Grid,
    Form,
    Header,
    Button,
    Segment,
    Message,
    Image
} from 'semantic-ui-react';

const LoginMenu = () => {
    const globalContext = useContext(AppContext);

    const onSubmitHandler = (e) => {
        const url = `http://localhost:5000/user/login`;
        const username = e.target.elements.username.value;
        const password = e.target.elements.password.value;

        const body = {
            "user": username,
            "pwd": password
        }
        axios.post(
            url,
            body
        )
        .then(res => {
            if (res.data.name !== undefined) {
                globalContext.name = res.data.name
                globalContext.userId = res.data.id;
                globalContext.token = res.data.token;
            } else {
                alert(res.data.message);
            }
        })
        .catch(err => (console.log(err)));
    }
    
    return (
        <Grid.Column>
            <Header as='h2' color='blue' textAlign='center'>
                <Image src='https://icon-library.net/images/react-icon/react-icon-28.jpg' />
                Log-in to your account
            </Header>
            <Form size='large' onSubmit={onSubmitHandler}>
                <Segment stacked>
                <Form.Input 
                    name='username'
                    fluid 
                    icon='user' 
                    iconPosition='left' 
                    placeholder='Username' 
                    required
                />
                <Form.Input
                    name='password'
                    fluid
                    icon='lock'
                    iconPosition='left'
                    placeholder='Password'
                    type='password'
                    required
                />

                <Button 
                    color='blue' 
                    fluid 
                    size='large'
                    type='submit'
                >
                    Login
                </Button>
                </Segment>
            </Form>
            <Message>
                New to us? <a href='#'>Sign Up</a>
            </Message>
        </Grid.Column>
    );
};

export default LoginMenu;