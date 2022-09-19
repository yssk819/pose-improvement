import React from 'react';
import './App.css';
import { BrowserRouter, Link, Routes, Route } from "react-router-dom";

const Home = () => <div style={styles.home}>Home</div>;
const Page1 = () => <div style={styles.page1}>Page1</div>;
const Page2 = () => <div style={styles.page2}>Page2</div>;

const styles = {
  home: {
    color: '#fff',
    fontSize: '64px',
    background: 'rgba(255, 100, 0)',
  },
  page1: {
    color: '#fff',
    fontSize: '64px',
    background: 'rgba(0, 150, 255)',
  },
  page2: {
    color: '#fff',
    fontSize: '64px',
    background: 'rgba(44, 219, 88)',
  },
}

const App = () => {

  return (
    <BrowserRouter>
      <div>
        <Link to="/">Home</Link>
        <br />
        <Link to="/page1">Page1</Link>
        <br />
        <Link to="/page2">Page2</Link>
        <br />

        <Routes>
          <Route index element={<Home />} />
          <Route path="page1" element={<Page1 />} />
          <Route path="page2" element={<Page2 />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
