import React, { Component } from 'react';
import axios from 'axios';
import {
    Grid,
    Placeholder,
    Table
} from 'semantic-ui-react';

const title_placeholder = (
    <Placeholder>
        <Placeholder.Line/>
    </Placeholder>
)

class LogPreview extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            log: {}
        }
    }

    componentDidMount() {
        const {match: {params}} = this.props;
        const url = `http://52.7.180.215:5000/user/logs/${params.id}`;
        axios.get(
            url
        )
        .then(res => {
            this.setState({
                log: res.data,
                isLoading: false
            })
            console.log(this.state)
        })
    }

    render() {
        return (
            <Grid>
                <Grid.Row>
                    <Grid.Column width={16}>
                        {
                            this.state.isLoading
                            ? title_placeholder
                            : 
                            <Table>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell>{this.state.log.id}</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>{this.state.log.time}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>{this.state.log.method}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>{this.state.log.path}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>{this.state.log.status}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>{this.state.log.body}</Table.Cell>
                                    </Table.Row>
                                </Table.Body>

                            </Table>
                        }
                    </Grid.Column>
                </Grid.Row>
            </Grid>
        )
    }
}

export default LogPreview;