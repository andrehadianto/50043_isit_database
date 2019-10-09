import React, { Component } from 'react';
import { Layout, Button } from 'antd';

const { Header, Content, Footer } = Layout;

class Home extends Component {
    render() {
        return (
            <Layout>
                <Header className="header">
                    <Button>Test</Button>
                </Header>
                <Content>
                    <div className="home">
                        <p>Content</p>
                    </div>
                </Content>
                <Footer>
                    <p>footer</p>
                </Footer>
            </Layout>
        )
    }
}

export default Home;