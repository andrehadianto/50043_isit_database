import React, { useState } from 'react';
import axios from 'axios';
import SignUpMenu from './SignUpMenu';
import {
    Form,
    Button,
    Icon,
    Modal,
    Container,
    Divider
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
            size='tiny'
        >
            <Modal.Content style={{ 'padding': 30 }}>
                <Container>
                    <Form size='small' onSubmit={onSubmitHandler}>
                        <Form.Input
                            error={isInvalid}
                            name='username'
                            label='Username'
                            placeholder='Username' 
                            required
                            fluid 
                        />
                        <Form.Input
                            error={isInvalid}
                            name='password'
                            label='Password'
                            placeholder='Password'
                            type='password'
                            required
                            fluid
                        />
                        <Button 
                            color='blue' 
                            size='large'
                            type='submit'
                            loading={isLoading}
                            fluid 
                        >
                            Login
                        </Button>
                    </Form>

                    <Divider hidden/>

                    <Modal.Actions>
                        <SignUpMenu/>
                    </Modal.Actions>
                </Container>
            </Modal.Content>
        </Modal>
    );
};

export default LoginMenu;