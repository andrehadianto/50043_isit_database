import React, { Component } from 'react';
import axios from 'axios';
import BookPreviewList from '../components/BookPreviewList';
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
    Divider,
    Label
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
            reviewList: [],

            rating: 0

        }
        this.submitReviewHandler = this.submitReviewHandler.bind(this);
        this.handleRate = this.handleRate.bind(this);
    }

    componentDidMount() {
        const {match: {params}} = this.props;
        const bookUrl = `${process.env.API_URL}/book/${params.asin}`;
        axios.get(
            bookUrl
        )
        .then(res => {
            this.setState({
                bookDetails: res.data,
                bookIsLoading: false
            });
        })

        const reviewUrl = `${process.env.API_URL}/reviews/${params.asin}`;
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

    handleRate(e, {rating, maxRating}) {
        this.setState({rating})
    }

    submitReviewHandler(e) {
        const {match: {params}} = this.props;
        const overall = this.state.rating;
        const review = e.target.elements.review.value;
        const summary = e.target.elements.summary.value;

        if (!review || !summary) {
            alert("Summary and Review cannot be empty");
        } else if (sessionStorage.getItem('name') && sessionStorage.getItem('id') && sessionStorage.getItem('token')) {
            const formData = new FormData();
            formData.set('overall', overall);
            formData.set('reviewText', review);
            formData.set('reviewerID', sessionStorage.getItem('id'));
            formData.set('reviewerName', sessionStorage.getItem('name'));
            formData.set('summary', summary);
    
            const url = `${process.env.API_URL}/reviews/${params.asin}`;
            axios.post(
                url, 
                formData
            )
            .then(res => {
                window.location.reload(true);
            })
            .catch(err => {
                console.log(err);
            })
        } else {
            const nickname = e.target.elements.anonymous.value;

            const formData = new FormData();
            formData.set('overall', overall);
            formData.set('reviewText', review);
            formData.set('reviewerID', "ANONYMOUS");
            formData.set('reviewerName', nickname);
            formData.set('summary', summary);
    
            const url = `${process.env.API_URL}/reviews/${params.asin}`
            axios.post(
                url, 
                formData
            )
            .then(res => {
                window.location.reload(true);
            })
            .catch(err => {
                console.log(err);
            })
        }
    }

    render() {
        return (
            <div>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Segment>
                                Category
                            </Segment>
                        </Grid.Column>
                    </Grid.Row>
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
                            <Segment color='grey'>
                                {
                                    this.state.bookIsLoading
                                    ? title_placeholder
                                    : (this.state.bookDetails.price !== undefined && this.state.bookDetails.price !== 0)
                                    ? <Header textAlign='center' dividing color='pink'>SGD ${this.state.bookDetails.price}</Header>
                                    : <Header textAlign='center' dividing><Label tag color='pink'>Free of charge</Label></Header>
                                }
                            </Segment>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <Segment.Group>
                    <Segment padded vertical>
                        <Grid container>
                            <Grid.Column>
                                <Form onSubmit={this.submitReviewHandler}>
                                    <Container>
                                        <Rating
                                            name='overall'
                                            onRate={this.handleRate}
                                            style={{marginBottom: '10px'}}
                                            size='large'
                                            icon='star'
                                            maxRating={5}/>
                                    </Container>
                                    <Form.Input
                                        name='summary'
                                        placeholder='Summary'
                                        required
                                    />
                                    <Form.TextArea
                                        name='review'
                                        placeholder='Share your thoughts!'
                                        style={{minHeight: '6em'}}
                                        required
                                    />
                                    <Form.Group inline>
                                        <Form.Button type='submit' primary>Submit</Form.Button>
                                        {
                                            sessionStorage.getItem('name') && sessionStorage.getItem('id') && sessionStorage.getItem('token')
                                            ? null
                                            : <Form.Input name='anonymous' placeholder='Nickname' required/>
                                        }
                                    </Form.Group>

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
                                            ? <span style={{fontStyle: 'italic', fontSize: '120%', lineHeight: '1.5'}}>No review</span>
                                            : this.state.reviewList.reverse().map((review, index) => {
                                                const months_arr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                                                const date = new Date(review.unixReviewTime * 1000);
                                                const day = date.getDate();
                                                const month = months_arr[date.getMonth()];
                                                const year = date.getFullYear();
                                                return (
                                                    <div key={index}>
                                                        <Item>
                                                            <Item.Content>
                                                                <Item.Header as='h4'><span style={{color: 'blue'}}>{review.reviewerName}</span></Item.Header>
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
                
                {
                    this.state.bookIsLoading
                    ? title_placeholder
                    : <BookPreviewList books={this.state.bookDetails.related.also_bought}/>
                }
            </div>
        );
    }
}

export default BookDetails;