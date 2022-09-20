import React from "react";
import { Link } from "react-router-dom";


const Luggage = () => {
  return (
    <div>
      これはLuggage
      <br />
      <Link to="/balance">Balanceへ</Link>
    </div>
  );
}

export default Luggage;