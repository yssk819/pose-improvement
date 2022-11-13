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
  const [frontMessage, setFrontMessage] = useState(null);
  const [sideMessage, setSideMessage] = useState(null);
  const navigate = useNavigate();

  const reset = () => {
    navigate("/");
    setFrontImage(null);
    setSideImage(null);
    setFrontMessage(null);
    setSideMessage(null);
  };

  return (
    <div className="App">
      <div className="App-header">
        <Icon className="App-header-icon" />
        <h1 className="App-header-name">姿勢改善アプリ</h1>
      </div>

      <div className="App-main">
        <Routes>
          <Route path="/" element={<Home navigate={navigate} />} />
          <Route path="/camera1" element={<Camera navigate={navigate} isFront={true} setMessage={setFrontMessage} setImage={setFrontImage} />} />
          <Route path="/camera2" element={<Camera navigate={navigate} isFront={false} setMessage={setSideMessage} setImage={setSideImage} />} />
          <Route path="/result" element={<Result frontMessage={frontMessage} sideMessage={sideMessage} frontImage={frontImage} sideImage={sideImage} reset={reset} />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
