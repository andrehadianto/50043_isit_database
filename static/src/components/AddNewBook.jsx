import React, { Component } from 'react';
import { Segment, Grid, Header, Form } from 'semantic-ui-react';

class AddNewBook extends Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <Segment vertical padded>
                <Grid container verticalAlign='middle'>
                    <Grid.Row>
                        <Header as='h2'>
                            Add new book
                        </Header>
                    </Grid.Row>
                    <Grid.Row>
                        <Form>
                            <Form.Input fluid placeholder='Book title'/>
                            <Form.TextArea placeholder='Description'/>
                            <Form.Input fluid placeholder='price'/>
                            <Form.Select fluid placeholder='Select category' options={this.props.options}/>
                            <Form.Button>Submit</Form.Button>
                        </Form>
                    </Grid.Row>
                </Grid>
            </Segment>
        );
    }
}

export default AddNewBook;