import React from "react";

const Home = (props) => {
  return (
    <div>
      <h2>Home</h2>
      <p>AI姿勢推定で立ち姿勢を改善しよう！</p>

      <div>
        <button onClick={() => props.navigate("/camera")}>はじめる</button>
      </div>

    </div>
  );
};

export default Home;