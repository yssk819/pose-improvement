import React from "react";
import { Link } from "react-router-dom";

import "./index.css"


const Balance = () => {
  return (
    <div className="balance">
      <p>足圧センサで重心位置を測定</p>

      <br />
      <Link to="/camera" className="link">次へ</Link>
    </div>
  );
}

export default Balance;