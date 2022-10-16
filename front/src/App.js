import React, {useState} from "react";
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import './App.css';
// import components
import Home from "./components/Home";
import Camera from "./components/Camera";
import Result from "./components/Result";

const App = () => {
  const [image, setImage] = useState();
  const [message, setMessage] = useState("判定待ち");
  const navigate = useNavigate();

  const reset = () => {
    navigate("/");
    setImage(null);
    setMessage("判定待ち");
  };

  return (
    <div>
      <div className="header">
        <h1>姿勢改善アプリ</h1>
      </div>

      <Routes>
        <Route path="/" element={<Home navigate={navigate} />} />
        <Route path="/camera" element={<Camera navigate={navigate} setMessage={setMessage} setImage={setImage} />} />
        <Route path="/result" element={<Result message={message} image={image} reset={reset} />} />
      </Routes>
    </div>
  );
};

export default App;
