import React, {useState} from "react";
import './App.css';
// import components
import Camera from "./components/Camera";
import Result from "./components/Result";

const App = () => {
  const [isGotResult, setIsGotResult] = useState(false);
  const [image, setImage] = useState();
  const [message, setMessage] = useState("判定待ち");

  const reset = () => {
    setIsGotResult(false);
    setImage(null);
    setMessage("判定待ち");
  };

  return (
    <div>
      <div className="header">
        <h1>姿勢改善アプリ</h1>
      </div>

      {!isGotResult ? 
        <Camera setImage={setImage} setMessage={setMessage} setIsGotResult={setIsGotResult} /> :
        <Result image={image} message={message} reset={reset} />
      }
    </div>
  );
};

export default App;
