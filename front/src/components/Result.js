import React from "react";

import exampleFront from "./example_front.png";
import exampleSide from "./example_side.png";

const Result = (props) => {
  return (
    <div>
      <h1 className="Result-h1">判定結果</h1>

      <div className="Result-container">
        <div className="Result-image-container">
          <div>
            <div className="Result-image-res-container">
              <div className="Result-image-res-content">
                <h2 className="Result-image-h2">正面</h2>
                <img className="Result-image-res" src={`data:image/png;base64,${props.frontImage}`} alt="front" />
              </div>
              
              <div className="Result-image-res-content">
                <h2 className="Result-image-h2">側面</h2>
                <img className="Result-image-res" src={`data:image/png;base64,${props.sideImage}`} alt="side" />
              </div>
            </div>

            <div>
              <h2 className="Result-image-h2">お手本</h2>
            </div>

            <div className="Result-image-example-container">
              <div className="Result-image-example-content">
                <img className="Result-image-example" src={exampleFront} alt="example front" />
              </div>

              <div className="Result-image-example-content">
                <img className="Result-image-example" src={exampleSide} alt="example side" />
              </div>
            </div>
          </div>
        </div>

        <div className="Result-comment-container">
          <div>
            <div className="Result-comment-front">
              <h2 className="Result-comment-h2">アドバイス</h2>
              <h3 className="Result-comment-h3">正面</h3>
              <ul className="Result-comment-ul">
                {props.frontMessages.map((message) => {
                  return (
                    <li className="Result-comment-li">{message}</li>
                  )
                })}
              </ul>
            </div>
            <div className="Result-comment-side">
              <h3 className="Result-comment-h3">側面</h3>
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
    </div>
  );
};

export default Result;