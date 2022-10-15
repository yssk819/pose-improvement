import React, { useCallback, useRef, useState } from "react";
import Webcam from "react-webcam";
import axios from "axios";

const videoConstraints = {
  width: 720,
  height: 360,
  facingMode: "user",
};

const Camera = (props) => {
  const url = "http://127.0.0.1:8000";
  const webcamRef = useRef({});
  
  const judge = () => {
    const imageSrc = webcamRef.current.getScreenshot();

    const params = {
      "data": imageSrc,
    };

    axios.post(url, params).then((res) => {
      props.setMessage(res.data.message);
      props.setImage(res.data.image);
      props.setIsGotResult(true);
    })
  }

  return (
    <div>
      <h2>Camera</h2>

      <div>
        <Webcam
          audio={false}
          width={540}
          height={360}
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
}

export default Camera;