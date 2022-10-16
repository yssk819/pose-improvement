import React from "react";

const Home = (props) => {
  return (
    <div>
      <div className="Home-headline">
        <p className="Home-headline-p">AI姿勢推定で<br />立ち姿勢を改善しよう！</p>
      </div>

      <div className="Home-instruction">
        <p className="Home-instruction-p">本アプリでは...(アプリの説明)</p>
      </div>

      <div>
        <button onClick={() => props.navigate("/camera")}>はじめる</button>
      </div>

    </div>
  );
};

export default Home;