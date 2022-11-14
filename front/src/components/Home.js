import React from "react";

import homeImage from "./home-image.png";

const Home = (props) => {
  return (
    <div>
      <div className="Home-headline">
        <p className="Home-headline-p">本アプリではAI姿勢推定を用いて、正面・側面の起立姿勢を測定し、正しい姿勢の判定を行います。</p>
      </div>

      <div className="Home-instruction-headline">
        <h2 className="Home-instruction-headline-h2">"正しい姿勢" とは</h2>
      </div>

      <div className="Home-instruction-content">
        <ul className="Home-instruction-content-ul">
          <li>① 左右均等な重心</li>
          <li>③ 伸びた背筋</li>
        </ul>

        <ul className="Home-instruction-content-ul">
          <li>② 肩、骨盤が地面と並行</li>
          <li>④ 耳、肩、腰、足が一直線</li>
        </ul>
      </div>

      <div>
        <button className="Home-button" onClick={() => props.navigate("/camera1")}>はじめる</button>
      </div>

      <div>
        <img className="Home-image" src={homeImage} alt="home" />
      </div>

    </div>
  );
};

export default Home;