import React, { useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

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
    };

    axios.post(url, params).then((res) => {
      props.setMessage(res.data.message);
      props.setImage(res.data.image);
      props.navigate("/result");
    });
  };

  return (
    <div>
      <h2>Camera</h2>
      <p>カメラの正面に立って撮影してください。</p>

      <div>
        <Webcam
          audio={false}
          width={240}
          height={480}
          ref={webcamRef}
          screenshotFormat="image/png"
          videoConstraints={videoConstraints}
        />
      </div>

      <div>
        <button onClick={judge}>判定</button>
      </div>
    </div>
  );
};

export default Camera;