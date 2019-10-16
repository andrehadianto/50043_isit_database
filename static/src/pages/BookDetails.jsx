import React, { Component } from 'react';
import axios from 'axios';
import {
    Grid, 
    Segment,
    Image,
    Placeholder,
    Header,
    Item,
    Rating,
    Form,
    Container,
    Divider
} from 'semantic-ui-react';

const image_placeholder = (
    <Placeholder>
        <Placeholder.Image square/>
    </Placeholder>
)

const title_placeholder = (
    <Placeholder>
        <Placeholder.Line/>
    </Placeholder>
)
class BookDetails extends Component {
    constructor(props) {
        super(props);
        this.state = {
            bookIsLoading: true,
            reviewIsLoading: true,
            bookDetails: null,
            reviewList: []
        }
    }

    componentDidMount() {
        const {match: {params}} = this.props;
        const bookUrl = `http://localhost:5000/book/${params.asin}`;
        axios.get(
            bookUrl
        )
        .then(res => {
            this.setState({
                bookDetails: res.data,
                bookIsLoading: false
            });
        })

        const reviewUrl = `http://localhost:5000/reviews/${params.asin}`;
        axios.get(
            reviewUrl
        )
        .then(res => {
            this.setState({
                reviewList: [...res.data],
                reviewIsLoading: false
            });
        })
    }

    render() {
        return (
            <div>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={12}>
                            <Segment color='blue'>
                                <Grid>
                                    <Grid.Row>
                                        <Grid.Column width={5}>
                                            {
                                                this.state.bookIsLoading
                                                ? image_placeholder
                                                : <Image style={{minWidth: '250px', minHeight: '250px'}} src={this.state.bookDetails.imUrl}/>
                                            }
                                        </Grid.Column>
                                        <Grid.Column width={10}>
                                            <Segment vertical>
                                                {
                                                    this.state.bookIsLoading
                                                    ? title_placeholder
                                                    : <Header as='h3' dividing>{this.state.bookDetails.asin}</Header>
                                                }
                                                <Item.Description>
                                                    {
                                                        this.state.bookIsLoading
                                                        ? title_placeholder
                                                        : this.state.bookDetails.description === undefined
                                                            ? <span style={{fontStyle: 'italic', lineHeight: '1.5'}}>No description</span>
                                                            : this.state.bookDetails.description
                                                    }
                                                </Item.Description>
                                            </Segment>
                                        </Grid.Column>
                                    </Grid.Row>
                                </Grid>
                            </Segment>
                        </Grid.Column>
                        <Grid.Column width={4}>
                            <Segment>
                                HAHABAHBAHBAHBHA
                            </Segment>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <Segment.Group>
                    <Segment padded vertical>
                        <Grid container>
                            <Grid.Column>
                                <Form>
                                    <Container>
                                        <Rating style={{marginBottom: '10px'}} size='large' icon='star' maxRating={5}/>
                                    </Container>
                                    <Form.TextArea
                                        placeholder='Share your thoughts!'
                                        style={{minHeight: '6em'}}
                                    />
                                    <Form.Button primary>Submit</Form.Button>
                                </Form>
                            </Grid.Column>
                        </Grid>
                    </Segment>
                    <Segment padded vertical>
                        <Grid container>
                            <Grid.Column>
                                <Item.Group>
                                    {
                                        this.state.reviewIsLoading
                                        ? title_placeholder
                                        : !this.state.reviewList.length
                                            ? <span style={{fontStyle: 'italic', lineHeight: '1.5'}}>No review</span>
                                            : this.state.reviewList.map((review, index) => {
                                                const months_arr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                                                const date = new Date(review.unixReviewTime * 1000);
                                                const day = date.getDate();
                                                const month = months_arr[date.getMonth()];
                                                const year = date.getFullYear();
                                                return (
                                                    <div key={index}>
                                                        <Item>
                                                            <Item.Content>
                                                                <Item.Header as='h4'>{review.reviewerName}</Item.Header>
                                                                <Rating defaultRating={review.overall} maxRating={5} disabled/>
                                                                <span style={{ marginLeft: '2em' }}>{`${day} ${month} ${year}`}</span>
                                                                <Item.Meta>
                                                                    <h5>{review.summary}</h5>
                                                                </Item.Meta>
                                                                <Item.Description>
                                                                    {review.reviewText}
                                                                </Item.Description>
                                                            </Item.Content>
                                                        </Item>
                                                        <Divider/>
                                                    </div>
                                                )
                                            })
                                    }
                                </Item.Group>
                            </Grid.Column>
                        </Grid>
                    </Segment>

                </Segment.Group>
            </div>
        );
    }
}

export default BookDetails;