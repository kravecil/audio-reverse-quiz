import { Layout } from 'antd';
import React from 'react';

const { Header, Content, Footer } = Layout;

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header>
        Header
      </Header>
      <Content>
        Content
      </Content>
      <Footer>
        Footer
      </Footer>
    </Layout>
  );
};

export default App;