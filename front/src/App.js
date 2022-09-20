import React from "react";
import { BrowserRouter, Link, Routes, Route } from "react-router-dom";

import './App.css';
import Home from "./pages/home";
import Luggage from './pages/luggage';
import Balance from './pages/balance';
import Camera from "./pages/camera";
import Result from './pages/result';


const App = () => {

  return (
    <BrowserRouter>
      <div>
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
