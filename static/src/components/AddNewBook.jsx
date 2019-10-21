import React, { Component, createRef } from 'react';
import {
    Segment, 
    Grid, 
    Header, 
    Form, 
    Button 
} from 'semantic-ui-react';
import axios from 'axios';

const { Column } = Grid;

class AddNewBook extends Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null
        }
        this.fileInputRef = createRef();
        this.onFormSubmit = this.onFormSubmit.bind(this);
    }

    onFormSubmit(e) {
        const url = 'http://localhost:5000/book/new';
        const title = e.target.elements.title.value;
        const description = e.target.elements.description.value;
        const price = e.target.elements.price.value ? e.target.elements.price.value : 0;
        const category = e.target.elements.category.value ? e.target.elements.category.value : "";

        const json = {
            "title": title,
            "description": description,
            "price": price,
            "categories": [ category ],
            "imUrl": "https://knowyourmeme.com/photos/96044" // this.state.file.name
        }
        const config = { "Content-type": "application/json" };
        axios.post(
            url,
            json,
            config
        )
        .then(res => {
            console.log(res);
        })
        .catch(err => {
            console.log(err);
        })
    }

    render() {
        return (
            <Grid.Row>
                <Column width={12}>
                    <Segment color='teal' padded>
                        <Header as='h3' dividing>
                            Add new book
                        </Header>
                        <Grid container verticalAlign='middle'>
                            <Column>
                                <Form onSubmit={this.onFormSubmit}>
                                    <Form.Input 
                                        name='title'  
                                        placeholder='Book title' 
                                        required
                                    />
                                    <Form.TextArea 
                                        name='description' 
                                        placeholder='Description' 
                                        style={{minHeight: '6em'}}
                                        required
                                    />
                                    <Form.Group inline>
                                        <Form.Input 
                                            name='price' 
                                            icon='dollar' 
                                            iconPosition='left' 
                                            placeholder='0.00'
                                        />
                                        <Form.Input 
                                            name='category' 
                                            placeholder='Category'
                                        />
                                    </Form.Group>
                                    <Form.Field>
                                        <Button
                                            content="Choose Image"
                                            labelPosition="left"
                                            icon="file image"
                                            onClick={() => this.fileInputRef.current.click()}
                                            
                                        />
                                        <input
                                            ref={this.fileInputRef}
                                            type="file"
                                            onChange={(e) => {this.state.file = e.target.files[0]}}
                                            hidden
                                        />
                                    </Form.Field>
                                    <Form.Button type='submit' primary>Submit</Form.Button>
                                </Form>
                            </Column>
                        </Grid>
                    </Segment>
                </Column>
                <Column width={4}>
                    <Segment color='teal' padded>
                        <Grid columns={4}>
                            This part will contain the preview of the soon to be uploaded book
                        </Grid>
                    </Segment>
                </Column>
            </Grid.Row>
        );
    }
}

export default AddNewBook;