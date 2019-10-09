import React from 'react';
import { Layout } from 'antd';

const { Header, Content, Footer } = Layout;

class Home extends React.Component {
    render() {
        return (
            <Layout>
                <Header className="header">
                    <p>header</p>
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