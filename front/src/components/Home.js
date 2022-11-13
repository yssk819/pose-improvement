import React from "react";

const Home = (props) => {
  return (
    <div>
      <div className="Home-headline">
        <p className="Home-headline-p">AI姿勢推定で<br />立ち姿勢を改善しよう！</p>
      </div>

      <div className="Home-instruction">
        <p className="Home-instruction-p">本アプリでは、AI(人工知能)を用いて、人体の関節や体勢を検出し、起立時における正しい姿勢の判定を行う。</p>
        <h2>本アプリにおける"正しい姿勢"とは</h2>
        <ul className="Home-instruction-ul">
          <li>左右均等に体重がかかっており、重心の左右のブレがない</li>
          <li>肩、骨盤が地面と並行である</li>
          <li>背筋がまっすぐと伸びている</li>
          <li>横から見た時、耳、肩、腰、ひざ、くるぶしが一直線になっている</li>
        </ul>
      </div>

      <div>
        <button onClick={() => props.navigate("/camera1")}>はじめる</button>
      </div>

    </div>
  );
};

export default Home;