import React, { Component } from 'react';
import axios from 'axios';
import _ from 'lodash';
import {
    Grid,
    Segment,
    Header,
    Image,
    Placeholder
} from 'semantic-ui-react';

const { Column } = Grid;

const preview_placeholder = _.times(12, (i) => (
    <Column> key={i}>
        <Placeholder>
            <Placeholder.Image square/>
        </Placeholder>
    </Column>
));

class AllBooks extends Component {
    constructor(props) {
        super(props);
        this.state = {
            bookPreviews: [],
            _isLoading: true
        };
    }

    componentDidMount() {
        const url = 'http://localhost:5000/books';
        axios.get(
            url
        )
        .then(res => {
            this.setState({
                bookPreviews: [...res.data],
                _isLoading: false
            });
        });
    }

    render() {
        return(
            <Column width={12}>
                <Segment>
                    <Header as='h3' dividing>
                        Hullo
                    </Header>
                    <Grid columns={6}>
                    {
                        this.state._isLoading
                        ? preview_placeholder
                        : this.state.bookPreviews.map((book, index) => {
                            return (
                                <Column key={index}>
                                    <Image src={book.imUrl}/>
                                </Column>
                            )
                        })
                    } 
                    </Grid>
                </Segment>
            </Column>
        );
    }
}

export default AllBooks;