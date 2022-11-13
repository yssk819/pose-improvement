import React, { useRef } from "react";
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
      "isFront": props.isFront,
    };

    axios.post(url, params).then((res) => {
      props.setMessage(res.data.message);
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
      <h2>カメラで撮影</h2>

      {props.isFront
        ? <p>体の正面を撮影してください。</p>
        : <p>体の側面を撮影してください。</p>}

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
        <button onClick={judge}>撮影</button>
      </div>
    </div>
  );
};

export default Camera;