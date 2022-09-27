import React, { useCallback, useRef, useState } from "react";
import { Link } from "react-router-dom";
import Webcam from "react-webcam";
import axios from "axios";

import "./index.css"


const videoConstraints = {
  width: 720,
  height: 360,
  facingMode: "user",
};

const Camera = () => {
  const url = "http://127.0.0.1:8000";
  const [message, setMessage] = useState("判定待ち");
  const webcamRef = useRef({});
  const [image, setImage] = useState();
  
  const judge = () => {
    const imageSrc = webcamRef.current.getScreenshot();

    const params = {
      "data": imageSrc,
    };

    axios.post(url, params).then((res) => {
      setMessage(res.data.message);
      setImage(res.data.image);
    })
  }

  return (
    <div>
      これはCamera
      <br />

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

      <div>
        判定結果 : {message}
      </div>

      <div>
        <img src={`data:image/png;base64,${image}`} />
      </div>

      <Link to="/result">Resultへ</Link>
    </div>
  );
}

export default Camera;