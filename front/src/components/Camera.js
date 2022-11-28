import React, { useRef } from "react";
import Webcam from "react-webcam";
import axios from "axios";

import exampleFront from "./example_front.png";
import exampleSide from "./example_side.png";

const videoConstraints = {
  width: 360,
  height: 720,
  facingMode: "user",
};

const Camera = (props) => {
  const webcamRef = useRef({});
  
  const judge = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    const url = "http://127.0.0.1:8000";

    const params = {
      "data": imageSrc,
      "isFront": props.isFront,
    };

    axios.post(url, params).then((res) => {
      props.setMessages(res.data.messages);
      props.setImage(res.data.image);
      if (props.isFront) {
        props.navigate("/camera2");
      }
      else {
        props.navigate("/result");
      }
    });
  };

  return (
    <div>
      {props.isFront
        ? <h2>体の正面を撮影</h2>
        : <h2>体の側面を撮影</h2>}
      <p>※マスクは外してください。</p>

      <div className="Camera-container">
        <div className="Camera-example-container">
          <div className="Camera-example-content">
            {/* <h3>お手本</h3> */}
            {props.isFront
              ? <img className="Camera-example" src={exampleFront} alt="example front" />
              : <img className="Camera-example" src={exampleSide} alt="example side" />
            }
          </div>
        </div>

        <div className="Camera-webcam-container">
          <div className="Camera-webcam-content">
            <Webcam
              audio={false}
              width={240}
              height={480}
              ref={webcamRef}
              screenshotFormat="image/png"
              videoConstraints={videoConstraints}
            />
          </div>
        </div>

        <div className="Camera-button-container">
          <div className="Camera-button-content">
            <button className="Camera-button" onClick={judge}>撮影</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Camera;
