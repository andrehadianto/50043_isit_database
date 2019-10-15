import React, { Component } from 'react';
import { Segment, Grid, Header, Form } from 'semantic-ui-react';

const { Column } = Grid;

class AddNewBook extends Component {
    constructor(props) {
        super(props);
    }
    
    render() {
        return (
            <Segment padded>
                <Grid container verticalAlign='middle'>
                    <Column style={{minWidth: 600}}>
                        <Header as='h2'>
                            Add new book
                        </Header>
                        <Form>
                            <Form.Input fluid placeholder='Book title'/>
                            <Form.TextArea placeholder='Description'/>
                            <Form.Input fluid placeholder='price'/>
                            <Form.Select fluid placeholder='Select category' options={this.props.options}/>
                            <Form.Button primary>Submit</Form.Button>
                        </Form>
                    </Column>
                </Grid>
            </Segment>
        );
    }
}

export default AddNewBook;