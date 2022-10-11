import React from "react";
import { BrowserRouter, Link, Routes, Route } from "react-router-dom";

import './App.css';
import Home from "./pages/Home";
import Luggage from './pages/Luggage';
import Balance from './pages/Balance';
import Camera from "./pages/Camera";
import Result from './pages/Result';


const App = () => {

  return (
    <BrowserRouter>
      <div>
        <div className="header">
          <p>立ち姿勢判定アプリ</p>
        </div>

        <Routes>
          <Route index element={<Home />} />
          <Route path="luggage" element={<Luggage />} />
          <Route path="balance" element={<Balance />} />
          <Route path="camera" element={<Camera />} />
          <Route path="result" element={<Result />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;
