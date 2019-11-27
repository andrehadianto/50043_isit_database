import React, { useEffect, useState, Fragment } from 'react';
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

const CategoryFilter = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [getCategoryAPI, setCategoryAPI] = useState(`${process.env.API_URL}/categories`);
    const [catData, setCatData] = useState([]);

    const onSubmitHandler = (e) => {
        console.log("submitting");
        console.log(e);
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
            <Container>
                    { 
                        isLoading 
                        ? null 
                        : catData.map((catList, index) => {
                                catList.categories.map((cat, index) => {
                                    categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                                })
                            })
                    }
                    <Form onSubmit={ onSubmitHandler }>
                        <Form.Field>
                            <Dropdown
                                style={{ borderTopRightRadius: 0, borderBottomRightRadius: 0 }}
                                placeholder='Filter by category' 
                                options={ categoryOptions }
                                multiple
                                search
                                clearable
                                selection
                            />
                            {/* <Link to={{ pathname: `/categories/` }}> */}
                        <Button 
                            color='teal'
                            type='submit'
                            style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                        >
                            Filter
                        </Button>
                        </Form.Field>
                        {/* </Link> */}
                    </Form>
            </Container>
        </Menu>
    )
}

export default CategoryFilter;