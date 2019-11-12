import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import {
    Segment,
    Grid,
    Header,
    Icon,
    Button,
    Table,
    Pagination,
    Placeholder
} from 'semantic-ui-react';
import axios from 'axios';

const preview_placeholder = _.times(50, (i) => (
    <Table.Row  key={i}>
        <Table.Cell>
            <Placeholder>
                <Placeholder.Line/>
            </Placeholder>
        </Table.Cell>
        <Table.Cell>
            <Placeholder>
                <Placeholder.Line/>
            </Placeholder>
        </Table.Cell>
        <Table.Cell>
            <Placeholder>
                <Placeholder.Line/>
            </Placeholder>
        </Table.Cell>
        <Table.Cell>
            <Placeholder>
                <Placeholder.Line/>
            </Placeholder>
        </Table.Cell>
        <Table.Cell>
            <Placeholder>
                <Placeholder.Line/>
            </Placeholder>
        </Table.Cell>
    </Table.Row>
));

const SeeLogList = (props) => {
    const [isHidden, setIsHidden] = useState(true);
    const [logList, setLogList] = useState([]);
    const [url, setUrl] = useState('http://52.205.122.23:5000/user/logs?page=1&count=50')
    const [activePage, setActivePage] = useState(1);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        axios.get(
            url
        )
        .then(res => {
            setLogList([...res.data]);
            setIsLoading(false);
        });
    }, [url])
    
    const onPageChange = (e, pageInfo) => {
        setIsLoading(true);
        setActivePage(pageInfo.activePage);
        setUrl(`http://52.205.122.23:5000/user/logs?page=${pageInfo.activePage.toString()}&count=50`)
    }

    return (
        <Grid>
            <Grid.Row>
                <Grid.Column width={16}>
                    {
                        isHidden
                        ?
                        <Segment placeholder>
                            <Header icon>
                                <Icon name='file pdf outline'/>
                                The files you are about to see are sensitive
                            </Header>
                            <Button primary onClick={() => setIsHidden(false)}>Show me</Button>
                        </Segment>
                        :
                        <Table celled striped>
                            <Table.Header>
                                <Table.Row>
                                        <Table.HeaderCell colSpan='5'>
                                            <Pagination
                                                secondary
                                                ellipsisItem={null}
                                                activePage={activePage}
                                                onPageChange={onPageChange}
                                                totalPages={99}
                                            />
                                        </Table.HeaderCell>
                                    </Table.Row>
                            </Table.Header>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>Time</Table.HeaderCell>
                                    <Table.HeaderCell>Method</Table.HeaderCell>
                                    <Table.HeaderCell>Pathname</Table.HeaderCell>
                                    <Table.HeaderCell>Body</Table.HeaderCell>
                                    <Table.HeaderCell>Status</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                            {
                                isLoading
                                ? preview_placeholder
                                :
                                logList.map((log, index) => {
                                    return (
                                            <Table.Row key={index}>
                                                <Table.Cell>
                                                    <Icon name='file alternate' size='large'/>
                                                    {log.time}
                                                </Table.Cell>
                                                <Table.Cell>
                                                    {log.method}
                                                </Table.Cell>
                                                <Table.Cell>
                                                    {log.path}
                                                </Table.Cell>
                                                <Table.Cell>
                                                    <Link to={{pathname: `/user_action/logs/${log.id}`}}>
                                                        {log.body}
                                                    </Link>
                                                </Table.Cell>
                                                <Table.Cell>
                                                    {log.status}
                                                </Table.Cell>
                                            </Table.Row>
                                        )
                                })
                            }
                            </Table.Body>
                            <Table.Footer>
                                <Table.Row>
                                    <Table.HeaderCell colSpan='5'>
                                        <Pagination
                                            secondary
                                            ellipsisItem={null}
                                            activePage={activePage}
                                            onPageChange={onPageChange}
                                            totalPages={99}
                                        />
                                    </Table.HeaderCell>
                                </Table.Row>
                            </Table.Footer>
                        </Table>
                    }
                </Grid.Column>
            </Grid.Row>
        </Grid>
    )

}

export default SeeLogList;