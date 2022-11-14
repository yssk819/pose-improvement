import React from "react";

const Wiiboard = (props) => {
  const BalanceBoard = require("wii-balance-board-pi");
  var balanceBoard = new BalanceBoard();
  balanceBoard.connect();
  balanceBoard.on("data", data => {
    console.log(data);
  });

  return (
    <div>
      Wiiboard
    </div>
  );
};

export default Wiiboard;
