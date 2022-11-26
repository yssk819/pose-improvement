import React, {useState} from "react";
import { Route, Routes, useNavigate } from "react-router-dom";
import './App.css';
// import components
import Home from "./components/Home";
import Camera from "./components/Camera";
import Result from "./components/Result";
import { ReactComponent as Icon } from "./components/accessibility-human.svg";

const App = () => {
  const [frontImage, setFrontImage] = useState();
  const [sideImage, setSideImage] = useState();
  const [frontMessages, setFrontMessages] = useState(null);
  const [sideMessages, setSideMessages] = useState(null);
  const navigate = useNavigate();

  const reset = () => {
    navigate("/camera1");
    setFrontImage(null);
    setSideImage(null);
    setFrontMessages(null);
    setSideMessages(null);
  };

  return (
    <div className="App">
      <div className="App-header">
        <Icon className="App-header-icon" />
        <h1 className="App-header-name">カメラで立ち姿勢を改善！</h1>
      </div>

      <div className="App-main">
        <Routes>
          <Route path="/" element={<Home navigate={navigate} />} />
          <Route path="/camera1" element={<Camera navigate={navigate} isFront={true} setMessages={setFrontMessages} setImage={setFrontImage} />} />
          <Route path="/camera2" element={<Camera navigate={navigate} isFront={false} setMessages={setSideMessages} setImage={setSideImage} />} />
          <Route path="/result" element={<Result frontMessages={frontMessages} sideMessages={sideMessages} frontImage={frontImage} sideImage={sideImage} reset={reset} />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
