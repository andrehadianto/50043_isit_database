import React, { useEffect, useState } from 'react';
import { Redirect } from 'react-router-dom';
import axios from 'axios';
import {
    Menu,
    Container,
    Dropdown,
    Button,
    Form,
    Popup
} from 'semantic-ui-react';

let filter = []

const CategoryFilter = () => {
    const [getCategoryAPI, setCategoryAPI] = useState(`${process.env.API_URL}/categories`);
    const [redirect, setRedirect] = useState(false);
    const [isInvalid, setIsInvalid] = useState(false);
    const categoryOptions = []

    const categorySelectionHandler = (e, data) => {
        filter = data.value;
    }

    const redirectHandler = () => {
        if (!!filter.length) {
            setRedirect(true);
        } else {
            setIsInvalid(true)
        }
    }

    useEffect(() => {
        if (sessionStorage.getItem('categories') == null) {
            axios.get(
                getCategoryAPI
            )
            .then(res => {
                sessionStorage.setItem('categories', JSON.stringify(res.data));
                JSON.parse(sessionStorage.getItem('categories')).map((catList, index) => {
                    catList.categories.map((cat, index) => {
                        categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                    })
                })
            });
        } else {
            JSON.parse(sessionStorage.getItem('categories')).map((catList, index) => {
                catList.categories.map((cat, index) => {
                    categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                })
            })
        }
    }, []);

    if (redirect) {
        return ( <Redirect to={{pathname: '/filter', state: {filter: filter}}}/> )
    } else {
        return (
            <Menu secondary inverted size="small">
                <Container textAlign='center'>
                    <Form style={{ width: 'inherit'}}>
                        <Form.Group>
                            <Popup
                                content='Filter cannot be empty'
                                trigger={
                                    <Dropdown
                                        style={{ borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
                                        placeholder='Filter by category' 
                                        options={ categoryOptions }
                                        onChange={ categorySelectionHandler }
                                        multiple
                                        search
                                        clearable
                                        selection
                                        fluid
                                    />
                                }
                                position='bottom left'
                                open={ isInvalid }
                            />
                            <Button 
                                color='teal'
                                type='button'
                                style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                                onClick={ redirectHandler }
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