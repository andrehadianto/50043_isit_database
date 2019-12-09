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
            log: {},
            body: ''
        }
    }

    componentDidMount() {
        const {match: {params}} = this.props;
        const url = `${process.env.API_URL}/user/logs/${params.id}`;
        axios.get(
            url
        )
        .then(res => {
            this.setState({
                log: res.data,
                isLoading: false
            })
            try {
                this.setState({
                    body: JSON.stringify(JSON.parse(res.data.body), null, 1)
                })
            } catch(err) {
                this.setState({ body: res.data.body })
            }
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
                            <Table definition>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell/>
                                        <Table.HeaderCell>{this.state.log.id}</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>Time</Table.Cell>
                                        <Table.Cell>{this.state.log.time}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Method</Table.Cell>
                                        <Table.Cell>{this.state.log.method}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Path</Table.Cell>
                                        <Table.Cell>{this.state.log.path}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Status Code</Table.Cell>
                                        <Table.Cell>{this.state.log.status}</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>Body</Table.Cell>
                                        <Table.Cell>
                                            <pre>
                                                { this.state.body }
                                            </pre>
                                        </Table.Cell>
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