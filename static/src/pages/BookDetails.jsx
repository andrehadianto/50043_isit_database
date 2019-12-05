import React, { Component, Fragment } from 'react';
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
    Label,
    Icon,
    Comment
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

const purchase_benefits = [
    {icon: "truck", text: " Free delivery for self collection"},
    {icon: "check circle outline", text: " Available at Kinokuniya"},
    {icon: "universal access", text: " Suitable for all"}
]

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
            console.log(this.state)
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
            <Fragment>
                <Grid>
                    <Grid.Row>
                        <Grid.Column width={12}>
                            <Grid>
                                <Grid.Row>
                                    <Grid.Column width={6}>
                                        {
                                            this.state.bookIsLoading
                                            ? image_placeholder
                                            : <Image style={{minWidth: '325', minHeight: '325'}} src={this.state.bookDetails.imUrl}/>
                                        }
                                    </Grid.Column>
                                    <Grid.Column width={10}>
                                        <Segment vertical>
                                            {
                                                this.state.bookIsLoading
                                                ? title_placeholder
                                                : this.state.bookDetails.title
                                                    ? <Header as='h3' dividing>{this.state.bookDetails.title}</Header>
                                                    : <Header as='h3' dividing>{this.state.bookDetails.asin}</Header>
                                            }
                                            <Item.Group>
                                                {
                                                    this.state.bookIsLoading
                                                    ? title_placeholder
                                                    : <Item>
                                                        {
                                                            this.state.bookDetails.categories[0].map((category, index) => {
                                                                return (
                                                                    <Label content={ category } key={ index }/>
                                                                )
                                                            })
                                                        }
                                                    </Item>
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
                                            </Item.Group>
                                        </Segment>
                                    </Grid.Column>
                                </Grid.Row>
                            </Grid>
                        </Grid.Column>
                        <Grid.Column width={4}>
                            <Grid>
                                <Grid.Row>
                                    <Grid.Column>
                                        <Segment vertical>
                                            {
                                                this.state.bookIsLoading
                                                ? title_placeholder
                                                : (this.state.bookDetails.price !== undefined && this.state.bookDetails.price !== 0)
                                                ? <Header as='h3' textAlign='center' dividing color='pink'>SGD {this.state.bookDetails.price}</Header>
                                                : <Header as='h3' textAlign='center' dividing color='pink'>Free of charge</Header>
                                            }
                                            <Item.Group link>
                                                {
                                                    purchase_benefits.map((item, index) => {
                                                        return (
                                                            <Item key={ index }>
                                                                <Item.Content verticalAlign='middle'>
                                                                    <Item.Description>
                                                                        <Icon size='large' name={item.icon}/>
                                                                        { item.text }
                                                                    </Item.Description>
                                                                </Item.Content>
                                                            </Item>
                                                        )
                                                    })
                                                }
                                            </Item.Group>
                                        </Segment>
                                    </Grid.Column>
                                </Grid.Row>
                            </Grid>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>
                <Grid>
                    <Grid.Row>
                        <Grid.Column>
                            <Container>
                                <Grid>
                                    <Grid.Column>
                                        <Comment.Group>
                                            <Header as='h3' dividing content='Reviews'/>
                                            {
                                                this.state.reviewIsLoading
                                                ? title_placeholder
                                                : !this.state.reviewList.length
                                                    ? <Comment content='Be the first one to leave a review!'/>
                                                    : this.state.reviewList.reverse().map((review, index) => {
                                                        const months_arr = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                                                        const date = new Date(review.unixReviewTime * 1000);
                                                        const day = date.getDate();
                                                        const month = months_arr[date.getMonth()];
                                                        const year = date.getFullYear();
                                                        return (
                                                            <Fragment key={index}>
                                                                <Comment>
                                                                    <Comment.Avatar as='a' src={`https://api.adorable.io/avatars/50/${review.reviewerName}.png`}/>
                                                                    <Comment.Content>
                                                                        <Comment.Author as='a'>{review.reviewerName}</Comment.Author>
                                                                        <Comment.Metadata>{`${day} ${month} ${year}`}</Comment.Metadata>
                                                                        {/* <Comment.Text><Rating defaultRating={review.overall} maxRating={5} disabled/></Comment.Text> */}
                                                                        <Comment.Text as='h5'><Rating defaultRating={review.overall} maxRating={5} disabled/>&nbsp;&nbsp;&nbsp;{ review.summary }</Comment.Text>
                                                                        <Comment.Text>{ review.reviewText }</Comment.Text>
                                                                    </Comment.Content>
                                                                </Comment>
                                                            </Fragment>
                                                        )
                                                    })
                                            }
                                        </Comment.Group>
                                    </Grid.Column>
                                </Grid>
                            </Container>

                            <Divider hidden/>
                            <Divider hidden/>
                            <Divider hidden/>

                            <Container>
                                <Grid>
                                    <Grid.Column>
                                        <Header as='h3' dividing content='Leave your Review'/>
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
                                                <Form.Button type='submit' content='Submit' labelPosition='left' icon='edit' primary/>
                                                {
                                                    sessionStorage.getItem('name') && sessionStorage.getItem('id') && sessionStorage.getItem('token')
                                                    ? null
                                                    : <Form.Input name='anonymous' placeholder='Nickname' required/>
                                                }
                                            </Form.Group>
                                        </Form>
                                    </Grid.Column>
                                </Grid>
                            </Container>
                        </Grid.Column>
                    </Grid.Row>
                </Grid>

                <Divider hidden/>
                <Divider hidden/>
                <Divider hidden/>

                <Container>
                    <Header as='h3' dividing content='People who bought this also bought'/>
                {
                    this.state.bookIsLoading
                    ? title_placeholder
                    : !this.state.bookDetails.related
                        ? <Comment content='This book is forever alone.'/>
                        : !this.state.bookDetails.related.also_bought
                            ? <Comment content='This book is forever alone.'/>
                            : <BookPreviewList books={this.state.bookDetails.related.also_bought}/>
                }
                </Container>
            </Fragment>
        );
    }
}

export default BookDetails;