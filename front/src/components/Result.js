import React from "react";

import exampleFront from "./example_front.png";
import exampleSide from "./example_side.png";

const Result = (props) => {
  return (
    <div>
      <h2>判定結果</h2>

      <div className="Result-container">
        <div className="Result-image-container">
          <div className="Result-image-content">
            <h3>正面</h3>
            <div>
              <img className="Result-image" src={`data:image/png;base64,${props.frontImage}`} alt="front" />
            </div>
            <div>
              <img className="Result-image-example" src={exampleFront} alt="example front" />
            </div>
          </div>

          <div className="Result-image-content">
            <h3>側面</h3>
            <div>
              <img className="Result-image" src={`data:image/png;base64,${props.sideImage}`} alt="side" />
            </div>
            <div>
              <img className="Result-image-example" src={exampleSide} alt="example side" />
            </div>
          </div>
        </div>

        <div className="Result-comment-container">
          <div className="Result-comment-front">
            <p>正面コメント</p>
            <ul className="Result-comment-ul">
              {props.frontMessages.map((message) => {
                return (
                  <li className="Result-comment-li">{message}</li>
                )
              })}
            </ul>
          </div>
          <div className="Result-comment-side">
            <p>側面コメント</p>
            <ul className="Result-comment-ul">
              {props.sideMessages.map((message) => {
                return (
                    <li className="Result-comment-li">{message}</li>
                )
              })}
            </ul>
          </div>

          <div>
            <button className="Result-reset-button" onClick={props.reset}>もう一回</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Result;