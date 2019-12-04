import React, { useEffect, useState, Fragment } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import _ from 'lodash';
import {
    Grid,
    Header,
    Pagination,
    Placeholder,
    Item,
    Divider,
    Container,
    Input,
    Button,
    Label
} from 'semantic-ui-react';

const { Column } = Grid;

const preview_placeholder = _.times(24, (i) => (
    <Column  key={i}>
        <Placeholder>
            <Placeholder.Image style={{minWidth: '150px', minHeight: '150px'}} square/>
            <Placeholder.Line/>
        </Placeholder>
    </Column>
));

const FilteredBooks = (props) => {
    const [activePage, setActivePage] = useState(1);
    const [bookData, setBookData] = useState([]);
    const [getBookApiUrl, setGetBookApiUrl] = useState(`${process.env.API_URL}/books/category?page=1&count=24`);
    const [isLoading, setIsLoading] = useState(true);
    const [goToPage, setGoToPage] = useState(1);
    const [isInvalid, setIsInvalid] = useState(false);

    useEffect(() => {
        const body = { "categoryArray": props.location.state.filter };
        const header = { "Content-type": "application/json" };
        axios.post(
            getBookApiUrl,
            body,
            header
        )
        .then(res => {
            setBookData([...res.data.body]);
            setIsLoading(false);
        });
    }, [getBookApiUrl]);

    const onPageChange = (e, pageInfo) => {
        setIsLoading(true);
        setActivePage(pageInfo.activePage);
        setGetBookApiUrl(`${process.env.API_URL}/books/category?page=${pageInfo.activePage.toString()}&count=24`);
    }

    const goToClickHandler = (e) => {
        if (goToPage > 0) {
            setIsInvalid(false);
            setIsLoading(true);
            setActivePage(goToPage);
            setGetBookApiUrl(`${process.env.API_URL}/books/category?page=${goToPage.toString()}&count=24`);    
        } else {
            setIsInvalid(true);
        }
    }

    return (
        <Fragment>
            <Grid>
            {
                props.location.state.filter.map((category, index) => {
                    return (
                        <Label content={ category } key={ index }/>
                    )
                })
            }
            </Grid>
            <Grid>
                <Column width={16}>
                        <Grid columns={6}>
                        {
                            isLoading
                            ? preview_placeholder
                            : bookData.map((book, index) => {
                                return (
                                    <Column key={index}>
                                        <Link to={{pathname: `/review/${book.asin}`}}>
                                            <Item>
                                                <Item.Image verticalAlign='middle' size='small' style={{minWidth: '150px', minHeight: '150px'}} src={book.imUrl}/>
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
                </Column>
            </Grid>
        </Fragment>
    );
    
}

export default FilteredBooks;