import React from "react";
import { Link } from "react-router-dom";


const Home = () => {
  return (
    <div>
      <p>カメラで撮影した写真から立ち姿勢を判定</p>

      <br />
      <Link to="/luggage">はじめる</Link>
    </div>
  );
}

export default Home;