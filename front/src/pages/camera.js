import React from "react";
import { Link } from "react-router-dom";


const Camera = () => {
  return (
    <div>
      これはCamera
      <br />
      <Link to="/result">Resultへ</Link>
    </div>
  );
}

export default Camera;