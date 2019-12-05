import React, { useEffect, useState, Fragment } from 'react';
import { Link } from 'react-router-dom'
import axios from 'axios';
import _ from 'lodash';
import { 
    Grid, 
    Item,
    Header,
    Placeholder,
    Container,
    Pagination
} from 'semantic-ui-react';

const preview_placeholder = _.times(6, (i) => (
    <Grid.Column  key={i}>
        <Placeholder>
            <Placeholder.Image style={{minWidth: '100px', minHeight: '100px'}} square/>
            <Placeholder.Line/>
        </Placeholder>
    </Grid.Column>
));

const BookPreviewList = (props) => {
    const [getBookPreviewUrl, setGetBookPreviewUrl] = useState(`${process.env.API_URL}` + '/books/previews?page=1&count=6');
    const [bookList, setBookList] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [activePage, setActivePage] = useState(1);
    const [bookProps, setBookProps] = useState(props.books);

    useEffect(() => {
        const source = axios.CancelToken.source();

        const body = { "asinArray": bookProps };
        const header = { cancelToken: source.token };
        axios.post(
            getBookPreviewUrl,
            body,
            header
        )
        .then(res => {
            setBookList([...res.data.body]);
            setIsLoading(false);
        });
    }, [getBookPreviewUrl]);

    const onPageChange = (e, pageInfo) => {
        setIsLoading(true);
        setActivePage(pageInfo.activePage);
        setGetBookPreviewUrl(`${process.env.API_URL}/books/previews?page=${pageInfo.activePage.toString()}&count=6`);
    }

    return (
        <Fragment>
            <Grid columns={6}>
                {
                    isLoading
                    ? preview_placeholder
                    : bookList.map((book, index) => {
                        return (
                            <Grid.Column key={index}>
                                <Link to={{pathname: `/review/${book.asin}`}}>
                                    <Item>
                                        <Item.Image verticalAlign='middle' size='small' style={{minWidth: '100px', minHeight: '100px'}} src={book.imUrl}/>
                                        <Header textAlign='center' as='h5'>{book.asin}</Header>
                                    </Item>
                                </Link>
                            </Grid.Column>
                        )
                    })
                }
            </Grid>
            <Container textAlign='center'>
                <Pagination
                    secondary
                    ellipsisItem={null}
                    activePage={activePage}
                    onPageChange={onPageChange}
                    totalPages={99}
                />
            </Container>
        </Fragment>
    )
}

export default BookPreviewList;