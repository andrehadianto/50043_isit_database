import React, { useState } from 'react';
import { Redirect } from 'react-router-dom';
import _ from 'lodash';
import {
    Button,
    Form,
    Icon
} from 'semantic-ui-react';

let value = '';

const BookSearch = () => {
    const [redirect, setRedirect] = useState(false);

    const searchHandler = (e) => {
        e.preventDefault();
        value = e.target.elements.asin.value;
        console.log(value)
        if (!!value.length) {
            console.log('someting here')
            setRedirect(true);
        }
    }

    if ( redirect ) {
        console.log(`${value} is my value`)
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