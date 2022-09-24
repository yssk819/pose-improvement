import React, { useCallback, useRef, useState } from "react";
import { Link } from "react-router-dom";
import Webcam from "react-webcam";

import "./index.css"


const videoConstraints = {
  width: 720,
  height: 360,
  facingMode: "user",
};

const Camera = () => {
  const webcamRef = useRef({});
  const [url, setUrl] = useState();
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setUrl(imageSrc);
    }
  }, [webcamRef]);

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
          screenshotFormat="image/jpeg"
          videoConstraints={videoConstraints}
        />
      </div>

      <div>
        <button onClick={capture}>撮影</button>
      </div>

      <Link to="/result">Resultへ</Link>
    </div>
  );
}

export default Camera;