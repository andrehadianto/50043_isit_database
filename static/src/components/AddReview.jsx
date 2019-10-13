import React, { Component } from 'react';
import axios from 'axios';
import { Segment, Grid, Header, Form, Popup } from 'semantic-ui-react';

const { Row } = Grid;
const { Select, TextArea, Button } = Form;

const timeoutLength = 3000;

class AddReview extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isValidated: true
        };
        this.postReview = this.postReview.bind(this);
    }

    postReview(event) {
        console.log('submitting review');
        const review = event.target.elements.review.value;
        console.log(review);
        const book = "B000FA5SHK"; // book test
        const url = "http://localhost:5000/review/" + book;
        if (review === '') {
            this.setState({isValidated: false});
        }
    }

    render() {
        return (
            <Segment vertical padded>
                <Grid container verticalAlign='middle'>
                    <Row>
                        <Header as='h2'>
                            Add new review
                        </Header>
                    </Row>
                    <Row>
                        <Form onSubmit={this.postReview}>
                            <Select name='book' fluid placeholder='Select book' options={this.props.options}/>
                            <Popup 
                                position='top right'
                                content='Review cannot be empty'
                                onOpen={setTimeout(() => {this.setState({isValidated: true})}, timeoutLength)}
                                open={!this.state.isValidated}
                                trigger={
                                    <TextArea name='review' placeholder='How was the book?'/>
                            }/>
                            <Button>Submit</Button>
                        </Form>
                    </Row>
                </Grid>
            </Segment>
        );
    }
}

export default AddReview;