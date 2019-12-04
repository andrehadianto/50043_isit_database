import React, { useEffect, useState } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import {
    Menu,
    Container,
    Dropdown,
    Button,
    Form
} from 'semantic-ui-react';

const categoryOptions = []
let filter = []

const CategoryFilter = () => {
    const [getCategoryAPI, setCategoryAPI] = useState(`${process.env.API_URL}/categories`);
    const [redirect, setRedirect] = useState(false);

    const categorySelectionHandler = (e, data) => {
        filter = data.value;
    }

    useEffect(() => {
        if (sessionStorage.getItem('categories') == null) {
            axios.get(
                getCategoryAPI
            )
            .then(res => {
                sessionStorage.setItem('categories', JSON.stringify(res.data));
            });
        }
        JSON.parse(sessionStorage.getItem('categories')).map((catList, index) => {
            catList.categories.map((cat, index) => {
                categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
            })
        })
    }, []);

    if (redirect) {
        return ( <Redirect to={{pathname: '/filter', state: {filter: filter}}}/> )
    } else {
        return (
            <Menu secondary inverted size="small">
                <Container textAlign='center'>
                    <Form style={{ width: 'inherit'}}>
                        <Form.Group>
                            <Dropdown
                                style={{ borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
                                placeholder='Filter by category' 
                                options={ categoryOptions }
                                id='idd'
                                onChange={ categorySelectionHandler }
                                multiple
                                search
                                clearable
                                selection
                                fluid
                            />
                            <Button 
                                color='teal'
                                type='submit'
                                style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                                onClick={() => {setRedirect(true)}}
                            >
                                Filter
                            </Button>
                        </Form.Group>
                    </Form>
                </Container>
            </Menu>
        )
    }
}

export default CategoryFilter;