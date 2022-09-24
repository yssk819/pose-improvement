import React from "react";
import { Link } from "react-router-dom";


const Home = () => {
  return (
    <div>
      これはHome
      <br />
      <Link to="/luggage">Luggageへ</Link>
    </div>
  );
}

export default Home;