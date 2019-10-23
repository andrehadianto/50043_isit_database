import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import _ from 'lodash';
import {
    Grid,
    Segment,
    Header,
    Pagination,
    Placeholder,
    Item,
    Container
} from 'semantic-ui-react';

const AlsoBought = () => {
    const [activePage, setActivePage] = useState(1);
    const [bookData, setBookData] = useState([]);
    const [getBookApiUrl, setGetBookApiUrl] = useState('http://localhost:5000/books?page=1&count=18');
    const [isLoading, setIsLoading] = useState(true);
}

export default AlsoBought;