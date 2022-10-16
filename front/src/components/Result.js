import React from "react";

const Result = (props) => {
  return (
    <div>
      <h2>Result</h2>

      <div>
        判定結果 : {props.message}
      </div>

      <div>
        <img src={`data:image/png;base64,${props.image}`} />
      </div>

      <div>
        <button onClick={props.reset}>Reset</button>
      </div>
    </div>
  );
};

export default Result;