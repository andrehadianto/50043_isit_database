import React, { useState, useEffect } from 'react';
import { Redirect } from 'react-router-dom';
import _ from 'lodash';
import {
    Button,
    Form,
    Icon,
    Search
} from 'semantic-ui-react';
import axios from 'axios';

const BookSearch = (props) => {
    const [redirect, setRedirect] = useState(false);
    const [getTitlesAPI, setTitlesAPI] = useState(`${process.env.API_URL}/books_titles`);
    const [results, setResults] = useState([]);
    const [searchLoading, setSearchLoading] = useState(false);
    const [strings, setStrings] = useState('');
    const [source, setSource] = useState([]);
    const [redirectASIN, setRedirectASIN] = useState('');
    
    useEffect(() => {
        axios.get(
            getTitlesAPI
        )
        .then(res => {
            const modifiedSource = res.data.titles.map(book => ({title: book.title, key: book.asin}));
            setSource(modifiedSource);
        })
    }, [])

    const searchHandler = (e) => {
        e.preventDefault();
        if (!!strings.length) {
            let i;
            for (i = 0; i < source.length; i++) {
                if (source[i].title == strings) {
                    setRedirectASIN(source[i].key)
                    setRedirect(true);
                }
            }
        }
    }

    const handleSearchChange = (e, { value }) => {
        setSearchLoading(true);
        setStrings(value);
    }

    useEffect(() => {
        setTimeout(() => {
            if (strings.length < 1) {
                setSearchLoading(false);
                setResults([]);
                setStrings('');
            };
            const re = new RegExp(_.escapeRegExp(strings), 'i')
            const isMatch = (result) => re.test(result.title);
            setSearchLoading(false);
            setResults([..._.filter(source, isMatch)])
        }, 300)
    }, [strings])

    if ( redirect ) {
        return ( <Redirect to={{pathname: `/review/${redirectASIN}`}}/> )
    } else {
        return (
            <Form onSubmit={searchHandler}>
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
                    <Search
                        style={{ width: '-webkit-fill-available', borderTopLeftRadius: 0, borderBottomLeftRadius: 0, paddingLeft: 0 }}
                        loading={ searchLoading }
                        onResultSelect={(e, {result}) => {setStrings(result.title)}}
                        onSearchChange={_.debounce(handleSearchChange, 500, {leading: true})}
                        results={results}
                        value={strings}
                        fluid
                        placeholder='Search by book title'
                        {...props}
                    />
                </Form.Group>
            </Form>
        )
    }
}

export default BookSearch;