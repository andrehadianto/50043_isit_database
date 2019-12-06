import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import _ from 'lodash';
import {
    Button,
    Form,
    Icon
} from 'semantic-ui-react';

const BookSearch = () => {
    const [redirect, setRedirect] = useState(false);

    const searchHandler = (e) => {
        e.preventDefault();
        const value = e.target.elements.asin.value;
        if (!!value.length) {
            setRedirect(true);
        }
    }

    if ( redirect ) {
        return ( <Redirect to={{pathname: `/review/${value}`}}/> )
    } else {
        return (
            <Form onSubmit={ searchHandler }>
                <Form.Group>
                    <Button 
                        icon
                        labelPosition='left'
                        color='teal'
                        type='submit'
                        style={{ borderTopRightRadius: 0, borderBottomRightRadius: 0, marginRight: 0 }}
                    >
                        <Icon name='search'/>
                        Search
                    </Button>
                    <Form.Field style={{ width: '-webkit-fill-available', borderTopLeftRadius: 0, borderBottomLeftRadius: 0, paddingLeft: 0 }}>
                        <input
                            style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                            name='asin'
                            placeholder='Search by book asin'
                            required
                        />
                    </Form.Field>
                </Form.Group>
            </Form>
        )
    }
}

export default BookSearch;