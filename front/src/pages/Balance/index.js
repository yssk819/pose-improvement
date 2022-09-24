import React from "react";
import { Link } from "react-router-dom";

import "./index.css"


const Balance = () => {
  return (
    <div className="balance">
      これはBalance
      <br />
      <Link to="/camera" className="link">Cameraへ</Link>
    </div>
  );
}

export default Balance;