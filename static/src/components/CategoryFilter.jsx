import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
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
    const [isLoading, setIsLoading] = useState(true);
    const [getCategoryAPI, setCategoryAPI] = useState(`${process.env.API_URL}/categories`);
    const [catData, setCatData] = useState([]);

    const onSubmitHandler = (e) => {
        console.log(filter)
        if (!!!filter.length) {
            console.log('filter is empty')
        } else {
            const body = {
                "categoryArray": filter
            };
            const header = {
                "Content-type": "application/json"
            };
            axios.post(
                `${process.env.API_URL}/books/category?page=1&count=24`, 
                body,
                header
            ).then(res => {
                console.log(res)
            })
        }
    }

    const categorySelectionHandler = (e, data) => {
        filter = data.value;
    }

    useEffect(() => {
        axios.get(
            getCategoryAPI
        )
        .then(res => {
            setCatData(res.data);
            setIsLoading(false);
        });
    }, []);

    return (
        <Menu secondary inverted size="small">
            <Container textAlign='center'>
                    { 
                        isLoading 
                        ? null 
                        : catData.map((catList, index) => {
                                catList.categories.map((cat, index) => {
                                    categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                                })
                            })
                    }
                    <Form style={{ width: 'inherit'}} onSubmit={ onSubmitHandler }>
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
                            {/* <Link to={{ pathname: `/categories/` }}> */}
                            <Button 
                                color='teal'
                                type='submit'
                                style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                            >
                                Filter
                            </Button>
                        </Form.Group>
                        {/* </Link> */}
                    </Form>
            </Container>
        </Menu>
    )
}

export default CategoryFilter;