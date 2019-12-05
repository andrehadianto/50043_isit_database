import React, { Component, createRef, Fragment } from 'react';
import { Link } from 'react-router-dom';
import {
    Segment, 
    Grid, 
    Header, 
    Form, 
    Button, 
    Card,
    Image,
    Icon,
    Label,
    Message
} from 'semantic-ui-react';
import axios from 'axios';

const { Row, Column } = Grid;
const categoryOptions = []

class AddNewBook extends Component {
    constructor(props) {
        super(props);
        this.state = {
            file: null,
            title: 'The Art of Trolling',
            description: 'Never gonna give you up, never gonna let you down, never gonna turn around, to hurt you.',
            filter: ["Books", "Comedy"],
            price: 0.00,
            isHidden: true,
            uploadedBook: ''
        }
        this.fileInputRef = createRef();
        this.onFormSubmit = this.onFormSubmit.bind(this);
        this.onPreview = this.onPreview.bind(this);
    }

    componentDidMount() {
        const url = `${process.env.API_URL}/categories`;
        if (sessionStorage.getItem('categories') == null) {
            axios.get(
                url
            )
            .then(res => {
                sessionStorage.setItem('categories', JSON.stringify(res.data));
                JSON.parse(sessionStorage.getItem('categories')).map((catList, index) => {
                    catList.categories.map((cat, index) => {
                        categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                    })
                })
            });
        } else {
            JSON.parse(sessionStorage.getItem('categories')).map((catList, index) => {
                catList.categories.map((cat, index) => {
                    categoryOptions.push({ key: cat.toString().trim(), value: cat.toString().trim(), text: cat.toString() })
                })
            })
        }
    }

    onPreview(e) {
        this.setState({price: this.state.price, isHidden: true});
    }

    onFormSubmit(e) {
        this.setState({ isHidden: true })

        const url = `${process.env.API_URL}/book/new`;
        const title = this.state.title;
        const description = this.state.description;
        const price = this.state.price ? this.state.price : 0;
        const category = this.state.filter ? this.state.filter : ["Books"];

        const body = {
            "title": title,
            "description": description,
            "price": price,
            "categories": category,
            "imUrl": "https://i.kym-cdn.com/photos/images/newsfeed/000/096/044/trollface.jpg" // this.state.file.name
        }
        axios.post(
            url,
            body,
        )
        .then(res => {
            this.setState({ isHidden: false, uploadedBook: res.data.body.asin });
            console.log(res);

        })
        .catch(err => {
            console.log(err);
        })
    }

    render() {
        return (
            <Fragment>
                <Grid>
                    <Row>
                        <Column width={12}>
                                <Header as='h3' dividing>
                                    Add new book
                                </Header>
                                <Grid container verticalAlign='middle'>
                                    <Column>
                                        <Form onSubmit={this.onFormSubmit}>
                                            <Form.Input 
                                                name='title'  
                                                placeholder='Book title' 
                                                onChange={(e, data) => { this.state.title = data.value }}
                                                required
                                            />
                                            <Form.TextArea 
                                                name='description' 
                                                placeholder='Description' 
                                                style={{minHeight: '6em'}}
                                                onChange={(e, data) => { this.state.description = data.value }}
                                                required
                                            />
                                            <Form.Group inline>
                                                <Form.Input 
                                                    name='price' 
                                                    icon='dollar' 
                                                    iconPosition='left' 
                                                    type='number'
                                                    placeholder='0.00'
                                                    step='.01'
                                                    onChange={(e, data) => { this.state.price = data.value }}
                                                />
                                                <Form.Select 
                                                    name='filter' 
                                                    placeholder='Category'
                                                    options={ categoryOptions }
                                                    multiple
                                                    selection
                                                    clearable
                                                    search
                                                    onChange={(e, data) => { this.state.filter = data.value }}
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
                                            <Form.Group inline>
                                                <Form.Button type='submit' content='Submit' primary/>
                                                <Form.Button type='button' onClick={ this.onPreview } color='teal' content='Preview'/>
                                            </Form.Group>
                                        </Form>
                                    </Column>
                                </Grid>
                        </Column>
                        <Column width={4}>
                            <Segment vertical padded>
                                <Grid columns={4}>
                                    <Card>
                                        <Image 
                                            src='https://react.semantic-ui.com/images/avatar/large/matthew.png'
                                            label={{
                                                as: 'a',
                                                color: 'red',
                                                content: 'Preview',
                                                ribbon: 'right',
                                            }}
                                        />
                                        <Card.Content>
                                            <Card.Header>{this.state.title}</Card.Header>
                                            <Card.Meta>
                                                {
                                                    this.state.filter.map((cat, index) => {
                                                        return (
                                                            <Label key={index} size='tiny' content={cat}/>
                                                        )
                                                    })
                                                }
                                            </Card.Meta>
                                            <Card.Description>{this.state.description}</Card.Description>
                                        </Card.Content>
                                        <Card.Content extra>
                                            <Icon name='dollar'/>
                                            {this.state.price}
                                        </Card.Content>
                                    </Card>
                                </Grid>
                            </Segment>
                        </Column>
                    </Row>
                </Grid>
                <Message hidden={ this.state.isHidden } success>
                    <Message.Header>Your new book has been added successfully</Message.Header>
                    <Message.Content><Link to={{pathname: `/review/${this.state.uploadedBook}`}}>Click here</Link> to see your newly added book</Message.Content>
                </Message>
            </Fragment>
        );
    }
}

export default AddNewBook;