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
    Divider,
    Container,
    Input,
    Button
} from 'semantic-ui-react';

const { Column } = Grid;

const preview_placeholder = _.times(24, (i) => (
    <Column  key={i}>
        <Placeholder>
            <Placeholder.Image style={{minWidth: '100px', minHeight: '100px'}} square/>
            <Placeholder.Line/>
        </Placeholder>
    </Column>
));

const AllBooks = (props) => {
    const [activePage, setActivePage] = useState(1);
    const [bookData, setBookData] = useState([]);
    const [getBookApiUrl, setGetBookApiUrl] = useState('http://52.7.180.215:5000/books?page=1&count=24');
    const [isLoading, setIsLoading] = useState(true);
    const [goToPage, setGoToPage] = useState(1);
    const [isInvalid, setIsInvalid] = useState(false);

    useEffect(() => {
        axios.get(
            getBookApiUrl
        )
        .then(res => {
            setBookData([...res.data]);
            setIsLoading(false);
        });
    }, [getBookApiUrl]);

    const onPageChange = (e, pageInfo) => {
        setIsLoading(true);
        setActivePage(pageInfo.activePage);
        setGetBookApiUrl(`http://52.7.180.215:5000/books?page=${pageInfo.activePage.toString()}&count=24`);
    }

    const goToClickHandler = (e) => {
        if (goToPage > 0) {
            setIsInvalid(false);
            setIsLoading(true);
            setActivePage(goToPage);
            setGetBookApiUrl(`http://52.7.180.215:5000/books?page=${goToPage.toString()}&count=24`);    
        } else {
            setIsInvalid(true);
        }
    }

    return (
        <Column width={12}>
            <Segment color='orange'>
                <Header as='h3' dividing>
                    List of Books
                </Header>
                <Grid columns={6}>
                {
                    isLoading
                    ? preview_placeholder
                    : bookData.map((book, index) => {
                        return (
                            <Column key={index}>
                                <Link to={{pathname: `/review/${book.asin}`}}>
                                    <Item>
                                        <Item.Image verticalAlign='middle' size='small' style={{minWidth: '100px', minHeight: '100px'}} src={book.imUrl}/>
                                        <Header textAlign='center' as='h5'>{book.asin}</Header>
                                    </Item>
                                </Link>
                            </Column>
                        )
                    })
                } 
                </Grid>
                <Divider/>
                <Container textAlign='center'>
                    <Pagination
                        secondary
                        ellipsisItem={null}
                        activePage={ activePage }
                        onPageChange={ onPageChange }
                        totalPages={99}
                    />
                    <Input 
                        onChange={ (e, {value}) => {setGoToPage(value)} }
                        value={goToPage}
                        style={{ width: '4em' }} 
                        action={ <Button content='Go' onClick={ goToClickHandler }/> }
                        error={isInvalid}
                    />
                </Container>
            </Segment>
        </Column>
    );
    
}

export default AllBooks;