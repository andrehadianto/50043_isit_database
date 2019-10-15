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
    Form
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
            isLoading: true,
            bookDetails: null
        }
    }

    componentDidMount() {
        const {match: {params}} = this.props;
        const url = `http://localhost:5000/book/${params.asin}`;
        axios.get(
            url
        )
        .then(res => {
            this.setState({
                bookDetails: res.data,
                isLoading: false
            });
            console.log(this.state);
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
                                                this.state.isLoading
                                                ? image_placeholder
                                                : <Image style={{minWidth: '250px', minHeight: '250px'}} src={this.state.bookDetails.imUrl}/>
                                            }
                                        </Grid.Column>
                                        <Grid.Column width={10}>
                                            <Segment vertical>
                                                {
                                                    this.state.isLoading
                                                    ? title_placeholder
                                                    : <Header as='h3' dividing>{this.state.bookDetails.asin}</Header>
                                                }
                                                <Item.Description>
                                                    {
                                                        this.state.isLoading
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
                    <Segment vertical>
                        <Grid container>
                            <Grid.Column>
                                <Form>
                                    <Item.Content>
                                        <Rating icon='star' maxRating={5}/>
                                    </Item.Content>
                                    <Form.TextArea
                                        placeholder='Share your thoughts!'
                                        style={{minHeight: '6em'}}
                                    />
                                    <Form.Button primary>Submit</Form.Button>
                                </Form>
                            </Grid.Column>
                        </Grid>
                    </Segment>
                    <Segment vertical>
                        asdffds
                    </Segment>

                </Segment.Group>
            </div>
        );
    }
}

export default BookDetails;