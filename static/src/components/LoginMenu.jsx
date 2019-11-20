import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import SignUpMenu from './SignUpMenu';
import {
    Grid,
    Form,
    Header,
    Button,
    Segment,
    Icon,
    Modal
} from 'semantic-ui-react';

const LoginMenu = () => {
    const [isInvalid, setIsInvalid] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const onSubmitHandler = (e) => {
        setIsLoading(true);
        const url = `${process.env.API_URL}/user/login`;
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
            setIsLoading(false);
            if (res.data.name !== undefined) {
                setIsInvalid(false);
                sessionStorage.setItem('name', res.data.name);
                sessionStorage.setItem('id', res.data.id);
                sessionStorage.setItem('token', res.data.token);
                if (window.location.pathname === '/isit/') {
                    window.location.replace('/isit');
                }
                window.location.reload(true);
            } else {
                setIsInvalid(true);
            }
        })
        .catch(err => (console.log(err)));
    }
    
    return (
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
                            <Icon name='bomb' size='large'/>
                            Log-in to your account
                        </Header>
                        <Form size='large' onSubmit={onSubmitHandler}>
                            <Segment stacked>
                                <Form.Input
                                    error={isInvalid}
                                    name='username'
                                    fluid 
                                    icon='user' 
                                    iconPosition='left' 
                                    placeholder='Username' 
                                    required
                                />
                                <Form.Input
                                    error={isInvalid}
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
                                    loading={isLoading}
                                >
                                    Login
                                </Button>
                            </Segment>
                        </Form>
                        <Modal.Actions>
                            <SignUpMenu/>
                        </Modal.Actions>
                    </Grid.Column>
                </Grid>
            </Modal.Content>
        </Modal>
    );
};

export default LoginMenu;