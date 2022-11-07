import React from "react";

const Result = (props) => {
  return (
    <div>
      <h2>判定結果</h2>

      <div>
        評価 : そこそこ良い姿勢です
      </div>

      <div className="Result-container">
        <div className="Result-content">
          <div>
            <h3>正面</h3>
            <img className="Result-content-image" src={`data:image/png;base64,${props.frontImage}`} alt="front" />
          </div>
          <div className="Result-content-comment">
            正面コメント : {props.frontMessage}
          </div>
        </div>

        <div className="Result-content">
          <div>
            <h3>側面</h3>
            <img className="Result-content-image" src={`data:image/png;base64,${props.sideImage}`} alt="side" />
          </div>
          <div className="Result-content-comment">
            側面コメント : {props.sideMessage}
          </div>
        </div>
      </div>

      <div>
        <button onClick={props.reset}>Reset</button>
      </div>
    </div>
  );
};

export default Result;