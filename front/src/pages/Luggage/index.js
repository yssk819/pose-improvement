import React from "react";
import { Link } from "react-router-dom";


const Luggage = () => {
  return (
    <div>
      <p>鞄を持っていますか？</p>
      
      <div>
        <input type="radio" name="luggage" value="はい"></input>はい
        <input type="radio" name="luggage" value="いいえ" checked></input>いいえ
      </div>

      <br />
      <Link to="/balance">次へ</Link>
    </div>
  );
}

export default Luggage;