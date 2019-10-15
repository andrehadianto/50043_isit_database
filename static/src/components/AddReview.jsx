import React, { Component } from 'react';
import axios from 'axios';
import { Segment, Grid, Header, Form, Message } from 'semantic-ui-react';

const { Column } = Grid;
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
            setTimeout(() => {this.setState({isValidated: true})}, timeoutLength);
            clearTimeout();
        }
    }

    render() {
        return (
            <Segment padded>
                <Grid container verticalAlign='middle'>
                    <Column style={{minWidth: 600}}>
                        <Header as='h2'>
                            Add new review
                        </Header>
                        <Form onSubmit={this.postReview}>
                            <Select name='book' placeholder='Select book' options={this.props.options}/>
                            <TextArea name='review' placeholder='How was the book?'/>
                            {!this.state.isValidated && <Message negative>Review cannot be empty</Message>}
                            <Button primary>Submit</Button>
                        </Form>
                    </Column>
                </Grid>
            </Segment>
        );
    }
}

export default AddReview;