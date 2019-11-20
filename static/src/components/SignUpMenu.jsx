import React, { useState } from 'react';
import axios from 'axios';
import {
    Grid,
    Form,
    Header,
    Button,
    Segment,
    Modal,
    Message,
    Divider
} from 'semantic-ui-react';

const SignUpMenu = () => {
    const [isInvalid, setIsInvalid] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [isOpen, setIsOpen] = useState(false);

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
                <Message>
                    New to us? <a href='#'>Sign Up</a>
                </Message>
            }
            style={{ maxWidth: '600px' }}
        >
            <Modal.Content>
                <Grid>
                    <Grid.Column>
                        <Header as='h2' color='red' textAlign='center'>
                            Create your very own account!
                        </Header>
                        <Form size='large' onSubmit={onSubmitHandler}>
                            <Segment>
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
                                    type='password'
                                    fluid
                                    icon='lock'
                                    iconPosition='left'
                                    placeholder='Password'
                                    required
                                />
                                <Form.Input
                                    error={isInvalid}
                                    name='passwordVerify'
                                    type='password'
                                    fluid
                                    icon='lock'
                                    iconPosition='left'
                                    placeholder='Re-enter password'
                                    required
                                />
                                <Divider hidden/>
                                <Form.Input
                                    error={isInvalid}
                                    name='name'
                                    fluid
                                    icon='font'
                                    iconPosition='left'
                                    placeholder='Display Name'
                                    required
                                />
                                <Button
                                    color='youtube'
                                    fluid
                                    size='large'
                                    type='submit'
                                    loading={isLoading}
                                >
                                    Sign Up
                                </Button>
                            </Segment>
                        </Form>
                    </Grid.Column>
                </Grid>
            </Modal.Content>
        </Modal>
    )
}

export default SignUpMenu;