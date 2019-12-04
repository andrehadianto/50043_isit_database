import React, { useState } from 'react';
import axios from 'axios';
import {
    Container,
    Form,
    Button,
    Modal,
    Divider
} from 'semantic-ui-react';

const SignUpMenu = () => {
    const [isInvalid, setIsInvalid] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const onSubmitHandler = (e) => {
        setIsLoading(true);
        const url = `${process.env.API_URL}/user/signup`;
        const username = e.target.elements.username.value;
        const password = e.target.elements.password.value;
        const passwordVerify = e.target.elements.passwordVerify.value;
        const name = e.target.elements.name.value;

        if (password !== passwordVerify) {
            setIsInvalid(true);
            setIsLoading(false);
            alert('Re-entered password is not the same');
        } else {
            const body = {
                "user": username,
                "pwd": password,
                "name": name
            }
            axios.post(
                url,
                body
            )
            .then(res => {
                setIsInvalid(false);
                setIsLoading(false);
                window.location.reload(true);
            })
        }
    }

    return (
        <Modal
            trigger={
                <Container textAlign='center'>
                    New to us? <a href='#'>Sign Up</a>
                </Container>
            }
            size='tiny'
        >
            <Modal.Content style={{ 'padding': 30 }}>
                <Container>
                        <Form size='small' onSubmit={onSubmitHandler}>
                                <Form.Input
                                    error={isInvalid}
                                    name='username'
                                    icon='user'
                                    iconPosition='left'
                                    label='Username'
                                    placeholder='Username'
                                    required
                                    fluid
                                />
                                <Form.Input
                                    error={isInvalid}
                                    name='password'
                                    type='password'
                                    icon='lock'
                                    iconPosition='left'
                                    label='Password'
                                    placeholder='Password'
                                    required
                                    fluid
                                />
                                <Form.Input
                                    error={isInvalid}
                                    name='passwordVerify'
                                    type='password'
                                    icon='lock'
                                    iconPosition='left'
                                    placeholder='Re-enter password'
                                    required
                                    fluid
                                />
                                <Divider hidden/>
                                <Form.Input
                                    error={isInvalid}
                                    name='name'
                                    icon='font'
                                    iconPosition='left'
                                    label='Display Name'
                                    placeholder='Display Name'
                                    required
                                    fluid
                                />
                                <Button
                                    color='teal'
                                    fluid
                                    size='large'
                                    type='submit'
                                    loading={isLoading}
                                >
                                    Sign Up
                                </Button>
                        </Form>
                </Container>
            </Modal.Content>
        </Modal>
    )
}

export default SignUpMenu;